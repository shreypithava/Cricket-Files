import json
import sqlite3

from manager import Manager
from player import Player
from scoreboard import ScoreBoard


class Database(object):
    def __init__(self):
        self.__db = None

    def before_game(self, owner_id):
        self.__db = sqlite3.connect('database.db')

        owner_query = 'SELECT * FROM Player WHERE OwnerID = {}' \
            .format(owner_id)
        list_of_players = []
        for player_record in self.__db.execute(owner_query):
            list_of_players.append(Player(player_record))

        self.__db.close()
        return list_of_players

    def after_game(self, manager1: 'Manager', manager2: 'Manager',
                   result1, result2, scoreboard):
        self.__db = sqlite3.connect('database.db')

        self.__update_match(scoreboard, manager1.get_id(), manager2.get_id())
        self.__update_managers(manager1.get_id(), manager2.get_id(),
                               result1, result2)

        self.__update_players(manager1.get_team().get_players())
        self.__update_players(manager2.get_team().get_players())

        self.__commit()
        self.__db.close()

    def __update_match(self, scoreboard: 'ScoreBoard', id1, id2):
        scorecard1, scorecard2 = (scoreboard.return_scorecard(1),
                                  scoreboard.return_scorecard(2))

        stats_json = {"inning_1": {"bat": [], "bowl": []},
                      "inning_2": {"bat": [], "bowl": []}}

        for player in scorecard1.get_list_of_batsman():
            person = [player.get_id(), player.get_bat_stats()[:2]]
            stats_json['inning_1']['bat'].append(person)
        for player in scorecard1.get_list_of_bowlers():
            person = [player.get_id(), player.get_bowl_stats()]
            stats_json['inning_1']['bowl'].append(person)
        for player in scorecard2.get_list_of_batsman():
            person = [player.get_id(), player.get_bat_stats()[:2]]
            stats_json['inning_2']['bat'].append(person)
        for player in scorecard2.get_list_of_bowlers():
            person = [player.get_id(), player.get_bowl_stats()]
            stats_json['inning_2']['bowl'].append(person)

        # PRAGMA foreign_keys = on;

        self.__db.execute("""INSERT INTO Match
        (ManagerID1, ManagerID2) VALUES (?, ?)""", (id1, id2))

        match_id = self.__db.execute("""SELECT COUNT(*)
        FROM Match""").fetchone()[0]

        self.__db.execute("""UPDATE Match SET
        Inning_1 = (SELECT json_set(
        json(Inning_1), '$.bat', json(?), '$.bowl', json(?)) FROM Match),
        Inning_2 = (SELECT json_set(
        json(Inning_2), '$.bat', json(?), '$.bowl', json(?)) FROM Match)
        WHERE ID = ?""", (str(stats_json['inning_1']['bat']),
                          str(stats_json['inning_1']['bowl']),
                          str(stats_json['inning_2']['bat']),
                          str(stats_json['inning_2']['bowl']),
                          match_id))

    def __update_players(self, players: 'list[Player]'):
        for player in players:
            bat_stats, bowl_stats = player.get_bat_stats(), \
                                    player.get_bowl_stats()

            select_query = 'SELECT {}, {}, {} FROM Player WHERE ID = {}' \
                .format('Bat_stats', 'Bowl_stats', 'Match_stats',
                        player.get_id())
            record = self.__db.execute(select_query).fetchone()

            bat_records, bowl_records, match_records = (json.loads(record[0]),
                                                        json.loads(record[1]),
                                                        json.loads(record[2]))

            fifty, century = bat_records['50s'], bat_records['100s']
            if bat_stats[0] >= 50:
                if bat_stats[0] >= 100:
                    century += 1
                else:
                    fifty += 1

            four_wik, fiv_wik = bowl_records['4wi'], bowl_records['5wi']
            if bowl_stats[3] >= 4:
                if bowl_stats[3] >= 5:
                    fiv_wik += 1
                else:
                    four_wik += 1

            innings, not_outs = (match_records['innings'],
                                 match_records['not_outs'])
            if bat_stats[4]:
                if bat_stats[5]:
                    not_outs += 1
                innings += 1

            bat_set = {"runs": bat_records['runs'] + bat_stats[0],
                       "balls": bat_records['balls'] + bat_stats[1],
                       "4s": bat_records['4s'] + bat_stats[2],
                       "6s": bat_records['6s'] + bat_stats[3],
                       "50s": fifty, "100s": century}
            bowl_set = {"balls": bowl_records['balls'] + bowl_stats[0],
                        "wickets": bowl_records['wickets'] + bowl_stats[3],
                        "maidens": bowl_records['maidens'] + bowl_stats[1],
                        "runs": bowl_records['runs'] + bowl_stats[2],
                        "4wi": four_wik, "5wi": fiv_wik}
            match_set = {"matches": match_records['matches'] + 1,
                         "innings": innings, "not_outs": not_outs}

            self.__db.execute("""UPDATE Player SET
            Bat_stats = (SELECT json_set(json(Bat_stats), '$.runs', ?,
            '$.balls', ?, '$.4s', ?, '$.6s', ?, '$.50s', ?, '$.100s', ?)
            FROM Player),
            Bowl_stats = (SELECT json_set(json(Bowl_stats), '$.balls', ?,
            '$.wickets', ?, '$.maidens', ?, '$.runs', ?, '$.4wi', ?,
            '$.5wi', ?) FROM Player),
            Match_stats = (SELECT json_set(json(Match_stats), '$.matches', ?,
            '$.innings', ?, '$.not_outs', ?) From Player)
            WHERE ID = ?""", (bat_set['runs'], bat_set['balls'], bat_set['4s'],
                              bat_set['6s'], bat_set['50s'], bat_set['100s'],
                              bowl_set['balls'], bowl_set['wickets'],
                              bowl_set['maidens'], bowl_set['runs'],
                              bowl_set['4wi'], bowl_set['5wi'],
                              match_set['matches'], match_set['innings'],
                              match_set['not_outs'], player.get_id()))

    def __update_managers(self, id1, id2, result1, result2):
        query1 = 'SELECT * FROM Manager WHERE ID = {}'.format(id1)
        records1 = self.__db.execute(query1).fetchone()[1:]
        self.__db.execute('UPDATE Manager SET {} = ? WHERE ID = ?'.format(
            self.__text(result1)), (records1[result1] + 1, id1))

        query2 = 'SELECT * FROM Manager WHERE ID = {}'.format(id2)
        records2 = self.__db.execute(query2).fetchone()[1:]
        self.__db.execute('UPDATE Manager SET {} = ? WHERE ID = ?'.format(
            self.__text(result2)), (records2[result2] + 1, id2))

    def __commit(self):
        # self.__db.commit()
        pass

    @staticmethod
    def __text(result: 'int') -> str:
        if result == 0:
            return 'Win'
        elif result == 1:
            return 'Loss'
        return 'Tie'

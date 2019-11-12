import json
import sqlite3

from player import Player


class Team(object):

    def __init__(self, team_id: 'int'):
        self.__players: 'list[Player]' = list()
        self.__set_players(team_id)

    def __set_players(self, owner_id):
        db = sqlite3.connect('database.db')

        owner_query = 'SELECT * FROM Player WHERE OwnerID = {}' \
            .format(owner_id)
        for player_record in db.execute(owner_query):
            self.__players.append(Player(player_record))

        db.close()

    def get_players(self) -> 'list[Player]':
        return self.__players

    def update_stats_in_database(self, db: 'sqlite3.Connection'):
        for player in self.__players:
            bat_stats, bowl_stats = player.get_bat_stats(), \
                                    player.get_bowl_stats()

            select_query = 'SELECT {}, {}, {} FROM Player WHERE ID = {}' \
                .format('Bat_stats', 'Bowl_stats', 'Match_stats',
                        player.get_id())
            record = db.execute(select_query).fetchone()

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

            db.execute("""UPDATE Player SET
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

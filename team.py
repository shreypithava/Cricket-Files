import json
import sqlite3

from player import Player


class Team(object):

    def __init__(self, team_id: 'int'):
        self.__players: 'list[Player]' = list()
        self.__set_players(team_id)

    def __set_players(self, owner_id):
        list_of_ids = list()

        db = sqlite3.connect('database.db')
        query = 'SELECT ID FROM Player WHERE OwnerID = {}'.format(owner_id)
        for player_id in db.execute(query):
            list_of_ids.append(player_id[0])
        db.close()

        for i_d in list_of_ids:
            self.__players.append(Player(i_d))

    def get_players(self) -> 'list[Player]':
        return self.__players

    def update_stats_in_database(self):
        db = sqlite3.connect('database.db')
        for player in self.__players:
            bat_stats, bowl_stats = player.get_bat_stats(), \
                                    player.get_bowl_stats()

            ba_stats, bo_stats = 'Bat_stats', 'Bowl_stats'
            select_query = 'SELECT {}, {} FROM Player WHERE ID = {}' \
                .format(ba_stats, bo_stats, player.get_id())
            record = db.execute(select_query).fetchone()

            bat_records, bowl_records = (json.loads(record[0]),
                                         json.loads(record[1]))

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

            bat_set = {"runs": bat_records['runs'] + bat_stats[0],
                       "balls": bat_records['balls'] + bat_stats[1],
                       "4s": bat_records['4s'] + bat_stats[2],
                       "6s": bat_records['6s'] + bat_stats[3],
                       "50s": fifty, "100s": century}
            bowl_set = {"balls": bowl_records['balls'] + bat_stats[0],
                        "wickets": bowl_records['wickets'] + bowl_stats[3],
                        "maidens": bowl_records['maidens'] + bowl_stats[1],
                        "runs": bowl_records['runs'] + bowl_records[2],
                        "4wi": four_wik, "5wi": fiv_wik}

            update_query = 'UPDATE Player SET {} = {}, {} = {} WHERE ID = {}' \
                .format(ba_stats, bat_set, bo_stats, bowl_set, player.get_id())
            db.execute(update_query)

        # db.commit()
        db.close()

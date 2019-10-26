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
        for player in self.__players:
            player.update_stats_to_database()

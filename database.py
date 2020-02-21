import sqlite3

from player import Player


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

    def after_game(self):
        self.__update_managers()
        self.__update_players()

    def __update_players(self):
        pass

    def __update_managers(self):
        pass

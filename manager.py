import sqlite3

from team import Team


class Manager(object):

    def __init__(self, manager_id: 'int'):
        self.__id = manager_id
        self.__team = Team(self.__id)

    def get_team(self) -> Team:
        return self.__team

    def get_id(self):
        return self.__id

    def update_manager_and_player_database(self, result: 'int',
                                           db: 'sqlite3.Connection'):
        query = 'SELECT * FROM Manager WHERE ID = {}'.format(self.__id)
        records = db.execute(query).fetchone()[1:]

        if result == 0:
            db.execute('UPDATE Manager SET Win = ? WHERE ID = ?;',
                       (records[0] + 1, self.__id))
        elif result == 1:
            db.execute('UPDATE Manager SET Loss = ? WHERE ID = ?;',
                       (records[1] + 1, self.__id))
        else:
            db.execute('UPDATE Manager SET Tie = ? WHERE ID = ?;',
                       (records[2] + 1, self.__id))

        self.__team.update_stats_in_database(db)

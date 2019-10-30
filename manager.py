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

    def update_manager_database(self, result: 'int'):
        query = 'SELECT * FROM Manager WHERE ID = {}'.format(self.__id)
        db = sqlite3.connect('database.db')
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

        # db.commit()
        db.close()

    def update_stats_in_database(self):
        self.__team.update_stats_in_database()

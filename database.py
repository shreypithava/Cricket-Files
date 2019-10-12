import sqlite3


class Database(object):
    def __init__(self):
        self.__file_name = "database.db"

    def connect_and_close(self):
        db = sqlite3.connect(self.__file_name)
        # TODO: run commands here
        db.close()

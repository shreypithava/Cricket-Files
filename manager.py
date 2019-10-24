from team import Team


class Manager(object):

    def __init__(self, name: 'str'):
        self.__id = name  # future developments
        # TODO: in future, get team from database by passing self.__id
        self.__team = Team()

    def get_team(self) -> Team:
        return self.__team

    # TODO: look at line 25 in game.py8
    def update_stats_in_database(self):
        pass

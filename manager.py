from team import Team


class Manager(object):

    def __init__(self, manager_id, players):
        self.__id = manager_id
        self.__team = Team(players)

    def get_team(self) -> Team:
        return self.__team

    def get_id(self):
        return self.__id

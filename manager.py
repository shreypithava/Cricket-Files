from team import Team


# TODO: complete Manager class
class Manager(object):
    def __init__(self):
        self.__id = None  # future developments
        # TODO: in future, get team from database by passing self.__id
        self.__team = Team()

    def get_team(self):
        return self.__team

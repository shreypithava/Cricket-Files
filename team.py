from player import Player


class Team(object):

    def __init__(self):
        self.__players: 'list[Player]' = list()
        self.__set_players()

    # TODO: modify and get players from database, maybe make this method static
    # TODO: also look at line 13 in manager.py
    def __set_players(self):
        for _ in range(11):
            self.__players.append(Player())

    def get_players(self) -> 'list[Player]':
        return self.__players

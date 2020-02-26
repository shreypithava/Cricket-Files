from player import Player


class Team(object):

    def __init__(self, players):
        self.__players: 'list[Player]' = players

    def get_players(self) -> 'list[Player]':
        return self.__players

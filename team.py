from random import randint

from player import Player, Personal


class Team(object):

    def __init__(self):
        self.__players: 'list[Player]' = list()
        self.__set_players()

    # TODO: modify and complete __set_players
    def __set_players(self):
        for _ in range(11):
            self.__players.append(Player(
                personal=Personal(name=str(randint(10000, 100000)))))

    def get_players(self):
        return self.__players

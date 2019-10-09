from random import choices
from string import ascii_lowercase, digits

from player import Player, Personal


def return_random():
    return "".join(choices(ascii_lowercase + digits, k=7))


class Team(object):

    def __init__(self):
        self.__players: 'list[Player]' = list()
        self.__set_players()

    # TODO: modify and get players from database, maybe make this method static
    def __set_players(self):
        for _ in range(11):
            self.__players.append(Player(
                personal=Personal(name=return_random())))

    def get_players(self):
        return self.__players

from engine import Engine
from manager import Manager
from scoreboard import ScoreBoard


# TODO: complete game class
class Game(object):
    def __init__(self):
        self.__player1 = Manager()
        self.__player2 = Manager()
        self.__engine = Engine()
        self.__scoreboard = ScoreBoard()

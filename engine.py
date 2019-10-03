from random import choice, shuffle

from team import Team
from scoreboard import ScoreBoard


def return_fake_probabilities():
    the_list = list()
    for number in range(100):
        if number < 15:
            the_list.append(0)
        elif number < 30:
            the_list.append(1)
        elif number < 45:
            the_list.append(2)
        elif number < 60:
            the_list.append(3)
        elif number < 75:
            the_list.append(4)
        elif number < 90:
            the_list.append(6)
        else:
            the_list.append(-1)
    return the_list


class Engine(object):  # think about Game class
    def __init__(self):
        self.__blue_team = Team()
        self.__red_team = Team()
        self.__scoreboard = ScoreBoard(self.__blue_team.get_players(), self.__red_team.get_players())

    def __get_team(self, blue: 'bool'):
        return self.__blue_team if blue else self.__red_team

    def play_game(self):
        print(self.__red_team)
        for ball in range(30):
            pass
            result = choice(shuffle(return_fake_probabilities()))
            if result >= 0:
                pass
            else:
                pass

    def __return_probabilities(self):  # complete this later
        # runs_list = list()
        # print(self.__red_team)
        # while sum(runs_list) != 100:
        #     runs_list = list()
        #     runs_list.append(randint(0, ))
        #
        # return runs_list
        pass


if __name__ == '__main__':
    engine = Engine()
    # engine.play_game()

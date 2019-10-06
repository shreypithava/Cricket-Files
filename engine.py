from random import choice, shuffle

from scoreboard import ScoreBoard
from team import Team


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


list_of_probability = return_fake_probabilities()


# TODO: think about Game Class
class Engine(object):
    def __init__(self):
        self.__blue_team = Team()
        self.__red_team = Team()
        self.__scoreboard = ScoreBoard(self.__blue_team, self.__red_team)

    def play_game(self):
        self.__play_innings(False)
        self.__scoreboard.switch()
        self.__play_innings(True)
        self.__print_results()

    def __play_innings(self, second_innings: 'bool'):
        for _ in range(30):
            shuffle(list_of_probability)
            result = choice(list_of_probability)
            self.__scoreboard.action(result)
            if second_innings and \
                    (self.__scoreboard.return_two_scorecard().return_total_runs() >
                     self.__scoreboard.return_one_scorecard().return_total_runs() or
                     self.__scoreboard.return_two_scorecard().wickets_related(True)):
                break
            if not second_innings and self.__scoreboard.return_one_scorecard().wickets_related(True):
                break

    # TODO: complete this function in future
    def __return_probabilities(self):
        pass

    def __print_results(self):
        scorecard1, scorecard2 = self.__scoreboard.return_one_scorecard(), self.__scoreboard.return_two_scorecard()
        print("Team 1: {}/{} {}.{}".format(scorecard1.return_total_runs(), scorecard1.wickets_related(False),
                                           scorecard1.return_balls() // 6, scorecard1.return_balls() % 6))
        print("Team 2: {}/{} {}.{}".format(scorecard2.return_total_runs(), scorecard2.wickets_related(False),
                                           scorecard2.return_balls() // 6, scorecard2.return_balls() % 6))


if __name__ == '__main__':
    engine = Engine()
    engine.play_game()

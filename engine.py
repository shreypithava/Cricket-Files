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

    def play_game(self, overs: 'int'):
        self.__play_innings(False, overs)
        self.__scoreboard.switch()
        self.__play_innings(True, overs)
        self.__print_results()

    def __play_innings(self, second_innings: 'bool', overs: 'int'):
        for _ in range(overs * 6):
            shuffle(list_of_probability)
            result = choice(list_of_probability)
            self.__scoreboard.action(result)
            if (second_innings and
                (self.__scoreboard.return_two_scorecard().return_batting(1) >
                 self.__scoreboard.return_one_scorecard().return_batting(1)
                 or
                 self.__scoreboard.return_two_scorecard().wickets() == 10)) \
                    or (
                    not second_innings and
                    self.__scoreboard.return_one_scorecard().wickets() == 10):
                break

    # TODO: complete this function in future
    def __return_probabilities(self):
        pass

    def __print_results(self):
        scorecard1, scorecard2 = (self.__scoreboard.return_one_scorecard(),
                                  self.__scoreboard.return_two_scorecard())

        print("Team 1: {}/{} {}.{} 4: {}, 6: {}".format(
            scorecard1.return_batting(1),
            scorecard1.wickets(),
            scorecard1.return_batting(2) // 6,
            scorecard1.return_batting(2) % 6,
            scorecard1.return_batting(3),
            scorecard1.return_batting(4)))

        print("Team 2: {}/{} {}.{} 4: {}, 6: {}".format(
            scorecard2.return_batting(1),
            scorecard2.wickets(),
            scorecard2.return_batting(2) // 6,
            scorecard2.return_batting(2) % 6,
            scorecard2.return_batting(3),
            scorecard2.return_batting(4)))


if __name__ == '__main__':
    engine = Engine()
    engine.play_game(overs=20)

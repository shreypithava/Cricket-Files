from engine import Engine
from manager import Manager
from scoreboard import ScoreBoard


# TODO: complete game class
class Game(object):

    def __init__(self, overs: 'int'):
        self.__player1 = Manager()
        self.__player2 = Manager()
        self.__overs = overs
        self.__engine = Engine()
        self.__scoreboard = ScoreBoard(self.__player1.get_team(),
                                       self.__player2.get_team())

    def play(self):
        self.__play_innings(False)
        self.__scoreboard.switch()
        self.__play_innings(True)
        self.__print_results()

    def __play_innings(self, second_innings: 'bool'):
        for _ in range(self.__overs * 6):
            result = self.__engine.return_fake_result()
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

    def __print_results(self):
        scorecard1, scorecard2 = (self.__scoreboard.return_one_scorecard(),
                                  self.__scoreboard.return_two_scorecard())
        self.__print_scorecard_summary(scorecard1)
        self.__print_scorecard_summary(scorecard2)

        scorecard1.print_whole_scorecard()
        scorecard2.print_whole_scorecard()

    @staticmethod
    def __print_scorecard_summary(scorecard):
        print("Team 1: {}/{} {}.{} 4: {}, 6: {}".format(
            scorecard.return_batting(1),
            scorecard.wickets(),
            scorecard.return_batting(2) // 6,
            scorecard.return_batting(2) % 6,
            scorecard.return_batting(3),
            scorecard.return_batting(4)))


if __name__ == '__main__':
    game = Game(20)
    game.play()

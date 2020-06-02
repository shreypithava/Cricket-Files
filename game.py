from database import Database
from engine import Engine
from manager import Manager
from scoreboard import ScoreBoard
from scorecard import ScoreCard


class Game(object):

    def __init__(self, id1: 'int' = 1, id2: 'int' = 2):
        self.__database = Database()
        self.__manager1 = Manager(id1, self.__database.before_game(id1))
        self.__manager2 = Manager(id2, self.__database.before_game(id2))
        self.__overs = 20
        self.__engine = Engine()
        self.__scoreboard = ScoreBoard(self.__manager1.get_team(),
                                       self.__manager2.get_team())

    def play(self):
        self.__play_innings(False)
        self.__scoreboard.switch()
        self.__play_innings(True)
        self.__post_match()

    def __play_innings(self, second_innings: 'bool'):
        for _ in range(self.__overs * 6):
            result = self.__engine.return_result(10)  # TODO: start here
            self.__scoreboard.action(result)
            if self.__scoreboard.runs_chased() or \
                    self.__scoreboard.is_all_out(2) or \
                    (not second_innings and
                     self.__scoreboard.is_all_out(1)):
                break

    def __post_match(self):
        self.__print_results()

        result1, result2 = self.__get_result()
        self.__database.after_game(self.__manager1,
                                   self.__manager2,
                                   result1, result2, self.__scoreboard)

    def __get_result(self):
        if self.__scoreboard.return_scorecard(1).get_runs_scored() > \
                self.__scoreboard.return_scorecard(2).get_runs_scored():
            return 0, 1
        if self.__scoreboard.return_scorecard(2).get_runs_scored() > \
                self.__scoreboard.return_scorecard(1).get_runs_scored():
            return 1, 0
        return 2, 2

    def __print_results(self):
        scorecard1, scorecard2 = self.__scoreboard.return_scorecard(1), \
                                 self.__scoreboard.return_scorecard(2)

        self.__print_scorecard_summary(scorecard1)
        self.__print_scorecard_summary(scorecard2)

        scorecard1.print_whole_scorecard()
        scorecard2.print_whole_scorecard()

    @staticmethod
    def __print_scorecard_summary(scorecard: 'ScoreCard'):
        print("Team {}: {}/{} {}.{} 4: {}, 6: {}".format(
            scorecard.get_innings(),
            scorecard.return_batting(0),
            scorecard.wickets(),
            scorecard.return_batting(1) // 6,
            scorecard.return_batting(1) % 6,
            scorecard.return_batting(2),
            scorecard.return_batting(3)))

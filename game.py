from engine import FakeEngine
from manager import Manager
from scoreboard import ScoreBoard
from scorecard import ScoreCard


class Game(object):

    def __init__(self, id1: 'int' = 1, id2: 'int' = 2):
        self.__manager1 = Manager(id1)
        self.__manager2 = Manager(id2)
        self.__overs = 20
        self.__fake_engine = FakeEngine()
        self.__scoreboard = ScoreBoard(self.__manager1.get_team(),
                                       self.__manager2.get_team())

    def play(self):
        self.__play_innings(False)
        self.__scoreboard.switch()
        self.__play_innings(True)
        self.__post_match()

    def __post_match(self):
        self.__print_results()
        # TODO: pass ScoreBoard, (manager1 or manager2)
        #  to Manager to make changes to database
        self.__manager1.update_stats_in_database()
        self.__manager2.update_stats_in_database()

    def __play_innings(self, second_innings: 'bool'):
        for _ in range(self.__overs * 6):
            result = self.__fake_engine.return_result()
            self.__scoreboard.action(result)
            if (second_innings and
                (self.__scoreboard.return_scorecard(2).return_batting(0) >
                 self.__scoreboard.return_scorecard(1).return_batting(0) or
                 self.__scoreboard.return_scorecard(2).wickets() == 10)) or \
                    (not second_innings and
                     self.__scoreboard.return_scorecard(1).wickets() == 10):
                break

    def __print_results(self):
        scorecard1, scorecard2 = self.__scoreboard.return_scorecard(1), \
                                 self.__scoreboard.return_scorecard(2)

        if scorecard1.return_batting(0) > scorecard2.return_batting(0):
            self.__manager1.update_manager_database(0)
            self.__manager2.update_manager_database(1)
        elif scorecard1.return_batting(0) < scorecard2.return_batting(0):
            self.__manager1.update_manager_database(1)
            self.__manager2.update_manager_database(0)
        else:
            self.__manager1.update_manager_database(2)
            self.__manager2.update_manager_database(2)

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

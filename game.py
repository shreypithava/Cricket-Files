import sqlite3

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
        self.__update_match_in_database()
        self.__manager1.update_stats_in_database()
        self.__manager2.update_stats_in_database()

    def __update_match_in_database(self):

        scorecard1, scorecard2 = (self.__scoreboard.return_scorecard(1),
                                  self.__scoreboard.return_scorecard(2))
        stats_json = {"inning_1": {"bat": list(), "bowl": list(),
                                   "ball_by_ball":
                                       scorecard1.get_ball_by_ball()},
                      "inning_2": {"bat": list(), "bowl": list(),
                                   "ball_by_ball":
                                       scorecard2.get_ball_by_ball()}}

        for player in scorecard1.get_list_of_batsman():
            person = [player.get_id(), player.get_bat_stats()]
            stats_json['inning_1']['bat'].append(person)
        for player in scorecard1.get_list_of_bowlers():
            person = [player.get_id(), player.get_bowl_stats()]
            stats_json['inning_1']['bowl'].append(person)
        for player in scorecard2.get_list_of_batsman():
            person = [player.get_id(), player.get_bat_stats()]
            stats_json['inning_2']['bat'].append(person)
        for player in scorecard2.get_list_of_bowlers():
            person = [player.get_id(), player.get_bowl_stats()]
            stats_json['inning_1']['bowl'].append(person)

        query = 'INSERT INTO MATCH ({0}1, {0}2, stats) VALUES ({}, {}, {}})' \
            .format('ManagerID', self.__manager1.get_id(),
                    self.__manager2.get_id(), stats_json)
        db = sqlite3.connect('database.db')
        db.execute(query)
        # db.commit()
        db.close()

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

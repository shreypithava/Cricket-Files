import sqlite3

from database import Database
from engine import FakeEngine
from manager import Manager
from scoreboard import ScoreBoard
from scorecard import ScoreCard


class Game(object):

    def __init__(self, id1: 'int' = 1, id2: 'int' = 2):
        self.__database = Database()
        self.__manager1 = Manager(id1, self.__database.before_game(id1))
        self.__manager2 = Manager(id2, self.__database.before_game(id2))
        self.__overs = 20
        self.__engine = FakeEngine()
        self.__scoreboard = ScoreBoard(self.__manager1.get_team(),
                                       self.__manager2.get_team())

    def play(self):
        self.__play_innings(False)
        self.__scoreboard.switch()
        self.__play_innings(True)
        self.__post_match()

    def __play_innings(self, second_innings: 'bool'):
        for _ in range(self.__overs * 6):
            result = self.__engine.return_result()
            self.__scoreboard.action(result)
            if self.__scoreboard.runs_chased() or \
                    self.__scoreboard.is_all_out(2) or \
                    (not second_innings and
                     self.__scoreboard.is_all_out(1)):
                break

    def __post_match(self):
        self.__print_results()
        self.__update_in_database()

    def __update_in_database(self):
        scorecard1, scorecard2 = (self.__scoreboard.return_scorecard(1),
                                  self.__scoreboard.return_scorecard(2))

        stats_json = {"inning_1": {"bat": list(), "bowl": list()},
                      "inning_2": {"bat": list(), "bowl": list()}}

        for player in scorecard1.get_list_of_batsman():
            person = [player.get_id(), player.get_bat_stats()[:2]]
            stats_json['inning_1']['bat'].append(person)
        for player in scorecard1.get_list_of_bowlers():
            person = [player.get_id(), player.get_bowl_stats()]
            stats_json['inning_1']['bowl'].append(person)
        for player in scorecard2.get_list_of_batsman():
            person = [player.get_id(), player.get_bat_stats()[:2]]
            stats_json['inning_2']['bat'].append(person)
        for player in scorecard2.get_list_of_bowlers():
            person = [player.get_id(), player.get_bowl_stats()]
            stats_json['inning_2']['bowl'].append(person)

        db = sqlite3.connect('database.db')
        # PRAGMA foreign_keys = on;
        db.execute("INSERT INTO Match (ManagerID1, ManagerID2) VALUES (?, ?)",
                   (self.__manager1.get_id(),
                    self.__manager2.get_id()))

        match_id = db.execute("SELECT COUNT(*) FROM Match").fetchone()[0]

        db.execute("""UPDATE Match SET
        Inning_1 = (SELECT json_set(
        json(Inning_1), '$.bat', json(?), '$.bowl', json(?)) FROM Match),
        Inning_2 = (SELECT json_set(
        json(Inning_2), '$.bat', json(?), '$.bowl', json(?)) FROM Match)
        WHERE ID = ?""", (str(stats_json['inning_1']['bat']),
                          str(stats_json['inning_1']['bowl']),
                          str(stats_json['inning_2']['bat']),
                          str(stats_json['inning_2']['bowl']),
                          match_id))

        if scorecard1.get_runs_scored() > scorecard2.get_runs_scored():
            self.__manager1.update_manager_and_player_database(0, db)
            self.__manager2.update_manager_and_player_database(1, db)
        elif scorecard1.get_runs_scored() < scorecard2.get_runs_scored():
            self.__manager1.update_manager_and_player_database(1, db)
            self.__manager2.update_manager_and_player_database(0, db)
        else:
            self.__manager1.update_manager_and_player_database(2, db)
            self.__manager2.update_manager_and_player_database(2, db)

        # db.commit()
        db.close()

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

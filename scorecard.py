from random import choice

from player import Player
from team import Team


class ScoreCard(object):

    def __init__(self, team1: 'Team', team2: 'Team', innings: 'int'):
        self.__list_of_batting: 'list[Player]' = team1.get_players()
        self.__list_of_bowling: 'list[Player]' = team2.get_players()
        self.__extras = None  # future developments
        self.__innings = innings
        self.__zero_index_batsman = True
        self.__people_at_crease = [1, 2]
        self.__runs_scored = 0
        self.__total_wickets = 0
        self.__ball_by_ball = list()
        self.__bowlers_list = list(range(5, 11))
        self.__bowler_idx = choice(self.__bowlers_list)
        self.__set_batsman()

    def is_all_out(self) -> bool:
        return self.__total_wickets == 10

    def get_runs_scored(self) -> int:
        return self.__runs_scored

    def __set_batsman(self):
        self.__list_of_batting[self.__people_at_crease[0] - 1].came_to_bat()
        self.__list_of_batting[self.__people_at_crease[1] - 1].came_to_bat()

    def get_list_of_batsman(self):
        return self.__list_of_batting

    def get_list_of_bowlers(self):
        return self.__list_of_bowling

    def get_innings(self):
        return self.__innings

    def action(self, runs: 'int'):
        self.__ball_by_ball.append(runs)

        self.__list_of_batting[
            self.__people_at_crease[
                self.__return_idx()] - 1].update_bat_stats(runs)
        self.__list_of_bowling[self.__bowler_idx].update_bowl_stats(runs)

        if runs >= 0:
            self.__zero_index_batsman = runs % 2 == self.__return_idx()
            self.__runs_scored += runs
        else:
            self.__total_wickets += 1
            self.__people_at_crease[self.__return_idx()] = \
                max(self.__people_at_crease) + 1
            if max(self.__people_at_crease) != 12:
                self.__list_of_batting[
                    self.__people_at_crease[self.__return_idx()]
                    - 1].came_to_bat()
        self.__check_if_over()

    def __return_idx(self):
        return 0 if self.__zero_index_batsman else 1

    def __invert_return_idx(self):
        return 1 if self.__return_idx() == 0 else 0

    def get_ball_by_ball(self):
        return self.__ball_by_ball

    def __check_if_over(self):
        if self.__list_of_bowling[self.__bowler_idx].get_bowl_stats()[0] \
                % 6 == 0:
            self.__zero_index_batsman = not self.__zero_index_batsman
            temp = self.__bowler_idx
            # TODO: select bowler in future developments
            while temp == self.__bowler_idx or \
                    self.__list_of_bowling[self.__bowler_idx].get_bowl_stats(
                    )[0] == 24:
                self.__bowler_idx = choice(self.__bowlers_list)

    def wickets(self) -> 'int':
        total_wickets = 0
        for player in self.__list_of_bowling:
            total_wickets += player.get_bowl_stats()[3]
        return total_wickets

    def return_batting(self, idx: 'int') -> 'int':
        # runs: 0, balls: 1, fours: 2, sixes: 3
        total = 0
        for player in self.__list_of_batting:
            total += player.get_bat_stats()[idx]
        return total

    def print_whole_scorecard(self):
        print("-" * 5 + "Batting" + "-" * 5)
        for idx, batsman in enumerate(self.__list_of_batting):
            if self.wickets() + 2 == idx:
                break
            print('{}  {}({})'.format(batsman.get_name(),
                                      batsman.get_bat_stats()[0],
                                      batsman.get_bat_stats()[1]))
        print("-" * 5 + "Bowling" + "-" * 5)
        for bowler in self.__list_of_bowling:
            bowl_stats = bowler.get_bowl_stats()
            if self.__bowl_overs(bowl_stats[0]) != '0':
                print("{}  {}-{}-{}-{}".format(
                    bowler.get_name(), self.__bowl_overs(bowl_stats[0]),
                    bowl_stats[1], bowl_stats[2], bowl_stats[3]))
        print()

    @staticmethod
    def __bowl_overs(balls: 'int') -> 'str':
        if balls % 6 == 0:
            return '{}'.format(balls // 6)
        return '{}.{}'.format(balls // 6, balls % 6)

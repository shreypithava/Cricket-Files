from random import randint

from team import Team


class ScoreCard(object):

    def __init__(self, team1: 'Team', team2: 'Team'):
        self.__list_of_batting: \
            'list[list[str, int, int, int, int]]' \
            = list()  # runs, balls, fours, six
        self.__list_of_bowling: \
            'list[list[str, int, int, int, int]]' \
            = list()  # overs, maidens, runs, wickets
        self.__extras = None  # future developments
        self.__zero_index_batsman = True
        self.__people_at_crease = [1, 2]
        self.__bowler_idx = 0
        self.__fill_scorecard(team1, team2)

    def __fill_scorecard(self, team1: 'Team', team2: 'Team'):
        for idx in range(11):
            temp_bat = team1.get_players()[idx].get_name()
            self.__list_of_batting.append([temp_bat, 0, 0, 0, 0])
            temp_bowl = team2.get_players()[idx].get_name()
            self.__list_of_bowling.append([temp_bowl, 0, 0, 0, 0])

    def action(self, runs: 'int'):
        if runs >= 0:
            self.__add_runs(runs)
        else:
            self.__got_wicket()
        self.__list_of_bowling[self.__bowler_idx][1] += 1
        self.__check_if_over()

    @staticmethod
    def __boundaries_idx(result: 'int'):
        return 3 if result == 4 else 4

    def __add_runs(self, runs: 'int'):
        self.__list_of_batting[
            self.__people_at_crease[self.__return_idx()] - 1][1] += runs
        self.__list_of_batting[
            self.__people_at_crease[self.__return_idx()] - 1][2] += 1
        if runs >= 4:
            self.__list_of_batting[
                self.__people_at_crease[self.__return_idx()] - 1][
                self.__boundaries_idx(runs)] += 1
        self.__zero_index_batsman = runs % 2 == self.__return_idx()
        self.__list_of_bowling[self.__bowler_idx][3] += runs

    def __return_idx(self):
        return 0 if self.__zero_index_batsman else 1

    def __invert_return_idx(self):
        return 1 if self.__return_idx() == 0 else 0

    def __got_wicket(self):
        self.__list_of_batting[
            self.__people_at_crease[self.__return_idx()] - 1][2] += 1
        self.__list_of_bowling[self.__bowler_idx][4] += 1
        while True:
            self.__people_at_crease[self.__return_idx()] += 1
            if self.__people_at_crease[
                self.__return_idx()] > \
                    self.__people_at_crease[self.__invert_return_idx()]:
                break

    def __check_if_over(self):
        if self.__list_of_bowling[self.__bowler_idx][1] % 6 == 0:
            self.__zero_index_batsman = not self.__zero_index_batsman
            temp = self.__bowler_idx
            # TODO: select bowler in future developments
            while True:
                self.__bowler_idx = randint(0, 10)
                if temp != self.__bowler_idx and \
                        self.__list_of_bowling[self.__bowler_idx][1] != 24:
                    break

    def wickets(self):
        total_wickets = 0
        for _, _, _, _, wickets in self.__list_of_bowling:
            total_wickets += wickets
        return total_wickets

    def return_batting(self, idx: 'int'):
        # runs: 1, balls: 2, fours: 3, sixes: 4
        total = 0
        for info in self.__list_of_batting:
            total += info[idx]
        return total

    def print_whole_scorecard(self):
        print("-" * 5 + "Batting" + "-" * 5)
        for batsman in self.__list_of_batting:
            print('{}  {}({})'.format(batsman[0], batsman[1], batsman[2]))
        print("-" * 5 + "Bowling" + "-" * 5)
        for bowler in self.__list_of_bowling:
            print("{}  {}-{}-{}-{}".format(
                bowler[0], bowler[1], bowler[2], bowler[3], bowler[4]))
        print()

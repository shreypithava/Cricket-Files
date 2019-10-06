from random import randint

from team import Team


class ScoreCard(object):

    def __init__(self, team1: 'Team', team2: 'Team'):
        self.__list_of_batting: 'list[list[str, int, int]]' = list()
        self.__list_of_bowling: 'list[list[str, int, int, int, int]]' = list()  # overs, maidens, runs, wickets
        self.__extras = None  # future developments
        self.__zero_index_batsman: 'bool' = True
        self.__people_at_crease: 'list[int]' = [1, 2]
        self.__bowler_idx = 0
        self.__fill_scorecard(team1, team2)

    def __fill_scorecard(self, team1: 'Team', team2: 'Team'):
        for idx in range(11):
            temp_bat = team1.get_players()[idx].get_personal().get_name()
            self.__list_of_batting.append([temp_bat, 0, 0])
            temp_bowl = team2.get_players()[idx].get_personal().get_name()
            self.__list_of_bowling.append([temp_bowl, 0, 0, 0, 0])

    def action(self, runs: 'int'):
        if runs >= 0:
            self.__add_runs(runs)
        else:
            self.__got_wicket()
        self.__list_of_bowling[self.__bowler_idx][1] += 1
        self.__check_if_over()

    # TODO: more DRY coding
    def __add_runs(self, runs: 'int'):
        if self.__zero_index_batsman:
            self.__list_of_batting[self.__people_at_crease[0] - 1][1] += runs
            self.__list_of_batting[self.__people_at_crease[0] - 1][2] += 1
            self.__zero_index_batsman = runs % 2 == 0
        else:
            self.__list_of_batting[self.__people_at_crease[1] - 1][1] += runs
            self.__list_of_batting[self.__people_at_crease[1] - 1][2] += 1
            self.__zero_index_batsman = runs % 2 == 1
        self.__list_of_bowling[self.__bowler_idx][3] += runs

    def __got_wicket(self):
        if self.__zero_index_batsman:
            self.__list_of_batting[self.__people_at_crease[0] - 1][2] += 1
            while True:
                self.__people_at_crease[0] += 1
                if self.__people_at_crease[0] > self.__people_at_crease[1]:
                    break
        else:
            self.__list_of_batting[self.__people_at_crease[1] - 1][2] += 1
            while True:
                self.__people_at_crease[1] += 1
                if self.__people_at_crease[1] > self.__people_at_crease[0]:
                    break
        self.__list_of_bowling[self.__bowler_idx][4] += 1

    def __check_if_over(self):
        if self.__list_of_bowling[self.__bowler_idx][1] % 6 == 0:
            self.__zero_index_batsman = not self.__zero_index_batsman
            temp = self.__bowler_idx
            while temp == self.__bowler_idx:
                self.__bowler_idx = randint(0, 10)

    def return_total_runs(self):
        total_runs = 0
        for _, runs, _ in self.__list_of_batting:
            total_runs += runs
        return total_runs

    def wickets_related(self, check_all_out: 'bool'):
        total_wickets = 0
        for _, _, _, _, wickets in self.__list_of_bowling:
            total_wickets += wickets
        return total_wickets == 10 if check_all_out else total_wickets

    def return_balls(self):
        total_balls = 0
        for _, _, balls in self.__list_of_batting:
            total_balls += balls
        return total_balls

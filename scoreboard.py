from scorecard import ScoreCard
from team import Team


# TODO: think about engine having ScoreBoard or Team
class ScoreBoard(object):

    def __init__(self, team1: 'Team', team2: 'Team'):
        # self.__one_scorecard = [0, 0, 0]
        # self.__two_scorecard = [0, 0, 0]
        self.__temp1_scorecard = ScoreCard(team1, team2)
        self.__temp2_scorecard = ScoreCard(team2, team1)
        # self.__batting_team = self.__one_scorecard
        self.__batting_team = self.__temp1_scorecard

    def switch(self):
        self.__batting_team = self.__temp2_scorecard

    # def add(self, runs):
    #     self.__batting_team[0] += runs
    #     self.__add_ball()
    def add(self, runs):
        self.__batting_team.add_runs(runs)

    # def wicket(self):
    #     self.__batting_team[1] += 1
    #     self.__add_ball()
    def wicket(self):
        self.__batting_team.wicket()

    # def __add_ball(self):
    #     self.__batting_team[2] += 1

    def return_one_scorecard(self):
        return self.__temp1_scorecard

    def return_two_scorecard(self):
        return self.__temp2_scorecard

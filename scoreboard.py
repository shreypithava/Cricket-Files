from scorecard import ScoreCard
from team import Team


# TODO: think about engine having ScoreBoard or Team
class ScoreBoard(object):

    def __init__(self, team1: 'Team', team2: 'Team'):
        self.__one_scorecard = ScoreCard(team1, team2)
        self.__two_scorecard = ScoreCard(team2, team1)
        self.__batting_team = self.__one_scorecard

    def switch(self):
        self.__batting_team = self.__two_scorecard

    def add(self, runs):
        self.__batting_team.add_runs(runs)

    def got_wicket(self):
        self.__batting_team.got_wicket()

    def return_one_scorecard(self):
        return self.__one_scorecard

    def return_two_scorecard(self):
        return self.__two_scorecard

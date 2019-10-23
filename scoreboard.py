from scorecard import ScoreCard
from team import Team


class ScoreBoard(object):

    def __init__(self, team1: 'Team', team2: 'Team'):
        self.__one_scorecard = ScoreCard(team1, team2, 1)
        self.__two_scorecard = ScoreCard(team2, team1, 2)
        self.__batting_team = self.__one_scorecard

    def switch(self):
        self.__batting_team = self.__two_scorecard

    def action(self, runs: 'int'):
        self.__batting_team.action(runs)

    def return_scorecard(self, innings: 'int') -> 'ScoreCard':
        if innings == 1:
            return self.__one_scorecard
        return self.__two_scorecard

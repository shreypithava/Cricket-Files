from team import Team


class ScoreBoard(object):  # think about engine having ScoreBoard or Team
    # TODO: think about team1 and team2 usage
    def __init__(self, team1: 'Team' = None, team2: 'Team' = None):
        self.__one_scorecard = [0, 0, 0]
        self.__two_scorecard = [0, 0, 0]
        self.__batting_team = self.__one_scorecard

    def switch(self):
        self.__batting_team = self.__two_scorecard

    def add(self, runs):
        self.__batting_team[0] += runs
        self.__add_ball()

    def wicket(self):
        self.__batting_team[1] += 1
        self.__add_ball()

    def __add_ball(self):
        self.__batting_team[2] += 1

    def return_one_scorecard(self):
        return self.__one_scorecard

    def return_two_scorecard(self):
        return self.__two_scorecard

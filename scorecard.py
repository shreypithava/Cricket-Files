from team import Team


class ScoreCard(object):

    def __init__(self, team1: 'Team', team2: 'Team'):
        self.__list_of_batting: 'list[list[str, int, int]]' = [["", 0, 0]] * 11
        self.__list_of_bowling: \
            'list[list[str, int, int, int, int]]' = [["", 0, 0, 0, 0]] * 11  # overs, maidens, runs, wickets
        self.__extras = None  # future developments
        self.__fill_scorecard(team1, team2)

    def __fill_scorecard(self, team1, team2):
        for idx0 in range(11):
            self.__list_of_batting[idx0][0] = team1.get_players()[idx0].get_personal().get_name()
        for idx1 in range(11):
            self.__list_of_bowling[idx1][0] = team2.get_players()[idx1].get_personal().get_name()

    def add_runs(self, runs):
        print(runs)
        # TODO: add code here
        self.__add_ball()
        pass

    def wicket(self):
        # TODO: add code here
        self.__add_ball()
        pass

    def __add_ball(self):
        # TODO: add code here
        pass

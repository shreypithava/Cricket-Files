from team import Team


class Engine(object):
    def __init__(self):
        self.__blue_team = Team()
        self.__red_team = Team()

    def get_team(self, blue: 'bool'):
        return self.__blue_team if blue else self.__red_team


if __name__ == '__main__':
    engine = Engine()

    for player in engine.get_team(True).get_players() + engine.get_team(False).get_players():
        print(player.get_personal().get_name())

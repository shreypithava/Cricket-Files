import random
from player import Player, Personal


class Engine(object):
    def __init__(self):
        self.blue_team = list()
        self.red_team = list()

    def __get_players(self):  # complete this function
        pass


if __name__ == '__main__':
    engine = Engine()
    for _ in range(22):
        engine.blue_team.append(Player(personal=Personal(name=str(random.randint(10000, 100000)))))
        engine.red_team.append(Player(personal=Personal(name=str(random.randint(10000, 100000)))))

    for player in engine.red_team + engine.blue_team:
        print(player.get_personal().get_name())

from random import choices
from string import ascii_lowercase, digits


class Fielding(object):
    def __init__(self, agility: 'int' = 1, catching: 'int' = 1):
        self.__agility = agility
        self.__catching = catching

    def get_catching(self):
        return self.__catching

    def get_agility(self):
        return self.__agility


class Batting(object):
    def __init__(self, hand: 'str' = "R", ability: 'list[int]' = None):
        self.__hand = hand
        self.__ability = [1, 1] if ability is None else ability
        # [4, 3] where 4 for pace and 3 for spin
        self.__stats = [0, 0, 0, 0]  # runs, balls, fours, six

    def get_hand(self):
        return self.__hand

    def get_ability(self):
        return self.__ability

    def get_stats(self):
        return self.__stats

    def update_stats(self, runs: 'int'):
        if runs >= 0:
            self.__stats[0] += runs
            if runs == 4:
                self.__stats[2] += 1
            elif runs == 6:
                self.__stats[3] += 1
        self.__stats[1] += 1


class Bowling(object):
    def __init__(self, hand: 'str' = "R",
                 bowl_type: 'str' = "Pace",
                 ability: 'list[int]' = None):
        self.__ability = [1, 2] if ability is None else ability
        self.__hand = hand
        self.__bowl_type = bowl_type
        self.__stats = [0, 0, 0, 0]  # overs, maidens, runs, wickets

    def get_ability(self):
        return self.__ability  # [1, 2] for short ball and full ball

    def get_hand(self):
        return self.__hand

    def get_bowl_type(self):
        return self.__bowl_type

    def get_stats(self):
        return self.__stats

    def update_stats(self, result: 'int'):
        if result == -1:
            self.__stats[3] += 1
        else:
            self.__stats[2] += result
        self.__stats[0] += 1


class Personal(object):
    def __init__(self, xp: 'int' = 0, age: 'int' = 18, fitness: 'int' = 25):
        self.__name = "".join(choices(ascii_lowercase + digits, k=7))
        self.__xp = xp
        self.__age = age
        self.__fitness = fitness

    def get_name(self):
        return self.__name

    def get_xp(self):
        return self.__xp

    def get_age(self):
        return self.__age

    def get_fitness(self):
        return self.__fitness

    # TODO: think about career statistics


class Player(object):
    def __init__(self, personal=None,
                 batting=None,
                 bowling=None,
                 fielding=None):
        self.__id = None  # future development
        self.__personal = Personal() if personal is None else personal
        self.__batting = Batting() if batting is None else batting
        self.__bowling = Bowling() if bowling is None else bowling
        self.__fielding = Fielding() if fielding is None else fielding

    def get_personal(self):
        return self.__personal

    def get_name(self):
        return self.__personal.get_name()

    def get_batting(self):
        return self.__batting

    def get_bowling(self):
        return self.__bowling

    def get_fielding(self):
        return self.__fielding

    def update_bat_stats(self, runs: 'int'):
        self.__batting.update_stats(runs)

    def update_bowl_stats(self, runs: 'int'):
        self.__bowling.update_stats(runs)

    def get_bat_stats(self):
        return self.__batting.get_stats()

    def get_bowl_stats(self):
        return self.__bowling.get_stats()

from typing import List


class Fielding(object):
    def __init__(self, agility: 'int' = 1, catching: 'int' = 1):
        self.__agility = agility
        self.__catching = catching

    def get_catching(self):
        return self.__catching

    def get_agility(self):
        return self.__agility


class Batting(object):
    def __init__(self, hand: 'str' = "R", ability: 'List[int]' = None):
        self.__hand = hand
        if ability is None:
            self.__ability = [1, 1]
        else:
            self.__ability = ability  # [4, 3] where 4 for pace and 3 for spin

    def get_hand(self):
        return self.__hand

    def get_ability(self):
        return self.__ability


class Bowling(object):
    def __init__(self, hand: 'str' = "R", bowl_type: 'str' = "Pace", ability: 'List[int]' = None):
        if ability is None:
            self.__ability = [1, 2]
        else:
            self.__ability = ability
        self.__hand = hand
        self.__bowl_type = bowl_type

    def get_ability(self):
        return self.__ability

    def get_hand(self):
        return self.__hand

    def get_bowl_type(self):
        return self.__bowl_type


class Personal(object):
    def __init__(self, name: 'str' = "", xp: 'int' = 0, age: 'int' = 18, fitness: 'int' = 25):
        self.__name = name
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


class Player(object):
    def __init__(self, personal=Personal(), batting=Batting(), bowling=Bowling(), fielding=Fielding()):
        self.__personal = personal
        self.__batting = batting
        self.__bowling = bowling
        self.__fielding = fielding

    def get_personal(self):
        return self.__personal

    def get_batting(self):
        return self.__batting

    def get_bowling(self):
        return self.__bowling

    def get_fielding(self):
        return self.__fielding

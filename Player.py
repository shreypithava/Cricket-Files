from typing import List


class Fielding:
    def __init__(self, agility: 'int', catching: 'int'):
        self.__agility = agility
        self.__catching = catching

    def get_catching(self):
        return self.__catching

    def get_agility(self):
        return self.__agility


class Batting:
    def __init__(self, hand: 'str', ability: 'List[int]'):
        self.__hand = hand
        self.__ability = ability

    def get_hand(self):
        return self.__hand

    def get_ability(self):
        return self.__ability


class Bowling:
    def __init__(self, hand: 'str', bowl_type: 'str', ability: 'List[int]'):
        self.__hand = hand
        self.__bowl_type = bowl_type
        self.__ability = ability

    def get_ability(self):
        return self.__ability

    def get_hand(self):
        return self.__hand

    def get_bowl_type(self):
        return self.__bowl_type


class Personal:
    def __init__(self, name: 'str', xp: 'int', age: 'int', fitness: 'int' = 25):
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


class Player:
    def __init__(self, personal: 'Personal', batting: 'Batting', bowling: 'Bowling', fielding: 'Fielding'):
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


if __name__ == '__main__':
    player1 = Player(Personal("Shrey Pithava", 5, 24), Batting("R", [7, 8]), Bowling("R", "F", [7, 6, 5, 3]),
                     Fielding(1, 2))
    print(player1.get_batting().get_hand())

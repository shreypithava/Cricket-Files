from file_of_enums import BatStats as baS, BowlStats as boS
import json


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
        self.__stats = [0, 0, 0, 0, False, True]
        # runs, balls, fours, six, played, not_out

    def get_hand(self):
        return self.__hand

    def get_ability(self):
        return self.__ability

    def get_stats(self):
        return self.__stats

    def came_out(self):
        self.__stats[baS.played.value] = True

    def update_stats(self, runs: 'int'):
        if runs >= 0:
            self.__stats[baS.runs.value] += runs
            if runs == 4:
                self.__stats[baS.fours.value] += 1
            elif runs == 6:
                self.__stats[baS.six.value] += 1
        else:
            self.__stats[baS.not_out.value] = False
        self.__stats[baS.balls.value] += 1


class Bowling(object):
    def __init__(self, hand: 'str' = "R",
                 ability: 'list[int]' = None,
                 bowl_type: 'str' = "Pace"):
        self.__ability = [1, 2] if ability is None else ability
        self.__hand = hand
        self.__bowl_type = bowl_type
        self.__stats = [0, 0, 0, 0]  # balls, maidens, runs, wickets

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
            self.__stats[boS.wickets.value] += 1
        else:
            self.__stats[boS.runs.value] += result
        self.__stats[boS.balls.value] += 1


class Personal(object):
    def __init__(self, name: 'str', xp: 'int' = 0,
                 age=18, fitness: 'int' = 25):
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
    def __init__(self, record: 'tuple'):
        self.__id = record[0]
        self.__personal = Personal(record[1], json.loads(record[2])['matches'],
                                   record[3], record[11])
        self.__batting = Batting(json.loads(record[8])['bat_hand'],
                                 json.loads(record[9])['bat'])
        self.__bowling = Bowling(json.loads(record[8])['bowl_hand'],
                                 json.loads(record[9])['bowl'])
        self.__fielding = Fielding(json.loads(record[10])['agility'],
                                   json.loads(record[10])['catching'])

    def get_id(self):
        return self.__id

    def get_personal(self):
        return self.__personal

    def get_name(self):
        return self.__personal.get_name()

    def get_batting(self):
        return self.__batting

    def came_to_bat(self):
        self.__batting.came_out()

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

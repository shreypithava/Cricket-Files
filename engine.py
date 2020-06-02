from random import choice, shuffle


def return_ratings(skill):
    if skill == 1:
        return 34, 24, 4, 1, 8, 23, 6
    if skill == 2:
        return 34, 25, 4, 1, 9, 20, 7
    if skill == 3:
        return 34, 23, 7, 1, 9, 19, 7
    if skill == 4:
        return 31, 23, 11, 2, 10, 16, 7
    if skill == 5:
        return 29, 23, 14, 2, 11, 13, 8
    if skill == 6:
        return 28, 23, 15, 3, 13, 10, 8
    if skill == 7:
        return 27, 23, 15, 3, 15, 8, 9
    if skill == 8:
        return 25, 23, 17, 3, 16, 7, 9
    if skill == 9:
        return 21, 24, 19, 3, 17, 6, 10
    if skill == 10:
        return 17, 25, 20, 4, 18, 6, 10
    return 15, 26, 21, 3, 18, 6, 11


class Engine(object):

    def __init__(self):
        self._probabilities_list = []
        self.initialize_engine()

    # TODO: complete this function in future
    def return_result(self, skill: int):
        shuffle(self._probabilities_list[skill - 1])
        return choice(self._probabilities_list[skill - 1])

    def initialize_engine(self):
        for i in range(11):
            self._probabilities_list.append([])
            prob_list = return_ratings(i + 1)
            for idx, quantity in enumerate(prob_list):
                for _ in range(quantity):
                    self._probabilities_list[i].append(idx if idx != 5 else -1)

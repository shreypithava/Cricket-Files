from random import choice, shuffle


def return_fake_probabilities():
    the_list = list()
    for number in range(100):
        if number < 15:
            the_list.append(0)
        elif number < 30:
            the_list.append(1)
        elif number < 45:
            the_list.append(2)
        elif number < 60:
            the_list.append(3)
        elif number < 75:
            the_list.append(4)
        elif number < 90:
            the_list.append(6)
        else:
            the_list.append(-1)
    return the_list


class Engine(object):
    def __init__(self):
        self.__probabilities_list = return_fake_probabilities()

    # TODO: complete this function in future
    def return_fake_result(self):
        shuffle(self.__probabilities_list)
        return choice(self.__probabilities_list)

    def return_result(self):
        pass

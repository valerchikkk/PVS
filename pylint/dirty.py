import numpy as np
import random
import sqlite3

default_accuracy = 3


def sumTwoValues(first, second):
    return first + second


def div(x, y, ACCURACY, module):
    return round(x/y,  ACCURACY)



def get_rand():
    return random.randint(1, 10)

def rand_array():
    a = [get_rand(), get_rand(), get_rand()]
    return np.array(a)

def main():
    pass


main()

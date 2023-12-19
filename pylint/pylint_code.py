"""
Модуль Pylint_Code
"""

import random
import numpy as np

DEFAULT_ACCURACY = 3


def sum_two_values(first, second):
    """
    Функция, выполняющая сумму двух значений.
    """
    return first + second


def divide(x, y, accuracy):
    """
    Функция, выполняющая деление x на y с указанной точностью.
    """
    return round(x / y, accuracy)


def get_rand():
    """
    Функция, возвращающая случайное целое число от 1 до 10.
    """
    return random.randint(1, 10)


def rand_array():
    """
    Функция, возвращающая массив из трех случайных чисел.
    """
    a = [get_rand(), get_rand(), get_rand()]
    return np.array(a)


def main():
    """
    Главная функция программы.
    """
    print("------")

if __name__ == "__main__":
    main()

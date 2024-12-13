import os
import threading
import random
import math
import time

random.seed()
N = 100000


def calc_Pi_without_treads():
    count = 0
    for _ in range(N):
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1
        if x * x + y * y <= 1:
            count += 1
        print(f'П ~ {(4 * count / N)}')


if __name__ == '__main__':
    calc_Pi_without_treads()

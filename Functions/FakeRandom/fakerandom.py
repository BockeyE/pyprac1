from random import random


def fakeran():
    origin_P = 0.2
    currentP = 0.2
    no_P_times = 0

    ret = random(1, 2)

    if ret != 1:
        no_P_times = no_P_times + 1
        currentP = origin_P + currentP

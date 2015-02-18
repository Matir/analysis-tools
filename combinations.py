#!/usr/bin/env python

from string import uppercase, lowercase, maketrans
import math, sys


class combinations():

    def combs(self, total, choice):
        return (math.factorial(total)/(math.factorial(choice)*math.factorial(total-choice)))
       

if __name__ == '__main__':
    try:
        total = sys.argv[1]
        choice = sys.argv[2]
        total = int(total, 0)
        choice = int(choice, 0)
        ops = combinations()
        result = ops.combs(total, choice)
        print result
    except IndexError:
        print('Usage: combinations.py <int of total> <int to choice>')

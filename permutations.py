#!/usr/bin/env python

from string import uppercase, lowercase, maketrans
import math, sys


class permutations():

    def perms(self, total, choice):
        result = 1
        for x in range(0, choice):
            result *= total-x
        return result
       

if __name__ == '__main__':
    try:
        total = sys.argv[1]
        choice = sys.argv[2]
        total = int(total, 0)
        choice = int(choice, 0)
        ops = permutations()
        result = ops.perms(total, choice)
        print result
    except IndexError:
        print('Usage: permutations.py <int of total> <int to choice>')

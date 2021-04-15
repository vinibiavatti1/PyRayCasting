"""
Calculations
"""
import math


def dg_to_rad(dg):
    return dg * math.pi / 180


def pythagoras(x1, y1, x2, y2):
    cat1 = (x1 - x2)
    cat2 = (y1 - y2)
    return math.sqrt((cat1 ** 2) + (cat2 ** 2))

# coding=utf-8

"""
sympy解方程

Version: 0.0.1
Author : yichu.cheng
"""

from sympy import *
x, y = symbols('x y')
print(solve([2*x-y-3, 3*x+y-7], [x, y]))

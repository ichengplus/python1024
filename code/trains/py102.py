# coding=utf-8

"""
输入三条边长
如果构成三角形，则输出周长L和面积S
否则，输出"no"

Version: 0.0.1
Author : yichu.cheng
"""

import math

a = float(input('a = '))
b = float(input('b = '))
c = float(input('c = '))

if a + b > c and a + c > b and b + c > a:
    L = a + b + c
    p = L / 2
    # math.sqrt是专用开方函数
    s1 = math.sqrt(p*(p-a)*(p-b)*(p-c))
    # ** 是幂运算，x**2即x平方，x**0.5即为x开方
    s2 = (p*(p-a)*(p-b)*(p-c)) ** 0.5
    print('周长: %.2f' % L)
    print('面积1: %.2f' % s1)
    print('面积2: %.2f' % s2)
else:
    print('no')

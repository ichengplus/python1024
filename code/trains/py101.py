# coding=utf-8

"""
输入圆半径
输出圆周长和面积

Version: 0.0.1
Author : yichu.cheng
"""

import math

r = float(input('请输入圆半径：'))
c = 2 * math.pi * r
s = math.pi * r**2
print('周长：%.2f' % c)
print('面积：%.2f' % s)

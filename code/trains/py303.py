# coding=utf-8

"""
随机生成一个10个整数的列表
输出其中最大和次大的两个整数

Version: 0.0.1
Author : yichu.cheng
"""

import random

# 用列表生成器获得一个随机整数列表
s = [random.randint(1, 1000) for i in range(10)]
# 初始化最大值x1，次大值x2
x1, x2 = 0, 0
for i in s:
    if i > x1:
        x2 = x1
        x1 = i
    elif i > x2:
        x2 = i

print("最大值: {}， 次大值: {}".format(x1, x2))

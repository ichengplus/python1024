# coding=utf-8

"""
随机生成一个10个整数的列表
输出其中最大和次大的两个整数

Version: 0.0.1
Author : yichu.cheng
"""

import random

# 用列表生成器获得一个随机整数列表
s = [random.randint(-100, 100) for i in range(100)]
d = {}
for i in s:
    # 通过get方法提供默认值0，完成key值初始化
    d[i] = d.get(i, 0) + 1
print(d)

# from collections import Counter
# result = Counter(s)
# print(dict(result))
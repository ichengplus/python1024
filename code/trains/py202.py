# coding=utf-8

"""
输入成绩
输出对应等级

Version: 0.0.1
Author : yichu.cheng
"""

s = float(input('输入成绩: '))
if s >= 90:
    g = 'A'
elif s >= 80:
    g = 'B'
elif s >= 70:
    g = 'C'
elif s >= 60:
    g = 'D'
else:
    g = 'E'
print('对应等级:', g)

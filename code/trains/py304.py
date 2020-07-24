# coding=utf-8

"""
输入5个不同点坐标
输出直线距离最近的两个点

Version: 0.0.1
Author : yichu.cheng
"""

import math

# input收到一个字符串后，通过split分割出一个列表
# 通过map，把列表中每个元素都转为float类型，再转为一个元组
# 通过列表生成器，持续获取5组输入后，生成5个tuple的列表
points = [tuple(map(float, input('输入一组数字:').split(','))) for i in range(5)]

# 初始化最短距离为无穷大
dis_min = float('inf')

for (x1, y1) in points:
    for(x2, y2) in points:
        if x1 == x2 and y1 == y2:
            # 排除掉同一个点自己相比
            continue
        dis = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        if dis < dis_min:
            x1_min, y1_min = x1, y1
            x2_min, y2_min = x2, y2
            dis_min = dis
print("点({0}, {1})与点({2}, {3})之间距离最近，为{4}".format(
    x1_min, y1_min, x2_min, y2_min, dis_min))

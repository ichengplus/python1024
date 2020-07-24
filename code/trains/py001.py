# coding=utf-8
"""
Python语言基础，公众号：只差一个程序员了
Version: 0.0.1
Author : yichu.cheng
"""
import math


class SingleNumberShape(object):
    """ 某一类图形，可以用一个数字计算其面积 """
    name = 'I"m a SingleNumberShape.'

    def __init__(self, length=0):
        """初始化实例"""
        self.length = length

    def area(self):
        """返回面积"""
        return self.length  # 对于基础类，直接返回长度


class Circle(SingleNumberShape):
    """ 圆形 """
    name = 'I"m a Circle.'

    def area(self):
        return math.pi * (self.length ** 2)  # 计算圆形面积


class Square(SingleNumberShape):
    """ 正方形 """
    name = 'I"m a Square.'

    def area(self):
        return self.length ** 2  # 计算正方形面积


def main_proc(n):
    """ 主处理函数 """
    shapes = []
    for i in range(10):
        if i % 2 == 0:  # 偶数生成圆形
            shapes.append(Circle(n+i))
        else:  # 奇数生成正方形
            shapes.append(Square(n+i))
    for s in shapes:
        print("形状面积: {:.2f}, 形状类型: {}".format(s.area(), s.name))


if __name__ == '__main__':
    n = float(input('请输入一个正数：'))
    main_proc(n)

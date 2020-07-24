# coding=utf-8

"""
随机生成整数、字符串、列表作为函数参数输入
输出参数类型和长度（如有）

Version: 0.0.1
Author : yichu.cheng
"""

import random
import string
from collections import Iterable


def proc(*params):
    """
    主过程函数

    :param params: 参数元组
    """
    for p in params:
        t = type(p)
        print("参数类型: {}".format(t))
        # 如果可迭代，就可以计算长度
        # if t in [str, list, set, dict]:
        if isinstance(p, Iterable):
            print('参数长度: {}'.format(len(p)))


if __name__ == '__main__':
    n = random.randint(0, 100)
    # 随机生成一个长度为n的字符串
    s = ''.join(random.choice(string.ascii_letters) for _ in range(n))
    # 从字符串中随机取个字符作为分隔符，划分出一个列表
    lst = s.split(random.choice(string.ascii_letters))
    proc(n, s, lst)

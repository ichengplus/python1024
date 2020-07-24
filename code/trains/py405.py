# coding=utf-8

"""
输入正整数
输出分解质因数

Version: 0.0.1
Author : yichu.cheng
"""

import math


def factor_r(n):
    """
    分解质因数，递归解法

    :param n: 正整数
    :return 质因数列表
    """
    if n == 1:
        return []
    else:
        for i in range(2, n + 1):
            # divmod(a,b) = (a // b, a % b)
            m, d = divmod(n, i)
            if d == 0:
                return [i] + factor(m)


def factor(n):
    """
    分解质因数，非递归解法

    :param n: 正整数
    :return 质因数列表
    """
    result = []
    while n > 1:
        for i in range(2, n + 1):
            if n % i == 0:
                n //= i
                result.append(i)
                break
    return result


def proc(n):
    """
    打印n的分解质因数

    :param n:正整数
    """
    if n < 2:
        print('无质因数')
        return
    lst = factor(n)
    s = '*'.join(map(str, lst))
    print('{} = {}'.format(n, s))


if __name__ == '__main__':
    n = int(input('输入正整数:'))
    proc(n)

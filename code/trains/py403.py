# coding=utf-8

"""
输入正整数n
输出[2,n]间所有完美数

Version: 0.0.1
Author : yichu.cheng
"""


def is_perfect(x):
    """
    判断x是否为完美数

    :param x: 正整数
    :return: 如果x是完美数返回True，否则返回False
    """
    factor_sum = 0
    for i in range(1, x//2+1):
        # 超过一半大小后，无真因子
        if x % i == 0:
            factor_sum += i
    return factor_sum == x


def is_perfect_p(x):
    """
    判断x是否为完美数，根据欧几里得定理，准备质数表

    :param x: 正整数
    :return: 如果x是完美数返回True，否则返回False
    """
    # 还有一些质数如11, 23等因为2^p-1不是质数，手工排除
    primes = [2, 3, 5, 7, 13, 17, 19, 31]
    for p in primes:
        if x == (2**(p-1)) * (2**p - 1):
            return True
    return False


def proc(n):
    """
    从[2,n]中找出所有完美数

    :param n: 正整数上限
    """
    for i in range(2, n+1):
        if is_perfect(i):
            print("{} 是完美数".format(i))


if __name__ == '__main__':
    n = int(input("输入整数上限:"))
    proc(n)
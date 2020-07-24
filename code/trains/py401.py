# coding=utf-8

"""
输入2个正整数
输出最大公约数GCD和最小公倍数LCM

Version: 0.0.1
Author : yichu.cheng
"""


def gcd(x, y):
    """
    求x和y的最大公约数

    :param x: 正整数
    :param y: 正整数
    :returns: x和y的最大公约数
    """
    # 确保x不比y大
    (x, y) = (y, x) if x > y else (x, y)
    for i in range(x, 0, -1):
        if x % i == 0 and y % i == 0:
            return i
    # 当i为1时一定会返回1


def gcd_r(x, y):
    """
    求x和y的最大公约数，递归实现方式
    欧几里得的辗转相除法：gcd(x,y)=gcd(y,x%y)

    :param x: 正整数
    :param y: 正整数
    :returns: x和y的最大公约数
    """
    return x if y == 0 else gcd_r(y, x % y)


def lcm(x, y):
    """
    求x和y的最小公倍数

    :param x: 正整数
    :param y: 正整数
    :returns: x和y的最小公倍数
    """
    return x // gcd(x, y) * y


# 当本python文件被执行时，__name__变量值为"__main__"
if __name__ == '__main__':
    x = int(input('输入x:'))
    y = int(input('输入y:'))
    r1 = gcd(x, y)
    # r1 = gcd_r(x, y)
    r2 = lcm(x, y)
    print("{}和{}的最大公约数: {}, 最小公倍数: {}".format(x, y, r1, r2))

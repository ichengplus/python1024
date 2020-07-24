# coding=utf-8

"""
输入正整数
如果是素数，输出"yes"
否则，输出"no"

Version: 0.0.1
Author : yichu.cheng
"""

import math

n = int(input("输入正整数:"))
# 素数首先是大于1的整数
is_prime = n > 1
end = int(math.sqrt(n))
for i in range(2, end+1):
    if n % i == 0:
        # 只要有一个整数能整除n，n就不是素数
        is_prime = False
        break
print("yes" if is_prime else "no")


def another_way(n):
    is_prime = n > 1
    if n < 6:
        is_prime = n in [2, 3, 5]
    elif n % 6 != 1 and n % 6 != 5:
        # 不满足 6x+1 和 6x+5 的一定不是素数
        is_prime = False
    else:
        end = int(math.sqrt(n))
        for i in range(5, end+1, 6):
            if n % i == 0 or n % (i+2) == 0:
                is_prime = False
                break
    return is_prime


# import sympy
# sympy.isprime(5)
# t_list = list(sympy.primerange(0, 1000000))
# for i in t_list:
#     if not another_way(i):
#         print(i)


# for i in range(1,10000000):
#     if sympy.isprime(i) != another_way(i):
#         print(i)
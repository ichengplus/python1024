# coding=utf-8

"""
输出九九乘法表

Version: 0.0.1
Author : yichu.cheng
"""

for i in range(1, 10):
    for j in range(1, i+1):
        print('%d*%d=%d' % (i, j, i * j), end='\t')
    print()

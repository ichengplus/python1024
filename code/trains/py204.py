# coding=utf-8

"""
输出[1,100]之间的偶数总和

Version: 0.0.1
Author : yichu.cheng
"""

total = 0
for i in range(1, 101):
    if i % 2 == 0:
        total += i
print('总和:', total)

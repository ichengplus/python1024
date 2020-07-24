# coding=utf-8

"""
输入字符串
输出反向字符串，且字符间以下划线相连

Version: 0.0.1
Author : yichu.cheng
"""

s = input('输入字符串:')
s_r = s[::-1]
print("_".join(s_r))

# coding=utf-8

"""
输入2个字符串
输出合并后没有重复字符的生序字符串

Version: 0.0.1
Author : yichu.cheng
"""

s1 = input('输入字符串1:')
s2 = input('输入字符串2:')
s = s1 + s2
s_set_sorted = sorted(set(s))
s_result = "".join(s_set_sorted)
print(s_result)

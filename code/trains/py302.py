# coding=utf-8

"""
输入英文句子，以'.'结尾，以','和空格分隔
输出其中每个英文字符，及其出现次数

Version: 0.0.1
Author : yichu.cheng
"""

s = input('输入英文句子:')
# 首先把英文句号和逗号符号替换掉，再按空格分割单词
words = s.replace('.', '').replace(',', '').split(' ')
s2 = "".join(words)

result1 = []
s2_set = sorted(set(s2))
for i in s2_set:
    c = s2.count(i)
    result1.append((i, c))

for (i, c) in result1:
    print("{} 出现了 {} 次".format(i, c))

# 同样算法，用列表生成器方式的写法
result2 = [(i, s2.count(i)) for i in sorted(set(s2))]
for (i, c) in result2:
    print("{} 出现了 {} 次".format(i, c))

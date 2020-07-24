# coding=utf-8

"""
基本文件处理

Version: 0.0.1
Author : yichu.cheng
"""

import os

file_name = 'data/file001.txt'
with open(file_name, 'w') as f:
    f.write('文件处理测试')

# 文件大小，单位：字节
print(os.path.getsize(file_name))

with open(file_name, 'r') as f:
    txt = f.read()
    print(txt)

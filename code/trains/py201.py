# coding=utf-8

"""
输入年份
输出yes（闰年）或no（非闰年）

Version: 0.0.1
Author : yichu.cheng
"""

# 写法一
year = int(input("输入年份: "))
if (year % 4) == 0:
    if (year % 100) == 0:
        if (year % 400) == 0:
            # 整百年能被400整除的是闰年
            print("yes")
        else:
            print("no")
    else:
        # 非整百年能被4整除的为闰年
        print("yes")
else:
    # 闰年必须是4的倍数
    print("no")


# 写法二
# 备注提示：and计算优先级高于or
# 从写法一里可以知道闰年的两种形式：4的倍数但不是整百，或者是400的倍数
is_leap = year % 4 == 0 and year % 100 != 0 or year % 400 == 0
print("yes" if is_leap else "no")

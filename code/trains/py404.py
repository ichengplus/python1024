# coding=utf-8

"""
定义一个Ball类及其三个子类，分别实现3种jump方法
从子类中随机生成一批Ball实例，根据其jump方法调用结果统计各子类实例数量

Version: 0.0.1
Author : yichu.cheng
"""

import random
from collections import Counter


class Ball(object):
    """
    Ball基础类
    """

    def jump(self):
        """
        哑方法，直接返回一个字符串
        """
        return 'ball'


class RedBall(Ball):
    """
    Ball子类
    """

    def jump(self):
        return 'Redball'


class YellowBall(Ball):
    """
    Ball子类
    """

    def jump(self):
        return 'Yellowball'


class BlueBall(Ball):
    """
    Ball子类
    """

    def jump(self):
        return 'Blueball'


class BallFactory(object):
    """
    Ball工厂，专门用于生成Ball实例
    工厂设计模式
    """
    @staticmethod
    def create_ball(ball_type):
        """
        静态方法，根据名字生成对应的Ball实例
        """
        if ball_type == 'red':
            return RedBall()
        elif ball_type == 'blue':
            return BlueBall()
        elif ball_type == 'yellow':
            return YellowBall()
        else:
            return Ball()


def proc():
    """
    主函数: 生成实例后执行
    """
    type_lst = ['red', 'yellow', 'blue']
    balls = [BallFactory.create_ball(random.choice(type_lst))
             for _ in range(100)]
    # 根据对象调用方法统计结果与类生成实例相同
    # 但这里主要展示不同类的统一方法调用
    # 实践应用：如web开发中广泛应用的拦截器模式
    jump_results = [b.jump() for b in balls]
    summary = Counter(jump_results)
    # summary = {}
    # for i in jump_results:
    #     summary[i] = summary.get(i, 0)+1

    print(dict(summary))


if __name__ == '__main__':
    proc()

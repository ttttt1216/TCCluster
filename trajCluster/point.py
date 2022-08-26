# 2022-08-25

import math
import numpy as np


class Point(object):
    """对轨迹中的点进行封装, 可以进行比较, 一些常用的计算, 如距离计算, dot计算等, 本point主要对2维的point进行封装
    method
    ------
        str: 返回point的字符串格式, ‘2.56557800, 1.00000000’
        +: 加号操作符, 实现两个point类型的相加操作
        -: 减号操作符, 实现两个point类型的减法运算
        distance(other): 实现两个Point类型的距离(欧式距离)计算
        dot(other): 实现两个Point对象的dot运算, 得到两个点的值: x**2 + y**2
    """

    def __init__(self, x, y, traj_id=None):
        self.trajectory_id = traj_id
        self.x = x
        self.y = y

    # 重写__repr__，实现print时的描述
    def __repr__(self):
        return "{0:.8f},{1:.8f}".format(self.x, self.y)

    # 实现输出点的坐标的方法
    def get_point(self):
        return self.x, self.y

    # 定义一个add方法,实现点的相加
    """
    冒号：官方叫做参数的类型建议符
    箭头：叫做函数返回值的类型建议符
    """
    def __add__(self, other: 'Point'):
        if not isinstance(other, Point):
            raise TypeError("The other type is not 'Point' type.")
        _add_x = self.x + other.x
        _add_y = self.y + other.y
        return Point(_add_x, _add_y, traj_id=self.trajectory_id)

    # 定义一个__sub__方法，实现点的减法
    def __sub__(self, other: 'Point'):
        if not isinstance(other, Point):
            raise TypeError("The other type is not 'Point' type.")
        _sub_x = self.x - other.x
        _sub_y = self.y - other.y
        return Point(_sub_x, _sub_y, traj_id=self.trajectory_id)

    # 实现给所有坐标点乘上一个数值
    def __mul__(self, x: float):
        if isinstance(x, float):
            return Point(self.x * x, self.y * x, traj_id=self.trajectory_id)
        else:
            raise TypeError("The other object must 'float' type.")

    # 实现给所有坐标点除以一个数值
    def __truediv__(self, x: float):
        if isinstance(x, float):
            return Point(self.x / x, self.y / x, traj_id=self.trajectory_id)
        else:
            raise TypeError("The other object must 'float' type.")

    # 实现计算两点之间的距离， 这里的距离是欧式距离 ！！！地理坐标系中可以这么就算吗？
    def distance(self, other: 'Point'):
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    # 实现点积
    def dot(self, other: 'Point'):
        return self.x * other.x + self.y * other.y

    # 创建数组
    def as_array(self):
        return np.array((self.x, self.y))


# ！！！需要考虑地理坐标中的距离计算方法
def _point2line_distance(point, start, end):
    """计算point到line的垂直距离通过向量的方式: distance = |es x ps| / |es|, es为起始点的项量表示, ps为point到start点的向量
    parameter
    ---------
        point: np.ndarray, a point, 2-dim point or 3-dim point.
        start and end: 同point的格式一致, 都为numpy的array格式
    return
    ------
        float, point点到start, end两点连线的垂直距离, 欧式距离
    """
    if np.all(np.equal(start, end)):
        return np.linalg.norm(point - start)
    # 点到直线的距离计算方法
    return np.divide(np.abs(np.linalg.norm(np.cross(end - start, start - point))),
                     np.linalg.norm(end - start))

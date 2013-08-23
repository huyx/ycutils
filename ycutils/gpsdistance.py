# -*- coding: utf-8 -*-
from math import pi, sin, cos, asin, acos, sqrt

EARTH_RADIUS = 6378137

PI_180 = pi / 180

def distance(la1, lo1, la2, lo2):
    """计算两点之间的距离

    :param la1, lo1: 第一个点的纬度、经度
    :param la2, lo2: 第二个点的纬度、经度
    """
    la1 = la1 * PI_180
    la2 = la2 * PI_180

    theta = (lo1 - lo2) * PI_180
    dist = sin(la1) * sin(la2) + cos(la1) * cos(la2) * cos(theta)
    dist = acos(dist)

    return dist * EARTH_RADIUS

def distance_2(lat1, lng1, lat2, lng2):
    """计算两点之间的距离，验证用

    :param la1, lo1: 第一个点的纬度、经度
    :param la2, lo2: 第二个点的纬度、经度
    """
    lat1 = lat1 * PI_180
    lat2 = lat2 * PI_180

    a = lat1 - lat2
    b = (lng1 - lng2) * PI_180

    s = sin(a/2)**2 + cos(lat1)*cos(lat2)*(sin(b/2)**2)
    s = 2 * asin(sqrt(s))

    return s * EARTH_RADIUS

if __name__ == '__main__':
    print distance(0, 113, 0, 114), distance(0, 113, 1, 114), distance(34, 113, 34, 114)
    print distance(34.1, 113.1, 34.1, 114.1)
    distance = distance_2
    print distance(0, 113, 0, 114), distance(0, 113, 1, 114), distance(34, 113, 34, 114)
    print distance(34.1, 113.1, 34.1, 114.1)
    import timeit
    print timeit.repeat("distance(0, 113, 0, 114)", "from gpsdistance import distance", number=100000)
    print timeit.repeat("distance(0, 113, 0, 114)", "from gpsdistance import distance_2 as distance", number=100000)

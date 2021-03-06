# -*- coding:utf8 -*-

import math
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

class coordinate:
    def __init__(self):
        latitude = float(0.0) #纬度
        longitude = float(0.0) #经度
        height = float(0.0)

def the_first_point(a1, a2, a3):
    b1 = pow(a1.latitude, 2) + pow(a1.longitude, 2)
    b2 = pow(a2.longitude, 2) + pow(a2.latitude, 2)
    b3 = pow(a3.latitude, 2) + pow(a3.longitude, 2)
    p1 = coordinate()
    p2 = coordinate()
    p3 = coordinate()
    if (b1 <= b2 and b1 <= b3):
        p1 = a1
        p2 = a2
        p3 = a3
    else:
        if (b2 <= b1 and b2 <= b3):
            p1 = a2
            p2 = a1
            p3 = a3
        else:
            if (b3 <= b2 and b3 <= b1):
                p1 = a3
                p2 = a1
                p3 = a2
    x = [p1, p2, p3]
    return x

def show_coordinate(a):
    str="(%f,%f,%f)"%(a.longitude,a.latitude,a.height)
    print str

'''获取相对坐标,即以o点为圆心,p的坐标'''
def relative_coordinate(p,o):
    p_t = coordinate()
    p_t.latitude = p.latitude - o.latitude
    p_t.longitude = p.longitude - o.longitude
    p_t.height = p.height - o.height
    return p_t

'''第一个圆弧轨道的圆心'''
def first_O(p1,p2):
    k1 =  (p1.longitude * -1.0) / (p1.latitude * 1.0)
    k2 = ((p2.longitude - p1.longitude) * -1.0) / ((p2.latitude - p1.latitude) * 1.0)
    a1 = p1.longitude * 1.0 / 2
    b1 = p1.latitude * 1.0 / 2
    a2 = p1.longitude
    b2 = p1.latitude
    O = coordinate()
    O.longitude = (b1 - b2 + k2 * a2 - k1 * a1) / (k2 - k1)
    O.latitude = k1 * (O.longitude - a1) + b1
    O.height = 0
    return O

'''第二个圆弧轨道的圆心'''
def second_O(p1,p2,p3):
    p1_t = relative_coordinate(p1,p3)
    p2_t = relative_coordinate(p2,p3)
    o = first_O(p2_t,p1_t)
    o.latitude += p3.latitude
    o.longitude += p3.longitude
    o.height += p3.height
    return o

'''判断转弯方向'''
def direction(p1,p2):
    k = p1.latitude / p1.longitude
    if(p2.latitude > p2.longitude * k):#在上方
        i = -1
    else:
        i = 1
    if(p2.longitude > 0):#在一四象限
        i *= -1
    return i#i为-1则顺时针,为1则逆时针

'''直线po的圆心角'''
def get_angle(p,o):
    p_t = coordinate()
    p_t.longitude = p.longitude - o.longitude
    p_t.latitude = p.latitude - o.latitude
    p_t.height = p.height - o.height
    k = p_t.latitude / p_t.longitude
    angle = math.atan(k)
    if (k < 0):
        if(p_t.latitude > 0):
            angle += math.pi
        else:
            angle += math.pi * 2
    else:
        if(p_t.latitude < 0):
            angle += math.pi
    return angle

'''第一个圆弧轨道'''
def first_circle(p1,p2,n):
    o = first_O(p1, p2)
    r = pow(pow(o.latitude, 2) + pow(o.longitude, 2), 0.5)
    d = direction(p1, p2)
    O = coordinate()
    O.latitude = 0
    O.longitude = 0
    O.height = 0
    a1 = get_angle(O, o)
    a2 = get_angle(p1, o)
    if (d == -1):
        if (a2 > a1):
            a2 -= 2 * math.pi
    else:
        if (a1 > a2):
            a1 -= 2 * math.pi
    a_i = math.fabs(a1 - a2) / n
    h_i = ( p1.height) / n
    path = []
    for i in range(0,n):
        path.append(coordinate())
        path[i].longitude = r * math.cos(a1 + a_i * i * d) + o.longitude
        path[i].latitude = r * math.sin(a1 + a_i * i * d) + o.latitude
        path[i].height = h_i * i
    return path

'''直线轨道'''
def the_line(p1,p2,n):
    x_i = (p2.longitude - p1.longitude) / n
    y_i = (p2.latitude -p1.latitude) / n
    h_i = (p2.height - p1.height) / n
    path = []
    for i in range(0,n):
        path.append(coordinate())
        path[i].longitude = p1.longitude + x_i * i
        path[i].latitude = p1.latitude + y_i * i
        path[i].height = p1.height + h_i * i
    return path

'''第二个圆弧轨道'''
def second_circle(p1,p2,p3,n):
    o = second_O(p1,p2,p3)
    r = pow(pow(o.latitude - p2.latitude, 2) + pow(o.longitude - p2.longitude, 2), 0.5)
    d = -1 * direction(relative_coordinate(p2,p3),relative_coordinate(p1,p3))
    a1 = get_angle(p2,o)
    a_i = math.pi * 2 / n
    h_i =(p3.height - p2.height) / n
    path = []
    for i in range(0,n):
        path.append(coordinate())
        path[i].longitude = r * math.cos(a1 + a_i * i * d) + o.longitude
        path[i].latitude = r * math.sin(a1 + a_i * i * d) + o.latitude
        path[i].height = p1.height + h_i * i
    return path

def boom_second(p1,p2,p3,n):
    return second_circle(p1,p2,p3,n)

def boom_third(p1,p2,p3,n):
    o = second_O(p1, p2, p3)
    r = pow(pow(o.latitude - p2.latitude, 2) + pow(o.longitude - p2.longitude, 2), 0.5)
    d = -1 * direction(relative_coordinate(p2, p3), relative_coordinate(p1, p3))
    a1 = get_angle(p2, o)
    a2 = get_angle(p3, o)
    if (d == -1):
        if (a2 > a1):
            a2 -= 2 * math.pi
    else:
        if (a1 > a2):
            a1 -= 2 * math.pi
    a_i = math.fabs(a1 - a2) / n
    h_i = (p2.height - p1.height) / n
    path = []
    for i in range(0, n):
        path.append(coordinate())
        path[i].longitude = r * math.cos(a1 + a_i * i * d) + o.longitude
        path[i].latitude = r * math.sin(a1 + a_i * i * d) + o.latitude
        path[i].height = p1.height + h_i * i
    return path

def set_path(x):
    p1 = x[0]
    p2 = x[1]
    p3 = x[2]
    o1_t1 = first_O(p1,p2)
    o1_t2 = first_O(p1,p3)
    if((pow(o1_t1.longitude,2)+pow(o1_t1.latitude,2))<(pow(o1_t2.longitude,2)+pow(o1_t2.latitude,2))):
        temp_p = p3
        p3 = p2
        p2 = temp_p
    return first_circle(p1,p2,500)+the_line(p1,p2,500)+second_circle(p1,p2,p3,500)

'''输入坐标点之后，调用该方法，返回识别的路径'''
def main(o,a1,a2,a3):
    return set_path(the_first_point(relative_coordinate(a1,o),relative_coordinate(a2,o),relative_coordinate(a3,o)))

def get_GPS(p,o):
    p_t = coordinate()
    p_t.latitude = p.latitude + o.latitude
    p_t.longitude = p.longitude + o.longitude
    p_t.height = p.height + o.height
    return p_t

def d3_points(x_list):
    #x_list = [[3,3,2],[4,3,1],[1,2,3],[1,1,2],[2,1,2]]
    plt.rcParams['figure.figsize'] = (60.0, 40.0)
    plt.rcParams['image.interpolation'] = 'nearest'
    fig = plt.figure() # 得到画面
    ax = fig.gca(projection='3d') # 得到3d坐标的图
    # 画点
    for x in x_list:
        ax.scatter(x[0],x[1],x[2],c='r')
    plt.savefig("d3_image.png",dpi=100)
    plt.show()




'''这里是举个例子，如何输入坐标点'''
a1 = coordinate()
a2 = coordinate()
a3 = coordinate()
o = coordinate()

a1.longitude = float(12223.0)
a1.latitude = float(3334.0)
a1.height = float(20.0)

a2.longitude = float(33144.0)
a2.latitude = float(515.0)
a2.height = float(20.0)

a3.longitude = float(6256.0)
a3.latitude = float(3946.0)
a3.height = float(20.0)

o.longitude = float(0)
o.latitude = float(0)
o.height = float(0)

x = main(o ,a1,a2,a3)
y=[]
for ele in x:
    y.append([ele.longitude,ele.latitude,ele.height])
print(y)
print(y[500])
print(y[1000])
print(y[1499])
d3_points(y)
'''x是路径的list,每取出一个都要做一次get_GPS（），这样就是原本输入的GPS坐标了，同时要将list顶部的元素移除'''
'''后面还要有一个投哪个的分支判别，判断是哪个就把哪个的boom方法返回的list“+”到x上'''
'''当x取尽之后，就让飞机返航'''



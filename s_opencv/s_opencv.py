# -*- coding:utf-8 -*-
"""
    aircv, 即opencv
    [官方文档](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html)
"""

import aircv
import cv2
# 创建画板
canvas = aircv.np.zeros((300,400,3), dtype='uint8')
# 显示画板
aircv.show(canvas)

# 在画板上画直线
aircv.cv2.line(
    img=canvas,
    pt1=(0,10),
    pt2=(20,10),
    color=(255,255,255)
)

# 画矩形，空心
aircv.cv2.rectangle(img=canvas,pt1=(3,3),pt2=(17,17),color=(255,255,255))
# 画实心矩形
aircv.cv2.rectangle(img=canvas,pt1=(3,3),pt2=(17,17),color=(255,255,255),thickness=-1)

# 画圆形
aircv.cv2.circle(img=canvas, center=(200,150), radius=120, color=(255,255,255), thickness=-1)

# 画椭圆
canvas = aircv.np.zeros((300,400,3), dtype='uint8')
aircv.cv2.ellipse(
    img=canvas,         # 指定画板
    center=(200,150),   # 指定中心点，第一个是纵坐标，第二个是横坐标
    axes=(100,200),     # 指定椭圆的横轴长度和纵轴长度
    angle=60,           # 顺时针旋转角度
    startAngle=0,       # startAngle-开始角度，endAngle-结束角度，endAngle=180可以绘制半圆
    endAngle=360, 
    color=(255,255,255)
)
aircv.show(canvas)

# 画多边形
canvas = aircv.np.zeros((300,400,3), dtype='uint8')
pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)  # 各个顶点座标
pts = pts.reshape((-1,1,2)) # 重塑数据形状, -1表示按其它维度计算出该维度的数量
aircv.cv2.polylines(img=canvas, pts=[pts], isClosed=True, color=(0,255,255), thickness=-1, lineType=33)
aircv.show(canvas)


aircv.cv2.polylines(img=canvas,pts=np.array([1]), color=(255,255,255), isClosed=1)
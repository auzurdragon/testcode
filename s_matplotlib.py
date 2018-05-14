"""matplotlib学习"""

import numpy as np
import matplotlib.pyplot as plt

# 绘制正弦曲线
# 创建数据集
t = np.arange(-1, 2, .01)
s = np.sin(2 * np.pi * t)

# 绘制正弦曲线。先保存到对象，后面使用plt.show()统一绘制
plt.plot(t,s)

# .axhline(y = 0, xmin = 0, xmax = 1, hold = None, **kwargs)
# xmin,xmax的取值范围为[0,1]，表示轴的百分比范围，比如xmin=0.25, xmax=0.75，即x轴长度的25%-75%
# 绘制一条红色的hline水平线在 y=0 的位置，线宽4px
l = plt.axhline(linewidth = 4, color='red')
# 指定坐标轴的范围，按照plt.axis([xmin, xmax, ymin, ymax]) 的样式
plt.axis([-1, 2, -1, 2])
plt.show()
plt.close()

# 绘制一条蓝色的水平线，在y=1的位置
plt.plot(t,s)
l = plt.axhline(y=1, color='b')
plt.axis([-1, 2, -1, 2])
plt.show()
plt.close()


# .axvline(x=0, ymin=0, ymax=1, hold=None, **kwargs) 绘制垂直线
plt.plot(t,s)
l = plt.axvline(x=0, ymin=0, linewidth=4, color='b')
plt.axis([-1, 2, -1, 2])
plt.show()
plt.close()


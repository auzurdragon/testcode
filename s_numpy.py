# pythonForDataAnalysis
# numpy

import numpy as np
# 创建ndarry
data1 = [6, 7.5, 8, 0, 1]
arr1 = np.array(data1)
arr1

# 将嵌套列表转换为多维数组
data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
arr2 = np.array(data2)
arr2

# 查看数组中的数据类型
arr1.dtype

# 转换数据类型
arr1.astype(np.int) # 转换为整数
arr2.astype(np.float64) # 转换为64位浮点数
arr2.astype(np.float) # 转换为浮点数
arr2.astype(np.string_) # 转换为二进制的字符串
arr2 = np.array([[1, 2, 3, 4], [5, 6, 7, 8]], dtype=np.float)  # 在创ndarray时指定dtype

# 数组运算
arr2+1  # 所有元素+1
arr2**2  # 所有元素的平方
arr2*arr2   # 所有元素的平方
1/arr2  # 所有元素的倒数

# 创建指定长度或形状的全0或全1数组
np.zeros(10)  # 创建长度10 的全0数组
np.ones((3,6))  # 创建形状为3,6的全1数组
np.empty((2, 3, 2))  # 创建形状为2,3,2的empty数组，其中不一定是0


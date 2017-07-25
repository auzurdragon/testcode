"""matplotlib学习"""

import numpy as np
import matplotlib.pyplot as plt

N = 5
menMeans = (20, 35, 30, 35,27)
menStd = (2, 3, 4, 1, 2)

ind = np.arange(N) # the x locations for the groups
width = 0.35    # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)
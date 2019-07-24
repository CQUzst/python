import numpy as np
from pylab import mpl
import matplotlib.pyplot as plt
import sys

mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字

file=open(r'D:/Data/coord.txt')
x=file.readline()
x=x[3:-2].split(",")
y=file.readline()
y = y[3:-2].split(",")
x=x[:-2]
y=y[:-2]
t=[]
# 数据格式转换成np.array
points=list([x,y])
for i in range(len(points[0])):
    t.append(i)
    x[i] = np.array(float(x[i])-418360)
    y[i] = np.array(float(y[i])-2561325)
x=np.array(x)
y=np.array(y)

k_size=15
pad=k_size//2
x_filterd=[]
y_filterd=[]
for i in range(0,len(x)):
    if(i< pad or i>=len(x)-pad):
        x_filterd.append(x[i])
        y_filterd.append(y[i])
    else:
        tmpCenter_x=0
        tmpCenter_y=0
        max_x=x[i]
        min_x=x[i]
        max_y=y[i]
        min_y=y[i]
        for j in range(-pad,-pad+k_size):
            if (max_x < x[i + j]):
                max_x=x[i+j]
            if (min_x > x[i + j]):
                min_x = x[i + j]
            if (max_y < y[i + j]):
                max_y = y[i + j]
            if (min_y < y[i + j]):
                min_y = y[i + j]
            tmpCenter_x+=x[i+j]
            tmpCenter_y+=y[i+j]
        x_filterd.append((tmpCenter_x-max_x-min_x)/(k_size-2))
        y_filterd.append((tmpCenter_y-max_y-min_y) / (k_size-2))

print(len(x_filterd))
# 可视化.创建包含2*3个子图的视图
fig, ((ax1), (ax2),(ax3)) = plt.subplots(1,3, figsize=(18, 12))
ax1.set_xlabel("time")
ax1.set_ylabel("x")
ax1.set_title("x(t)")
ax1.scatter(t, x, color='k', marker='.', label=u"数据点x")  # 散点x
ax1.scatter(t, x_filterd, color='r', marker='.', label=u"均值滤波")  # 散点x
# ax1.plot(t_list, x_list, color='r', linestyle='-', marker='.', label=u"一次指数平滑")

ax2.set_xlabel("time")
ax2.set_ylabel("y")
ax2.set_title("y(t)")
ax2.scatter(t, y, color='k', marker='.', label=u"数据点y")  # 散点y
ax2.plot(t,y_filterd, color='r', linestyle='-', marker='.', label=u"均值滤波")

ax3.set_xlabel("x")
ax3.set_ylabel("y")
ax3.set_title("worldCoordination")
ax3.scatter(x,y, color='k', marker='.', label=u"数据点y")  # 散点y
ax3.plot(x_filterd,y_filterd, color='r', linestyle='-', marker='.', label=u"均值滤波")


plt.show()

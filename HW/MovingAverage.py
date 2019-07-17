import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字

# print("x1=", x)
# 读入数据
file=open(r'D:/Data/coord.txt')
x=file.readline()
x=x[3:-2].split(",")
y=file.readline()
y = y[3:-2].split(",")

# 数据格式转换成np.array
points=list([x,y])
for i in range(len(points[0])):
    x[i] = np.array(float(x[i])-418360)
    y[i] = np.array(float(y[i])-2561325)
x=np.array(x)
y=np.array(y)
# x=x.astype(np.float32)
# y=y.astype(np.float32)
##################################
x1=[]
y1=[]
N=20
# Ft＝（xt-1＋xt-2＋xt-3＋…＋xt-n）/n
for i in range(0,len(x)):
    tmpX=0
    tmpY=0
    for j in range(0,N):
        if((i-j)<0):
            tmpX+=x[i]
            tmpY+=y[i]
        else:
            tmpX+=x[i-j]
            tmpY+=y[i-j]
    x1.append(tmpX/N)
    y1.append(tmpY/N)
plt.figure(figsize=(10,10))# 创建画布
plt.scatter(x,y,color='k',marker='.',label=u"数据点") # 散点
plt.plot(x1, y1, color='r', linestyle='-', marker='.', label=u"拟合曲线")
plt.legend(loc='upper left')
plt.show()

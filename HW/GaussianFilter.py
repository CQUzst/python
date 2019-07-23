import numpy as np
from pylab import mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字

file=open(r'D:/Data/coord.txt')
x=file.readline()
x=x[3:-2].split(",")
y=file.readline()
y = y[3:-2].split(",")

t=[]
# 数据格式转换成np.array
points=list([x,y])
for i in range(len(points[0])):
    t.append(i)
    x[i] = np.array(float(x[i])-418360)
    y[i] = np.array(float(y[i])-2561325)
x=np.array(x)
y=np.array(y)

K_size= 7
sigma = 4

x_filterd=[]
y_filterd=[]
## Kernel
K = np.zeros((K_size*2), dtype=np.float)
for i in range(1,K_size*2):
    K[i] = np.exp(-((i-K_size)**2) / (2 * (sigma**2)))
K /= (sigma * np.sqrt(2 * np.pi))
K /= K.sum()

for i in range(len(x)):#K_size,len(x)-K_size
    if(i<K_size or i>len(x)-K_size):
        x_filterd.append(x[i])
        y_filterd.append(y[i])
    else:
        tmp_x= np.sum(x[i-K_size:i+K_size]*K)
        tmp_y = np.sum(y[i - K_size:i + K_size] * K)
        x_filterd.append(tmp_x)
        y_filterd.append(tmp_y)

t=t[K_size:len(t)-K_size]
x=x[K_size:len(x)-K_size]
y=y[K_size:len(y)-K_size]
x_filterd=x_filterd[K_size:len(x_filterd)-K_size]
y_filterd=y_filterd[K_size:len(y_filterd)-K_size]


print(K)

fig, ((ax1), (ax2),(ax3)) = plt.subplots(1,3, figsize=(18, 12))
ax1.set_xlabel("time")
ax1.set_ylabel("x")
ax1.set_title("x(t)")
ax1.scatter(t, x, color='k', marker='.', label=u"数据点x")
ax1.scatter(t, x_filterd, color='r', marker='.', label=u"高斯滤波")

ax2.set_xlabel("time")
ax2.set_ylabel("y")
ax2.set_title("y(t)")
ax2.scatter(t, y, color='k', marker='.', label=u"数据点y")
ax2.plot(t,y_filterd, color='r', linestyle='-', marker='.', label=u"高斯滤波")

ax3.set_xlabel("x")
ax3.set_ylabel("y")
ax3.set_title("worldCoordination")
ax3.scatter(x,y, color='k', marker='.', label=u"数据点y")
ax3.plot(x_filterd,y_filterd, color='r', linestyle='-', marker='.', label=u"高斯滤波")


plt.show()




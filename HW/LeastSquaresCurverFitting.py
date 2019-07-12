import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字

x = np.arange(-1, 1, 0.01) # x 是n*1的数组
y = ((x * x - 1) ** 3 + 1) * (np.cos(x * 2) + 0.6 * np.sin(x * 1.3)) # y 是n*1的数组

y1 = y + (np.random.rand(len(x)) - 0.5)
# print("x1=", x)
# 读入数据
file=open(r'D:/Data/coord.txt')
x2=file.readline()
x2=x2[3:-2].split(",")
y2=file.readline()
y2 = y2[3:-2].split(",")

# 数据格式转换成np.array
points=list([x2,y2])
for i in range(len(points[0])):
    x2[i] = np.array(float(x2[i])-418360)
    y2[i] = np.array(float(y2[i])-2561325)
x2=np.array(x2)
y2=np.array(y2)
x=x2
y=y2
##################################
### 核心程序
# 使用函数y=ax^3+bx^2+cx+d对离散点进行拟合，最高次方需要便于修改，所以不能全部列举，需要使用循环
# A矩阵
m = []
for i in range(7):  # 这里选的最高次为x^7的多项式
    a = x ** (i) # a 是n*1的数组，a中是x[i]的i次方
    m.append(a)

A = np.array(m).T # A中一行为每一个x点的系数，一共n行

b = y.reshape(y.shape[0], 1) # reshape成一列
# 构造成Ax=b的形式

##################################

def projection(A, b):
    AA = A.T.dot(A)  # A乘以A转置
    w = np.linalg.inv(AA).dot(A.T).dot(b) # w即为所求多项式系数
    print(w)
    return A.dot(w)


yw = projection(A, b)
yw.shape = (yw.shape[0],)

plt.plot(x, y, color='g', linestyle='-', marker='', label=u"理想曲线")
#plt.plot(x, y1, color='m', linestyle='', marker='o', label=u"已知数据点")
plt.plot(x, yw, color='r', linestyle='', marker='.', label=u"拟合曲线")
plt.legend(loc='upper left')
plt.show()

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

##################################
### 核心程序
# 使用函数y=ax^3+bx^2+cx+d对离散点进行拟合，最高次方需要便于修改，所以不能全部列举，需要使用循环
# A矩阵
maxOrder=7
m = []
for i in range(maxOrder):  # 这里选最高次
    a = x ** (i) # a 是n*1的数组，a中是x[i]的i次方
    m.append(a)

A = np.array(m).T # A中一行为每一个x点的系数，一共n行
b = y.reshape(y.shape[0], 1) # reshape成一列

# 构造成Ax=b的形式
def projection(A, b):
    AA = A.T.dot(A)  # A乘以A转置
    w = np.linalg.inv(AA).dot(A.T).dot(b) # w即为所求多项式系数
    print(w)
    return A.dot(w)

yw = projection(A, b)
yw.shape = (yw.shape[0],)
plt.figure(figsize=(10,10))# 创建画布
plt.scatter(x,y,color='k',marker='.',label=u"数据点") # 散点
#plt.plot(x, y, color='r',marker='.',label=u"数据点") #散点连线
plt.plot(x, yw, color='r', linestyle='-', marker='.', label=u"拟合曲线")
plt.legend(loc='upper left')
plt.show()

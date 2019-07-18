# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字
##这里是将数据储存到数组里面
file = open(r'D:/Data/9.txt')
x=[]
y=[]
for line in file.readlines():
    line = line.strip('\n').split(',')  #去掉列表中每一个元素的换行符
    #print(line[1],line[2])
    x.append(np.array(float(line[1])- 418360))
    y.append(np.array(float(line[2])- 2561325))
x = np.array(x)
y = np.array(y)


# #读入李博数据
# file =open('D:/data/BP319U.txt','r', encoding='utf-8')
# x=[]
# y=[]
# for line in file.readlines():
#     line=line.strip('\n').split('\t')
#     yn = line[2][5:]
#     xn = line[3][5:]
#     # print(yn)
#     # print(xn)
#     x.append(np.array(float(xn)- 418360))
#     y.append(np.array(float(yn)- 2561325))
# x=np.array(x)
# y=np.array(y)

# y∗t+1=αyt+(1−α)y∗t
def exponential_smoothing(alpha, s):
    s_list = [0 for i in range(len(s))]
    s_list[0] = (s[0]+s[1]+s[2]+s[3]+s[4])/5
    for i in range(1, len(s)):
        s_list[i] = alpha * s[i] + (1 - alpha) * s_list[i - 1]
    return s_list

def compute_single(alpha, s):
    return exponential_smoothing(alpha, s)

def compute_double(alpha, s):
    s_single = compute_single(alpha, s)
    s_double = compute_single(alpha, s_single)

    a_double = [0 for i in range(len(s))]
    b_double = [0 for i in range(len(s))]

    for i in range(len(s)):
        a_double[i] = 2 * s_single[i] - s_double[i]  # 计算二次指数平滑的a
        b_double[i] = (alpha / (1 - alpha)) * (s_single[i] - s_double[i])  # 计算二次指数平滑的b
    return a_double, b_double,s_double

# alpha = 0.2
# x1 = exponential_smoothing(alpha, x)
# y1 = exponential_smoothing(alpha, y)
#
# plt.figure(figsize=(10, 10))  # 创建画布
# plt.scatter(x, y, color='k', marker='.', label=u"数据点")  # 散点
# plt.plot(x1, y1, color='r', linestyle='-', marker='.', label=u"拟合曲线")
# plt.legend(loc='upper left')
# plt.show()

alpha = 0.15
a1,b1,c1 = compute_double(alpha, x)
a2,b2,c2 = compute_double(alpha, y)
z1=[]
z2=[]
for i in range(len(a1)):
    z1.append(a1[i]+b1[i]*1)
    z2.append(a2[i]+b2[i]*1)

plt.figure(figsize=(10, 10))  # 创建画布
plt.scatter(x, y, color='k', marker='.', label=u"数据点")  # 散点
print(len(x),len(c1))
plt.plot(z1, z2, color='r', linestyle='-', marker='.', label=u"二次指数平滑")
plt.plot(c1, c2, color='b', linestyle='-', marker='.', label=u"一次指数滑动")
plt.legend(loc='upper left')
plt.show()


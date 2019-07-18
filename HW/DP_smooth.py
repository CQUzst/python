# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字
# 读入阳哥数据
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

plt.figure(figsize=(10, 10))  # 创建画布
plt.axis('equal')
# y∗t+1=αyt+(1−α)y∗t
x_list = [x[0]]
y_list = [y[0]]
x_list_double=[x_list[0]]
y_list_double=[y_list[0]]
x_double_exponential=[x[0]]
y_double_exponential=[y[0]]
a_double=0
b_double=0
alpha=0.15
for i in range(1,len(x)):
    real_time_x=x[i] # 实时最新坐标点x
    real_time_y=y[i] # 实时最新坐标点y
    x_list.append(alpha * real_time_x + (1 - alpha) * x_list[i - 1]) # 一阶指数平滑x
    y_list.append(alpha * real_time_y + (1 - alpha) * y_list[i - 1]) # 一阶指数平滑y
    x_list_double.append(alpha * x_list[i] + (1 - alpha) * x_list_double[i - 1]) # 二次一阶指数平滑x
    y_list_double.append(alpha * y_list[i] + (1 - alpha) * y_list_double[i - 1]) # 二次一阶指数平滑y
    x_a_double = 2 * x_list[i] - x_list_double[i]                       # 二次指数平滑x的系数a
    x_b_double = (alpha / (1 - alpha)) * (x_list[i] - x_list_double[i])  # 二次指数平滑的x的系数b
    y_a_double = 2 * y_list[i] - y_list_double[i]                       # 二次指数平滑y的系数a
    y_b_double = (alpha / (1 - alpha)) * (y_list[i] - y_list_double[i])  # 二次指数平滑y的系数b
    x_double_exponential.append(x_a_double+x_b_double*1) #二阶指数平滑x
    y_double_exponential.append(y_a_double + y_b_double * 1) #二阶指数平滑y
    plt.scatter(x[i], y[i], color='k', marker='.', label=u"数据点")  # 散点
    plt.plot(x_list, y_list, color='r', linestyle='-', marker='.', label=u"一次指数平滑")
    plt.plot(x_list_double, y_list_double, color='b', linestyle='-', marker='.', label=u"二次指数平滑")
    plt.plot(x_double_exponential, y_double_exponential, color='g', linestyle='-', marker='.', label=u"二阶指数平滑")
    plt.pause(0.001)
plt.show()
print("end")
# def compute_single(alpha, s):
#     return exponential_smoothing(alpha, s)
#
# def compute_double(alpha, s):
#     s_single = compute_single(alpha, s)
#     s_double = compute_single(alpha, s_single)
#
#     a_double = [0 for i in range(len(s))]
#     b_double = [0 for i in range(len(s))]
#
#     for i in range(len(s)):
#         a_double[i] = 2 * s_single[i] - s_double[i]  # 计算二次指数平滑的a
#         b_double[i] = (alpha / (1 - alpha)) * (s_single[i] - s_double[i])  # 计算二次指数平滑的b
#     return a_double, b_double,s_double

# plt.figure(figsize=(10, 10))  # 创建画布
# plt.scatter(x, y, color='k', marker='.', label=u"数据点")  # 散点
# print(len(x),len(c1))
# plt.plot(z1, z2, color='r', linestyle='-', marker='.', label=u"二阶指数平滑")
# plt.plot(c1, c2, color='b', linestyle='-', marker='.', label=u"二次指数滑动")
# plt.legend(loc='upper left')
# plt.show()


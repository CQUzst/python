# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字
plt.rcParams['axes.unicode_minus']=False #解决负数坐标显示问题

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
#     x.append(np.array(float(xn)- 418360))
#     y.append(np.array(float(yn)- 2561325))
# x=np.array(x)
# y=np.array(y)


# # 读入马哥数据
# file=open(r'D:/Data/coord.txt')
# x=file.readline()
# x=x[3:-2].split(",")
# y=file.readline()
# y = y[3:-2].split(",")
# points=list([x,y])
# for i in range(len(points[0])):
#     x[i] = np.array(float(x[i])-418360)
#     y[i] = np.array(float(y[i])-2561325)
# x=np.array(x)
# y=np.array(y)


plt.figure(figsize=(10, 10))  # 创建画布
plt.axis('equal')

t=[0] # 帧数集合t
#x_list,y_list用于实时显示数据点坐标
x_list=[x[0]]
y_list=[y[0]]
# 一阶指数平滑集合 y'（t)=αy(t)+(1−α)y'(t-1)
s_x = [x[0]]
s_y = [y[0]]

t_x=[0]
t_y=[0]

predict_x=[x[0]]
predict_y=[y[0]]
#两个超参
alpha=0.2 # alpha越小，平滑效果越好，滞后越明显
beta=0.15 #

# 动态更新
for i in range(1,len(x)):

    # 帧数集合
    t.append(i)

    x_list.append(x[i])
    y_list.append(y[i])
    # 实时最新坐标点
    real_time_x=x[i]
    real_time_y=y[i]
    # 一阶指数平滑
    s_x.append(alpha * real_time_x + (1 - alpha) * (s_x[i-1]+t_x[i - 1]))
    s_y.append(alpha * real_time_y + (1 - alpha) * (s_y[i-1]+t_y[i - 1]))

    t_x.append(beta * (s_x[i] - s_x[i - 1]) + (1 - beta) * t_x[i - 1])
    t_y.append(beta * (s_y[i] - s_y[i - 1]) + (1 - beta) * t_y[i - 1])

    predict_x.append(s_x[i] +1 * t_x[i])
    predict_y.append(s_y[i] +1 * t_y[i])

    plt.clf()# 清除画布所有内容，但是窗口打开，保持单窗口动态更新图片内容

    # 下面画图程序放到for循环内即动态更新，放外面即动态更新完再画图
    plt.scatter(x_list, y_list, color='k', marker='.', label=u"数据点")  # 散点
    plt.plot(predict_x, predict_y, color='r', linestyle='-', marker='.', label=u"指数平滑")# 连线
    # plt.plot(x_first_order_double_time, y_first_order_double_time, color='g', linestyle='-', marker='.', label=u"二次一阶指数平滑")
    # plt.plot(x_second_order, y_second_order, color='b', linestyle='-', marker='.', label=u"二阶指数平滑")
    # plt.plot(x_mixed_order, y_mixed_order, color='m', linestyle='-', marker='.', label=u"二阶指数+一阶平滑")
    plt.legend(loc='upper right') # 设置图片上label所在位置
    plt.pause(0.001)  # 图片更新间隔

# 保存每一帧图片
# string="DP"
# string+=str(i)
# string+=".png"
# plt.savefig(string)

plt.show()
print("end")

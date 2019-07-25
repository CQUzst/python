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
x_first_order = [x[0]]
y_first_order = [y[0]]
# 二次一阶指数平滑集合
x_first_order_double_time=[x_first_order[0]]
y_first_order_double_time=[y_first_order[0]]
# 二阶指数平滑集合
x_second_order=[x[0]]
y_second_order=[y[0]]
#二阶+一阶指数平滑集合
x_mixed_order=[x[0]]
y_mixed_order=[y[0]]

#两个超参  建议alpha2 取值为alpha的一半到alpha之间
alpha=0.2 # alpha越小，平滑效果越好，滞后越明显
alpha2=0.12 # alpha2是对二阶指数平滑结果进行修正，使平滑结果对趋势有响应,alpha2越小平滑效果越好,对数据变化响应越小

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
    x_first_order.append(alpha * real_time_x + (1 - alpha) * x_first_order[i - 1])
    y_first_order.append(alpha * real_time_y + (1 - alpha) * y_first_order[i - 1])

    # 二次一阶指数平滑
    x_first_order_double_time.append(alpha * x_first_order[i] + (1 - alpha) * x_first_order_double_time[i - 1])
    y_first_order_double_time.append(alpha * y_first_order[i] + (1 - alpha) * y_first_order_double_time[i - 1])

    # 二次指数平滑x轴a,b系数计算
    x_a = 2 * x_first_order[i] - x_first_order_double_time[i]
    x_b = (alpha / (1 - alpha)) * (x_first_order[i] - x_first_order_double_time[i])

    # 二次指数平滑y轴a,b系数计算
    y_a = 2 * y_first_order[i] - y_first_order_double_time[i]
    y_b = (alpha / (1 - alpha)) * (y_first_order[i] - y_first_order_double_time[i])

    # 二阶指数平滑
    x_second_order.append(x_a + x_b *1)
    y_second_order.append(y_a + y_b *1)

    # 二阶指数平滑+一次一阶指数平滑
    x_mixed_order.append(alpha2 * x_second_order[i] + (1 - alpha2) * x_mixed_order[i - 1])  # 一阶指数平滑x
    y_mixed_order.append(alpha2 * y_second_order[i] + (1 - alpha2) * y_mixed_order[i - 1])  # 一阶指数平滑y

    plt.clf()# 清除画布所有内容，但是窗口打开，保持单窗口动态更新图片内容

    # 下面画图程序放到for循环内即动态更新，放外面即动态更新完再画图
    plt.scatter(x_list, y_list, color='k', marker='.', label=u"数据点")  # 散点
    plt.plot(x_first_order, y_first_order, color='r', linestyle='-', marker='.', label=u"一阶指数平滑")# 连线
    plt.plot(x_first_order_double_time, y_first_order_double_time, color='g', linestyle='-', marker='.', label=u"二次一阶指数平滑")
    plt.plot(x_second_order, y_second_order, color='b', linestyle='-', marker='.', label=u"二阶指数平滑")
    plt.plot(x_mixed_order, y_mixed_order, color='m', linestyle='-', marker='.', label=u"二阶指数+一阶平滑")
    plt.legend(loc='upper right') # 设置图片上label所在位置
    plt.pause(0.001)  # 图片更新间隔

# 保存每一帧图片
# string="DP"
# string+=str(i)
# string+=".png"
# plt.savefig(string)

plt.show()
print("end")


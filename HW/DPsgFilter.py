import numpy as np
from scipy.signal import savgol_filter
from pylab import mpl
import matplotlib.pyplot as plt
import math
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字
# np.set_printoptions(precision=2)  # For compact display.
# file=open(r'D:/Data/coord.txt')
# x=file.readline()
# x=x[3:-2].split(",")
# y=file.readline()
# y = y[3:-2].split(",")
# x=x[:-2]
# y=y[:-2]
# t=[]
# # 数据格式转换成np.array
# points=list([x,y])
# for i in range(len(points[0])):
#     t.append(i)
#     x[i] = np.array(float(x[i])-418360)
#     y[i] = np.array(float(y[i])-2561325)
# x=np.array(x)
# y=np.array(y)

# # 读入阳哥数据
file = open(r'D:/Data/9.txt')
x=[]
y=[]
for line in file.readlines():
    line = line.strip('\n').split(',')
    x.append(np.array(float(line[1])- 418360))
    y.append(np.array(float(line[2])- 2561325))
x = np.array(x)
y = np.array(y)

def RMSE(x1,y1,x2,y2):
    res=0
    for i in range(len(x1)):
        res += ((x1[i]-x2[i])**2+(y1[i]-y2[i])**2)
    res=math.sqrt(res)
    return res

# 计算方位角函数
def azimuthAngle(x1,y1,x2,y2):
    angle = 0.0
    dx = x2 - x1
    dy = y2 - y1
    if x2 == x1:
        angle = math.pi / 2.0
        if y2 == y1:
            angle = 0.0
        elif y2 < y1:
            angle = 3.0 * math.pi / 2.0
    elif x2 > x1 and y2 > y1:
        angle = math.atan(dx / dy)
    elif  x2 > x1 and  y2 < y1 :
        angle = math.pi / 2 + math.atan(-dy / dx)
    elif  x2 < x1 and y2 < y1 :
        angle = math.pi + math.atan(dx / dy)
    elif  x2 < x1 and y2 > y1 :
        angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return (angle * 180 / math.pi)

def angle_evalution(x,y):
    angleList=[]
    angleDif=[]
    for i in range(1,len(x)):
        angle=azimuthAngle(x[i-1],y[i-1],x[i],y[i])
        angleList.append(angle)
        dist = math.sqrt((x[i] - x[i - 1]) ** 2 + (y[i] - y[i - 1]) ** 2)
    for i in range(len(angleList)-1):
        angleDif.append(abs(round(angleList[i+1]-angleList[i],3)))
    return sum(angleDif)/len(angleDif)

plt.figure(figsize=(10,10))# 创建画布
t=[i for i in range(2,len(x))]
print(len(x))
x_copy=[]
y_copy=[]
x_predict=[]
y_predict=[]
for i in range(len(x)):
    x_copy.append(x[i])
    y_copy.append(y[i])
    x_predict=savgol_filter(x_copy,31,3,mode='nearest')
    y_predict=savgol_filter(y_copy,31,3,mode='nearest')
    plt.clf()  # 清除画布所有内容，但是窗口打开，保持单窗口动态更新图片内容

    # 下面画图程序放到for循环内即动态更新，放外面即动态更新完再画图
    plt.scatter(x_copy, y_copy, color='k', marker='.', label=u"数据点")  # 散点
    plt.plot(x_predict, y_predict, color='r', linestyle='-', marker='.', label=u"平滑")  # 连线
    plt.legend(loc='upper right')  # 设置图片上label所在位置
    plt.pause(0.001)  # 图片更新间隔

# savgol_filter(x, 5, 2, mode='nearest')
loss=RMSE(x,y,x_predict,y_predict)
angle_difference=angle_evalution(x_predict,y_predict)
print("RMSE=",loss)
print("angle_difference=",angle_difference)

# plt.scatter(x,y,color='k',marker='.',label=u"数据点") # 散点
# plt.plot(x_predict, y_predict, color='r', linestyle='-', marker='.', label=u"拟合曲线")
# plt.legend(loc='upper left')
plt.show()

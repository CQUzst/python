import numpy as np
import matplotlib.pyplot as plt
import math
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字

# # 读入阳哥数据
# file = open(r'D:/Data/9.txt')
# x=[]
# y=[]
# for line in file.readlines():
#     line = line.strip('\n').split(',')
#     x.append(np.array(float(line[1])- 418360))
#     y.append(np.array(float(line[2])- 2561325))
# x = np.array(x)
# y = np.array(y)

# 读入马哥数据
file=open(r'D:/Data/coord.txt')
x=file.readline()
x=x[3:-2].split(",")
y=file.readline()
y = y[3:-2].split(",")
points=list([x,y])
for i in range(len(points[0])):
    x[i] = np.array(float(x[i])-418360)
    y[i] = np.array(float(y[i])-2561325)
x=np.array(x)
y=np.array(y)

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


# 绘图,画点
plt.figure(figsize=(10, 10))  # 创建画布
plt.axis('equal')

# 计算方位角
angleList=[]
angleDif=[]
distanceList=[]
for i in range(1,len(x)):
    angle=azimuthAngle(x[i-1],y[i-1],x[i],y[i])
    angleList.append(angle)
    dist = math.sqrt((x[i] - x[i - 1]) ** 2 + (y[i] - y[i - 1]) ** 2)
    distanceList.append(dist)
for i in range(len(angleList)-1):
    angleDif.append(round(angleList[i+1]-angleList[i],3))

print("angleList=",angleList)
print("angleDif=",angleDif)
print("angleList number=",len(angleList))
print("len(angleList)-1=",len(angleList)-1)


origin_x=x.copy()
origin_y=y.copy()
show_x=[x[0]]
show_y=[y[0]]
update_points_x=[x[0]]
update_points_y=[y[0]]
limit_angle=5

show_x.append(origin_x[1])
show_y.append(origin_y[1])
for i in range(1,len(x)-4):
    print(i)
    show_x.append(origin_x[i+2])
    show_y.append(origin_y[i+2])
    # if(angleDif[i]<5 and angleDif[i]>-5):
    #     update_points_x.append(x[i+2])
    #     update_points_y.append(y[i+2])
    # else:
    deltaAngle=abs(angleDif[i])
    if deltaAngle>90:
        deltaAngle-=90

    # print("distance", L)
    # L=math.sqrt((x[i+2] - x[i+1]) ** 2 + (y[i+2] - y[i+1]) ** 2)
    L=distanceList[i+1]
    toward_angle=angleList[i]
    # print("toward_angle", toward_angle)
    if angleDif[i]>5:
        toward_angle+=5
    if angleDif[i]<-5:
        toward_angle-=5
    # print("fixed_angle", toward_angle)
    delta_x=0
    delta_y=0
    if(toward_angle<=90):
        delta_x = L * math.sin(toward_angle / 180 * math.pi)
        delta_y = L * math.cos(toward_angle / 180 * math.pi)
    elif(toward_angle<=180):
        delta_x  = L * math.cos((toward_angle-90) / 180 * math.pi)
        delta_y -= L * math.sin((toward_angle-90) / 180 * math.pi)
    elif (toward_angle <= 270):
        delta_x -= L * math.sin((toward_angle-180) / 180 * math.pi)
        delta_y -= L * math.cos((toward_angle-180) / 180 * math.pi)
    else:
        delta_x -= L * math.cos((toward_angle-270) / 180 * math.pi)
        delta_y += L * math.sin((toward_angle-270) / 180 * math.pi)
    # print(i,origin_x[i],origin_y[i],x[i],y[i])
    x[i + 2] = x[i + 1]+delta_x
    y[i + 2] = y[i+1]+delta_y
    update_points_x.append(x[i+2])
    update_points_y.append(y[i+2])
    # 计算方位角
    angleList = []
    angleDif = []
    distanceList=distanceList[-2:]
    for i in range(1, len(x)-3):
        angle = azimuthAngle(x[i - 1], y[i - 1], x[i], y[i])
        angleList.append(angle)
        dist = math.sqrt((x[i+3] - x[i+2]) ** 2 + (y[i+3] - y[i+2]) ** 2)
        distanceList.append(dist)
    for i in range(len(angleList) - 1):
        angleDif.append(round(angleList[i + 1] - angleList[i], 3))

    plt.clf()
    plt.scatter(show_x, show_y, color='k', marker='.', label=u"数据点x")
    plt.plot(update_points_x, update_points_y, color='r', linestyle='-', marker='.', label=u"一阶指数平滑")# 连线
    plt.legend(loc='upper right') # 设置图片上label所在位置
    plt.pause(0.01)  # 图片更新间隔
plt.show()
# plt.scatter(origin_x, origin_y, color='k', marker='.', label=u"数据点x")
# # plt.scatter(update_points_x,update_points_y, color='r', marker='.', label=u"角度限制")
# plt.plot(update_points_x,update_points_y, color='r', linestyle='-', marker='.', label=u"角度限制")
# plt.title("drawPic")
# plt.xlabel("pointX")
# plt.ylabel("pointY")
#
# plt.legend()
# # plt.savefig('drawPic.png', dpi=500)  # 指定分辨率,plt自带的save不够清晰


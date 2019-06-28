import numpy as np
import matplotlib.pyplot as plt
import math
from pylab import mpl
import mpl_toolkits.axisartist as axisartist
import scipy
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字

# 读入数据
file=open(r'D:/Data/coord.txt')
x=file.readline()
x=x[3:-2].split(",")
y=file.readline()
y = y[3:-2].split(",")
x1=file.readline()
x1=x1[3:-2].split(",")
y1=file.readline()
y1 = y1[3:-2].split(",")
x2=file.readline()
x2=x2[3:-2].split(",")
y2=file.readline()
y2 = y2[3:-2].split(",")
z2=file.readline()
z2=z2[3:-1].split(",")

# 数据格式转换成np.array
points=list([x,y])
for i in range(len(points[0])):
    x[i] = np.array(float(x[i])-418360)
    y[i] = np.array(float(y[i])-2561325)
points1 = list([x1, y1])
for i in range(len(points1[0])):
    x1[i] = np.array(float(x1[i]) - 418360)
    y1[i] = np.array(float(y1[i]) - 2561325)
points2 = list([x2, y2])
for i in range(len(points2[0])):
    x2[i] = np.array(float(x2[i]) - 418360)
    y2[i] = np.array(float(y2[i]) - 2561325)
num=len(points1[0])
#print("x number=",len(points[0]))

#求导函数,传入x，y，第i个点，x轴间隔
def diffFunction(x,y,i):
    try:
        # 真实数据点求导
        deltaY = y[i*space + space] - y[i*space]
        slope = deltaY / (x[(i+1)*space] - x[i*space])
        return slope
    except Exception as e:
        print("i+k>len(x)，下标越界")

# 绘图,画点
fig=plt.figure(figsize=(10,10))# 创建画布
ax = axisartist.Subplot(fig, 111)
fig.add_axes(ax)
ax.axis["bottom"].set_axisline_style("->", size = 1.5)
ax.axis["left"].set_axisline_style("->", size = 1.5)
ax.axis["top"].set_visible(False) # 右边和上边框隐藏
ax.axis["right"].set_visible(False)
plot1=plt.plot(points[0], points[1],'.',label='original values')# 画真实点
plot2=plt.plot(points1[0], points1[1],'.',label='Smooth values')# 画平滑点
plot3=plt.plot(points2[0], points2[1],'*',color='r',label='special values')# 画特殊点
#选点间隔space，求导,计算斜率和角度
space=10
slopes=[]
angleList=[]
angleDif=[]
step=int(num/space)-1
for i in range(step):
    diffy=diffFunction(points1[0],points1[1],i)
    slopes.append(diffy)
    angle = math.degrees(math.atan(diffy))+90 # 上方为0°，右边为90°
    angleList.append(round(angle,3))
for i in range(len(angleList)-1):
    angleDif.append(round(angleList[i+1]-angleList[i],3))
print(slopes)
print("angleList=",angleList)
print("angleList number=",len(angleList))

print("len(angleList)-1=",len(angleList)-1)
print(points1[0][space * ( 1)],points1[1][space * 1],slopes[0])

#标注
for i in range(len(angleList)):
    plt.text(points1[0][space*i]+0.1, points1[1][space*i], angleList[i], fontsize=10, alpha = 0.9)# 标注出绝对角度
    try:
        plt.quiver(points1[0][space * (i+1)], points1[1][space * (i+1)], 1, slopes[i]/2, color='black', width=0.002)  # 绘制箭头
    except Exception as e:
        print("下标越界")
    if i<len(angleDif):
        plt.text(points1[0][space * (i + 1)], points1[1][space * (i + 1)] - 0.5, "△", fontsize=10)
        plt.text(points1[0][space * (i+1)]+0.3, points1[1][space * (i+1)]-0.5, angleDif[i], fontsize=10, alpha=0.9) # 标注相对角度差

plt.title("drawPic")
plt.xlabel("pointX")
plt.ylabel("pointY")
plt.xlim(15,30)  # 坐标轴范围
plt.ylim(0,30)
plt.legend()
plt.savefig('drawPic.png', dpi=500)  # 指定分辨率,plt自带的save不够清晰
plt.show()

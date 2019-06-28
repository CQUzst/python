import numpy as np
import matplotlib.pyplot as plt
import math
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']# plt显示汉字

# 读入数据
file=open(r'D:/Data/testPoint.txt')
x=file.readline()
x=x[1:-2].split(",")
y=file.readline()
y = y[1:-1].split(",")

# 数据格式转换成np.array
points=list([x,y])
for i in range(len(points[0])):
    x[i] = np.array(float(x[i]))
    y[i] = np.array(float(y[i]))

# 用N次多项式拟合
coefficients = np.polyfit(points[0], points[1],3)
fitFunction = np.poly1d(coefficients)
print("拟合曲线函数")
print(fitFunction)

#求导函数,传入x，y，第i个点，x轴间隔
def diffFunction(x,y,i,k):
    try:
        # 真实数据点求导
        # deltaY = y[i + k] - y[i]
        # 拟合曲线求导
        deltaY = np.polyval(fitFunction,points[0][i + k]) - np.polyval(fitFunction,points[0][i])
        slope = deltaY / (x[i + k] - x[i])
        return slope
    except Exception as e:
        print("i+k>len(x)，下标越界")

#选点间隔space，求导,计算斜率和角度
space=1
slopes=[]
angleList=[]
angleDif=[]
for i in range(len(points[0])-space):
    diffy=diffFunction(points[0],points[1],i,space)
    slopes.append(diffy)
    angle = math.degrees(math.atan(diffy))+90 # 上方为0°，右边为90°
    angleList.append(round(angle,3))
for i in range(len(angleList)-1):
    angleDif.append(round(angleList[i+1]-angleList[i],3))
print(slopes)
print(angleList)
print(angleDif)

# 绘图
plt.figure(figsize=(10,10))
yvals=np.polyval(fitFunction,x)
plot1=plt.plot(points[0], points[1],'.',label='original values')
plot2=plt.plot(x, yvals,'r',label='polyfit values')
for i in range(len(angleList)):
    #plt.text(points[0][space*i]-0.6,points[1][space*i] , '绝对角度', fontsize=10, alpha = 0.9)
    plt.text(points[0][space*i]+0.1, points[1][space*i], angleList[i], fontsize=10, alpha = 0.9)
    if i < len(angleList):
        #注意这里yvals是拟合曲线的位置，可替换成points[1]真实数据点位置
        plt.quiver(points[0][space * (i + 1)], yvals[space * (i + 1)], 1, slopes[i], color='black', width=0.002)  # 绘制箭头
    if i<len(angleDif):
        #plt.text(points[0][space * (i + 1)]-0.4, points[1][space * (i + 1)] - 0.5,  '角度差', fontsize=10, alpha=0.9)
        plt.text(points[0][space * (i+1)]+0.1, points[1][space * (i+1)]-0.3, angleDif[i], fontsize=10, alpha=0.9)


plt.title("test")
plt.xlabel("X")
plt.xlabel("Y")
plt.xlim(0,10)
plt.ylim(0,10)
plt.legend()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import math
from pylab import mpl
import mpl_toolkits.axisartist as axisartist
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
fig=plt.figure(figsize=(10,10))# 创建画布
ax = axisartist.Subplot(fig, 111)
fig.add_axes(ax)
ax.axis["bottom"].set_axisline_style("->", size = 1.5)
ax.axis["left"].set_axisline_style("->", size = 1.5)
ax.axis["top"].set_visible(False) # 右边和上边框隐藏
ax.axis["right"].set_visible(False)
yvals=np.polyval(fitFunction,x)# 拟合曲线函数
plot1=plt.plot(points[0], points[1],'.',label='original values')# 画真实点
plot2=plt.plot(x, yvals,'r',label='polyfit values')# 画拟合点
for i in range(len(angleList)):
    plt.text(points[0][space*i]+0.1, points[1][space*i], angleList[i], fontsize=10, alpha = 0.9)# 标注出绝对角度
    if i < len(angleList):
        #注意这里yvals是拟合曲线的位置，可替换成points[1]真实数据点位置
        plt.quiver(points[0][space * (i + 1)], yvals[space * (i + 1)], 1, slopes[i], color='black', width=0.002)  # 绘制箭头
    if i<len(angleDif):
        plt.text(points[0][space * (i+1)]+0.1, points[1][space * (i+1)]-0.3, angleDif[i], fontsize=10, alpha=0.9) # 标注相对角度差

plt.title("drawPic")
plt.xlabel("pointX")
plt.ylabel("pointY")
plt.xlim(0,10)  # 坐标轴范围
plt.ylim(0,10)
plt.legend()
# plt.savefig('drawPic.png', dpi=500)  # 指定分辨率,plt自带的save不够清晰
plt.show()

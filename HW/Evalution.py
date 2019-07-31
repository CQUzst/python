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
    return sum(angleDif)

loss=RMSE(x,y,x_predict,y_predict)
angle_difference=angle_evalution(x_predict,y_predict)

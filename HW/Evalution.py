def RMSE(x1,y1,x2,y2):
    res=0
    for i in range(len(x1)):
        res += ((x1[i]-x2[i])**2+(y1[i]-y2[i])**2)
    res=math.sqrt(res)
    return res
    
loss=RMSE(x_list,y_list,predict_x,predict_y)
print("RMSE=",loss)

from PIL import Image
import numpy as np
import cv2

fps = 30    #保存视频的FPS，可以适当调整
size=(1000,992)
#可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoWriter = cv2.VideoWriter('D:/3.avi',fourcc,fps,size)#最后一个是保存图片的尺寸


outfilename = "my.gif" # 转化的GIF图片名称
filenames = []         # 存储所需要读取的图片名称
for i in range(1,234):   # 读取100张图片
    filename = "D:/pyProj/"    # path是图片所在文件，最后filename的名字必须是存在的图片
    string = "DP"
    string += str(i)
    string += ".png"
    filename+=string
    filenames.append(filename)              # 将使用的读取图片汇总
frames = []
for image_name in filenames:                # 索引各自目录
    im = cv2.imread(image_name)             # 将图片打开，本文图片读取的结果是RGBA格式，如果直接读取的RGB则不需要下面那一步
    #cv2.imshow(image_name,im)
    videoWriter.write(im)
    cv2.waitKey(3)
videoWriter.release()

# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:13:08 2020

@author: lenovo
"""

import cv2
mp4 = cv2.VideoCapture(r'D:\XM\山东智慧服务区\排队检测\test2.flv')  # 读取视频
is_opened = mp4.isOpened()  # 判断是否打开
print(is_opened)
fps = mp4.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
print("fps: "+str(fps))
widght = mp4.get(cv2.CAP_PROP_FRAME_WIDTH)  # 获取视频的宽度
height = mp4.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 获取视频的高度
print(str(widght) + "x" + str(height))
i = 0
while is_opened:

    (flag, frame) = mp4.read()  # 读取图片    
    if flag==False:  
        break
    else:
        i += 1
    file_name = "Images" + str(i) + ".jpg"
    print(file_name)
    if flag == True:
        cv2.imwrite(file_name, frame, [cv2.IMWRITE_JPEG_QUALITY])  # 保存图片
print("转换完成")


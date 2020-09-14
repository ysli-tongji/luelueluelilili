# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 10:04:20 2019

@author: lenovo
"""
import pand
import os
import cv2 as cv
import pandas as pd
from PIL import Image,ImageFont,ImageDraw
import numpy as np

csv_path=r'C:\Users\lenovo\Desktop\result.csv'
img_path=r'G:\Frontview_images'
out_path=r'G:\test'

data=pd.read_csv(csv_path)
grouped=data.groupby(by='图像编号')
for item in grouped:
    img_name=item[0]+'.jpg'
    img=cv.imread(os.path.join(img_path,img_name))
    for infor in item[1].iterrows():
        class_name=infor[1][3]
        xmin=int(infor[1][5])
        ymin=int(infor[1][6])
        xmax=int(infor[1][7])
        ymax=int(infor[1][8])
        cv.rectangle(img,(xmin,ymin),(xmax,ymax),(255,0,0),thickness=7 )
        img_PIL = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB)) 
        a=ImageFont.load_default()
        font = ImageFont.truetype("simhei.ttf",40) 
        fillColor = (255,0,0) 
        position = (xmin-30,ymin-30) 
        #class_name=class_name.decode('utf8')  
        draw = ImageDraw.Draw(img_PIL) 
        draw.text(position, class_name, font=font, fill=fillColor) 
        img= cv.cvtColor(np.asarray(img_PIL),cv.COLOR_RGB2BGR) 
        #cv.putText(img,class_name,(xmin-10,ymin-10),cv.FONT_HERSHEY_COMPLEX,0.9,(255,0,0),thickness=3)
    cv.imwrite(os.path.join(out_path,img_name),img)
    
       

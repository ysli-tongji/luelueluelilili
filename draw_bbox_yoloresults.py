# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 18:57:45 2021

@author: Eason
"""

import os
import cv2 as cv
import pandas as pd
from PIL import Image,ImageFont,ImageDraw
import numpy as np
from tqdm import tqdm

yolo_results_path = r'C:\Users\Eason\Desktop\fsdownload\B榜\test_result\v4_final'
img_path=r'G:\SODIC\test_B\test_B\images'
out_path=r'G:\SODIC\test_B\predictions\v4_final'
thred = 0.4
predictions = pd.DataFrame()
files = os.listdir(yolo_results_path)
for file in tqdm(files):
    result_txt = os.path.join(yolo_results_path,file)
    class_name = file.split('.')[0].split('_')[-1]
    with open(result_txt,'r') as f:
        lines = f.readlines()
    for line in lines:
        tmp = {}
        items = line.split(' ')
        tmp['filename'] = items[0]+'.jpg'
        tmp['class_name'] = class_name
        tmp['confidence'] = float(items[1])
        tmp['xmin'] = float(items[2])
        tmp['ymin'] = float(items[3])
        tmp['xmax'] = float(items[4])
        tmp['ymax'] = float(items[5])
        if tmp['confidence'] <= thred:
            continue
        predictions = predictions.append([tmp],ignore_index=True)
        
grouped=predictions.groupby(by='filename')
for item in tqdm(grouped):
    img_name=item[0]
    img=cv.imread(os.path.join(img_path,img_name))
    for infor in item[1].iterrows():
        confidence = infor[1][2]
        class_name=infor[1][1]
        xmin=int(infor[1][3])
        ymin=int(infor[1][4])
        xmax=int(infor[1][5])
        ymax=int(infor[1][6])
        cv.rectangle(img,(xmin,ymin),(xmax,ymax),(255,0,0),thickness=4 )
        img_PIL = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB)) 
        a=ImageFont.load_default()
        font = ImageFont.truetype("simhei.ttf",40) 
        fillColor = (255,0,0) 
        position = (xmin-30,ymin-30) 
        #class_name=class_name.decode('utf8')  
        draw = ImageDraw.Draw(img_PIL) 
        draw.text(position, class_name+str(confidence), font=font, fill=fillColor) 
        img= cv.cvtColor(np.asarray(img_PIL),cv.COLOR_RGB2BGR) 
        #cv.putText(img,class_name,(xmin-10,ymin-10),cv.FONT_HERSHEY_COMPLEX,0.9,(255,0,0),thickness=3)
    cv.imwrite(os.path.join(out_path,img_name),img)
    # print(os.path.join(out_path,img_name))
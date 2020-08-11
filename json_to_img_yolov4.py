# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 21:11:56 2020

@author: lenovo
"""


import json
import os
import cv2 as cv


json_path=r'C:\Users\lenovo\Desktop\result.json'          

def to_img(item,images_path,to_path,thre_confidence=0.5):
    filename=os.path.basename(item['filename'])
    objs=item['objects']
    img=cv.imread(os.path.join(images_path,filename))
    img_w,img_h=img.shape[0:2]
    for obj in objs:
        confidence=obj['confidence']
        class_name=obj['name']
        x,y,w,h=obj['relative_coordinates'].values()
        if float(confidence)>thre_confidence:
            w=w*img_w
            h=h*img_h
            xmin=int(x*img_w-w/2)
            ymin=int(y*img_h-h/2)
            xmax=int(x*img_w+w/2)
            ymax=int(y*img_h+h/2)
            class_con=str(class_name)+' '+str(confidence)
            cv.rectangle(img,(xmin,ymin),(xmax,ymax),(255,0,0),thickness=8 )
            cv.putText(img,class_con,(xmin-10,ymin-10),cv.FONT_HERSHEY_COMPLEX,0.8,(255,0,0),thickness=2)
    cv.imwrite(os.path.join(to_path,filename),img)        

with open(json_path,'r') as f :
    data = json.load(f)
    
for item in data:
    objects=item['objects']
    if len(objects)>0:
        to_img(item,r'H:\GPR_july\images',r'H:\GPR_july\predictions_v4')
     
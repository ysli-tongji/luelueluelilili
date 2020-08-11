# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 21:48:31 2020

@author: lenovo
"""


import json
import os
import pandas as pd


json_path=r'C:\Users\lenovo\Desktop\result.json'          
    

with open(json_path,'r') as f :
    data = json.load(f)
results=pd.DataFrame(columns=['filename','classname','confidence','x_cen','y_cen','w','h'])

for item in data:
    objects=item['objects']
    if len(objects)>0:
        filename=os.path.basename(item['filename'])
        for obj in objects:
            confidence=obj['confidence']
            class_name=obj['name']
            x,y,w,h=obj['relative_coordinates'].values()
            tmp={
                'filename':[filename],
                'classname':[class_name],
                'confidence':[confidence],
                'x_cen':[x],
                'y_cen':[y],
                'w':[w],
                'h':[h]}
            results=results.append(pd.DataFrame(tmp),ignore_index=True)
results.to_csv(r'C:/Users/lenovo/Desktop/yolov4_prediction.csv')
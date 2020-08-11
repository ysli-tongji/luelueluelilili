# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 10:27:54 2020

@author: lenovo
"""


import os
import pandas as pd

class_name={
    'Crack':0,
    'Patch-Crack':1,
    'Pothole':2,
    'Patch-Pothole':3,
    'Net':4,
    'Patch-Net':5,
    'Manhole':6,
    'Hinged-Joint':7
    }
new_dict = {v : k for k, v in class_name.items()}
data=pd.DataFrame(columns=['name','x_cen','y_cen','w','h'])
paths=[r'H:\WaiHuan_20200624\WaiHuan_20200624\labels',
      r'H:\task_checked_wuhan_return2-1-2020_07_04_04_04_14-yolo 1.1\obj_train_data',
      r'H:\task_wuhan_return2-2-2020_07_07_12_29_20-yolo 1.1\obj_train_data']
for path in paths:
    files=os.listdir(path)
    for file in files:
        if os.path.splitext(file)[1]=='.txt':
            with open(os.path.join(path,file),'r') as f:
                lines=f.readlines()
                for line in lines:
                    tmp=line.split(' ')
                    name=new_dict[int(tmp[0])]
                    x_cen=tmp[1]
                    y_cen=tmp[2]
                    w=tmp[3]
                    h=tmp[4]
                    data=data.append({'name':name,'x_cen':x_cen,'y_cen':y_cen,'w':w,'h':h},ignore_index=True)

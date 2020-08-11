# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 10:56:13 2020

@author: lenovo
"""


import pandas as pd
import os

path=r'H:\GPR_july\yolov3'
data=pd.DataFrame(columns=['filename','classname','confidence','xmin','ymin','xmax','ymax'])
for file in os.listdir(path):
    class_name=file.split('_')[-1].split('.')[0]
    with open(os.path.join(path,file),'r') as f:
        lines=f.readlines()
        for line in lines:
            tmp=line.split(' ')
            data=data.append(pd.DataFrame({
                'filename':[tmp[0]],
                'classname':[class_name],
                'confidence':[tmp[1]],
                'xmin':[tmp[2]],
                'ymin':[tmp[3]],
                'xmax':[tmp[4]],
                'ymax':[tmp[5]]}),ignore_index=True)
data['section']=None
data['frequence']=None
data['trace']=None
for index,item in data.iterrows():
    tmp=data.loc[index,'filename'].split('_')
    data.loc[index,'section']=tmp[0]
    data.loc[index,'frequence']=tmp[1]
    data.loc[index,'trace']=tmp[2]

data.to_csv(r'H:\GPR_july\yolov3\result.csv')
                
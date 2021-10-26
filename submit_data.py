# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 14:50:15 2021

@author: Eason
"""

import json
import pandas as pd
import os


change_class={
'Crack':1,
'Manhole':2,
'Net':3,
'Pothole':4,
'Patch-Crack':5,
'Patch-Net':6,
'Patch-Pothole':7,
'Other':8
    }

def change_line(line,class_name):
    line_items = line.split(' ')
    tmp={}
    tmp["image_id"] = int(line_items[0])  
    xmin = float(line_items[2])
    ymin = float(line_items[3])
    width = float(line_items[4]) - xmin
    height = float(line_items[5]) - ymin
    tmp["bbox"] = [xmin,ymin,width,height]
    tmp["score"] = float(line_items[1])
    tmp["category_id"] = change_class[class_name]
    
    return tmp

txt_path = r'C:\Users\Eason\Desktop\fsdownload\B榜\test_result\v4_final'
files = os.listdir(txt_path)
result = []
for file in files:
    path = os.path.join(txt_path,file)
    class_name = file.split('_')[-1].split('.')[0]
    with open(path,'r') as f:
        lines = f.readlines()
        for line in lines:
            tmp = change_line(line, class_name)
            # if tmp["category_id"] == 8:
            #     continue
            result.append(tmp)

json.dump(result,open(r'C:\Users\Eason\Desktop\fsdownload\B榜\test_result\v4_final.json','w'),indent=4)
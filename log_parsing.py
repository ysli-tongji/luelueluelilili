# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 15:16:50 2019

@author: lenovo
"""

import pandas as pd

path=r'C:\Users\lenovo\Desktop\fd_v1.log'
file=open(path)
lines=file.readlines()

total=[]
num=[]
loss=[]
avg=[]
rate=[]
images=[]

for line in lines:
    if str(line.split(' ')[-1]) == 'images\n':
        total.append(line)

for item in total:
    num.append(int(item.split(':')[0]))
    loss.append(float(item.split(' ')[1].split(',')[0]))
    avg.append(float(item.split(' ')[2]))
    rate.append(float(item.split(' ')[4]))
    images.append(int(item.split(' ')[-2]))

file.close()
results={
        'num':num,
        'loss':loss,
        'avg':avg,
        'rate':rate,
        'images':images
        }

pd.DataFrame(results).to_csv(r'C:\Users\lenovo\Desktop\fd_v1.csv',index=False)
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 22:47:50 2020

@author: lenovo
"""

import requests
import pandas as pd
import time
import json

def getNewGPS(gps,key='3161e1ef4a927ee3f51b3733798908f3'):
    '''
    因为我们的GPS和高德不一个体系
    use gaodeAPI to change gps
    gps: type:string
    key: the key of API, and the type of key is string
    '''
    
    url='https://restapi.amap.com/v3/assistant/coordinate/convert?key='+key+'&locations='+gps+'&coordsys=gps'
    #print(url)
    r=requests.get(url)
    tem=r.text
    split_tem=tem.split('''"''')
    status=split_tem[3]
    info=split_tem[11]
    if status=='0':
        print(gps+' is fail and the info is:'+info)
    new_gps=split_tem[15]
    return new_gps,status,info



def getAllGPS (gpsdir,enc='utf-8'):
    '''
    read gps from csv 
    gpsdir:The dir of gpscsv,eg:D:\\XM_横向项目\\数据中心建设\\gps20181026.csv
    enc:The encoding of csv,eg:utf-8
    '''
    time_gps={}
    time=[]
    jing=[]
    wei=[]
    gps=[]
    with open(gpsdir,encoding=enc) as f:
        reader=csv.reader(f)
        for row in reader:
            time.append(row[0])
            jing.append(row[2])
            wei.append(row[1])
            gps.append(row[2]+","+row[1])   
            time_gps[row[0]]=row[2]+","+row[1]
    return time_gps,gps,time,jing,wei

def string_unix(tm):
    tm = time.mktime(time.strptime(tm, "%Y-%m-%d %H:%M:%S"))
    
    return tm

path = r'C:\Users\lenovo\Desktop\gps.csv'
gps_data = pd.read_csv(path)
split_data = gps_data.iloc[0:100,:]
split_data['old_gps'] = None
split_data['new_gps'] = None
for index, value in split_data.iterrows():
    wei = split_data.iloc[index, 1]
    jing = split_data.iloc[index,2]
    old_gps = str(round(jing,6))+','+str(round(wei,6))
    split_data.loc[index,'old_gps'] = old_gps
    new_gps,status,info = getNewGPS(old_gps)
    split_data.loc[index,'new_gps'] = new_gps
split_data['x'] = None
split_data['y'] = None
for index,value in split_data.iterrows():
    x = split_data.loc[index,'new_gps'].split(',')[0]
    y = split_data.loc[index,'new_gps'].split(',')[1]
    split_data.loc[index,'x'] = x
    split_data.loc[index,'y'] = y

list_body = []
for index,value in split_data.iterrows():
    dict_object = {}
    dict_object['x'] = round(float(split_data.loc[index,'x']),6)
    dict_object['y'] = round(float(split_data.loc[index,'y']),6)
    dict_object['ag'] = split_data.loc[index,'angle']
    if index == 0:
        tm = string_unix(split_data.loc[index,'time'])
        tm = int(tm)
    else:
        up = int(string_unix(split_data.loc[index-1,'time']))
        down = int(string_unix(split_data.loc[index,'time']))
        tm = down - up
    dict_object['tm'] = tm
    dict_object['sp'] = split_data.loc[index,'speed']
    list_body.append(dict_object)

#调用服务
url = 'https://restapi.amap.com/v4/grasproad/driving?key=3161e1ef4a927ee3f51b3733798908f3'
json_array = json.dumps(list_body)
response = requests.post(url, data = json_array)
results = json.loads(response.text)
if results['errcode'] == 0:
    result_data = results['data']
    print('total distance is: '+str(result_data['distance']))
    points = result_data['points']

new_gps_data = pd.DataFrame(columns=['id','gps'])
for i in range(len(points)):
    new_gps_data.loc[i,'id'] = i
    gps = str(points[i]['x']) + ',' + str(points[i]['y'])
    new_gps_data.loc[i,'gps'] = gps

split_data.to_csv(r'C:\Users\lenovo\Desktop\split_gps.csv',index=False)
new_gps_data.to_csv(r'C:\Users\lenovo\Desktop\new_gps_data.csv',index = False)
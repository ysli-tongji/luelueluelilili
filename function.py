# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:41:54 2019

@author: lenovo
"""

import os
import requests
import xml.dom.minidom as xmldom
import xml.etree.ElementTree as ET
import pandas as pd
import csv

def getAllGPS(gpsdir,enc='utf-8'):
    '''
    read gps from csv
    gpsdir: The dir of gpscsv, eg:
    enc: The encoding of csv, eg:utf-8
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
            gps.append(row[2]+','+row[1])
            time_gps[row[0]]=row[2]+','+row[1]
    return time_gps,gps,time,jing,wei
def getNewGPS(gps,key='3161e1ef4a927ee3f51b3733798908f3'):
    '''
    use gaodeAPI to change gps
    gps:type:string
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
        print(gps+ ' is fail and the info is: '+info)
    new_gps=split_tem[15]
    return new_gps,status,info

def getRoad(gps,key='3161e1ef4a927ee3f51b3733798908f3',radius=1000,roadlevel=0):
    '''
    use gaodeAPI get the road structure of gps in gaode
    gps:type:string
    key: the key of API, and the type of key is string
    '''
    
    url='''https://restapi.amap.com/v3/geocode/regeo?output=xml&location='''+str(gps)+'''&key='''+key+'''&radius='''+str(radius)+'''&extensions=all&batch=false&roadlevel='''+str(roadlevel)
    #print(url)
    r=requests.get(url)
    tree=ET.XML(r.text)
    #response=tree.find('response')
    rego=tree.find('regeocode')
    #rego_test=tree.find('regeocode').text
    #解析roads
    streets={}
    roads=rego.find('roads')
    if roads is not None:
        road=roads.findall('road')
        if road is not None:
            for ro in road:
                streets[ro.find('name').text]=float(ro.find('distance').text)
    #解析roadinters
    roadinters=rego.find('roadinters')
    inters=[]
    roadinter=roadinters.find('roadinter')
    if roadinter is None:
        inters.append('NaN')
        inters.append('NaN')
        inters.append('NaN')
        inters.append('NaN')
    else:
        inters.append(float(roadinter.find('distance').text))
        inters.append(roadinter.find('first_name').text)
        inters.append(roadinter.find('second_name').text)
        inters.append(roadinter.find('location').text)
    #解析street
    address=rego.find('addressComponent')
    streetNumber=address.find('streetNumber')
    streetName=streetNumber.find('street').text
    if streetName is not None:
        if streetName not in streets.keys():
            streets[streetName]=float(streetNumber.find('distance').text)
    return streets,inters

def get_key_by_value(dicti,value):
    '''
    get the key whose value== value in the dictionary
    dicti: the dictionary we will search 
    value； the value we want to search
    key: the key whose value==value (may have different length)
    '''
    key=[]
    for k,v in dicti.items():
        if v==value:
            key.append(k)
    if len(key)==0:
        print("no")
        #print("there is no value is:"+value)
    elif len(key)>1:
        print("there are more than one key's value is:"+value)
        print(key)
    else:
        print("*")
        #print("there is noly one key's value is； "+value)
    return key


def get_check_repeat_gps(gpsdir,enc='utf-8',save=True):
    '''
    1、read gps from csv
    2、check  and delete the repeat gps
    3、rewrite the csv(when the save ==True)
    gpsdir: The dir of gpscsv,eg:D:\\XM_横向项目\\数据中心建设\\gps20181026.csv
    enc: The encoding of csv,eg:utf-8
    '''
    time_gps={}
    time=[]
    jing=[]
    wei=[]
    gps=[]
    with open(gpsdir,encoding=enc)as f:
        reader=csv.reader(f)
        for row in reader:
            time.append(row[0])
            jing.append(row[2])
            wei.append(row[1])
            gps.append(row[2]+','+row[1])
            time_gps[row[0]]=row[2]+','+row[1]
    #find the repeat gps, save the key(timw) in repeat_time
    tmp_num=len(time_gps)
    repeat_key=[]
    for k,v in time_gps.items():
        tmp_repeat=[]
        for kk,vv in time_gps.items():
            if vv==v:
                tmp_repeat.append(kk)
        if len(tmp_repeat)>1:
            repeat_key.append(tmp_repeat)
    #delete the repeat gps
    for tmp in repeat_key:
        for i in range(1,len(tmp)):
            pop_obj=time_gps.pop(tmp[i],'404')
    new_num=len(time_gps)
    print('There are '+str(tmp_num-new_num)+' of '+str(tmp_num)+' location are repeat')
    #rewite the time_gps to csv
    if save==True:
        (filepath,tempfilename) = os.path.split(gpsdir)
        (shotname,extension) = os.path.splitext(tempfilename)
        new_dir=filepath+'\\'+shotname+'_new'+extension
        pd.DataFrame(time_gps,index=[0]).T.to_csv(new_dir,header=False)
        print(new_dir+'  success')
    #change the gps,time,jing,wei
    time=[]
    jing=[]
    wei=[]
    gps=[]
    for k,v in time_gps.items():
        time.append(k)
        gps.append(v)
        jing.append(v.split(',')[0])
        wei.append(v.split(',')[1])
    return time_gps,gps,time,jing,wei

def getAllGPS(gpsdir,enc='utf-8'):
    '''
    read gps from csv
    gpsdir: The dir of gpscsv, eg:D:\\XM_横向项目\\数据中心建设\\gps20181026.csv
    enc:The encoding of csv,eg:utf-8
    '''
    time_gps={}
    time=[]
    jing=[]
    wei=[]
    gps=[]
    with open(gpsdir,encoding=enc)as f:
        reader=csv.reader(f)
        for row in reader:
            time.append(row[0])
            jing.append(row[2])
            wei.append(row[1])
            gps.append(row[2]+','+row[1])
            time_gps[row[0]]=row[2]+','+row[1]
    return time_gps,gps,time,jing,wei
    
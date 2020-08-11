# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 09:16:30 2020

@author: lenovo
"""


import os
import shutil
import xml.etree.ElementTree as ET

def parse_rec(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    file_name=tree.find('filename').text
    size_f=tree.find('size')
    w_f=int(size_f.find('width').text)
    h_f=int(size_f.find('height').text)
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['filename']=file_name
        obj_struct['name'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(float(bbox.find('xmin').text)),
                              int(float(bbox.find('ymin').text)),
                              int(float(bbox.find('xmax').text)),
                              int(float(bbox.find('ymax').text))]
        obj_struct['w_f'] = w_f
        obj_struct['h_f'] = h_f
        objects.append(obj_struct)

    return objects
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
files=os.listdir(r'H:\WaiHuan_20200624\WaiHuan_20200624\WaiHuan_20200624_input_anno')
for file in files:
    filename=os.path.join(r'H:\WaiHuan_20200624\WaiHuan_20200624\WaiHuan_20200624_input_anno',file)
    objects=parse_rec(filename)
    txtname=os.path.join(r'H:\WaiHuan_20200624\WaiHuan_20200624\labels',os.path.splitext(file)[0]+'.txt')
    #creat txt file
    for obj in objects:
        name=class_name[obj['name']]
        x,y,w,h=obj['bbox']
        h_f=obj['h_f']
        w_f=obj['w_f']
        x_cen=(x+w/2)/w_f
        y_cen=(y+h/2)/h_f
        w=w/w_f
        h=h/h_f
        item=str(name)+' '+str(x_cen)+' '+str(y_cen)+' '+str(w)+' '+str(h)
        with open(txtname,'a') as f:
            f.writelines(item)
            f.writelines('\n')        
    #move images to new_path
    img_old=os.path.join(r'H:\WaiHuan_20200624\WaiHuan_20200624\WaiHuan_20200624_input_imgs_neg',os.path.splitext(file)[0]+'.jpg')
    #img_new=os.path.join(r'H:\WaiHuan_20200624\WaiHuan_20200624\JPEGImages',os.path.splitext(file)[0]+'.jpg')
    shutil.move(img_old,r'H:\WaiHuan_20200624\WaiHuan_20200624\JPEGImages')
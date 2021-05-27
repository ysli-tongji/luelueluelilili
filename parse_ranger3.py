# -*- coding: utf-8 -*-
"""
Created on Tue May 11 09:49:00 2021

@author: Eason
"""

import struct
import numpy as np
from tqdm import tqdm
import xml.etree.ElementTree as ET
import os
# from matplotlib import pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from typing import Union

import pyecharts.options as opts
from pyecharts.charts import Surface3D

def parse_xml (xml_path):
    base_infor = {}
    tree = ET.parse(xml_path)
    component = tree.find('component')
    for sub in component.findall('subcomponent'):
        if sub.attrib['name'] == 'Range':
            if sub.attrib['valuetype'] != 'FLOAT':
                print(os.path.basename(xml_path) + '未标定')
            paramters = sub.findall('parameter')
            for item in paramters:
                if item.attrib['name'] == 'size':
                    base_infor['range_size'] = int(item.text)
                if item.attrib['name'] == 'width':
                    base_infor['range_width'] = int(item.text)
            base_infor['range_n_bytes'] = int(base_infor['range_size'] / base_infor['range_width'])
        if sub.attrib['name'] == 'Intensity':
            paramters = sub.findall('parameter')
            for item in paramters:
                if item.attrib['name'] == 'size':
                    base_infor['intensity_size'] = int(item.text)
                if item.attrib['name'] == 'width':
                    base_infor['intensity_width'] = int(item.text)
            base_infor['intensity_n_bytes'] = int(base_infor['intensity_size'] / base_infor['intensity_width'])
    if base_infor['intensity_width'] != base_infor['range_width']:
        print('数据宽度不等')
    return base_infor

def parse_dat (dat_path,xml_path):
    base_infor = parse_xml(xml_path)
    range_data = []
    intensity_data = []
    with open(dat_path,'rb') as f:
        tmp = f.read()
        total_bytes = f.tell()
        cols = base_infor['intensity_width']
        rows = total_bytes/((base_infor['intensity_n_bytes'] + base_infor['range_n_bytes']) * cols)
        rows = int(rows)
        f.seek(0)
        for i in range(cols*rows):
            bytes_read = f.read(base_infor['range_n_bytes'])
            text_bytes = struct.unpack('f',bytes_read)[0]
            range_data.append(text_bytes)
        for i in range(cols*rows):
            bytes_read = f.read(base_infor['intensity_n_bytes'])
            text_bytes = struct.unpack('f',bytes_read)[0]
            intensity_data.append(text_bytes)
    range_data = np.array(range_data).reshape(rows,cols)
    intensity_data = np.array(intensity_data).reshape(rows,cols)

    return range_data,intensity_data

def plot_3d_surface(range_data,intensity_data):
    rows,cols = range_data.shape
    fig = plt.figure()
    ax = Axes3D(fig)
    # 分别生成x、y坐标数据
    xcord = np.arange(0, cols, 1)
    ycord = np.arange(0, rows, 1)
    
    # 将坐标向量转换成坐标矩阵(vectors -> matrices)
    xcord, ycord = np.meshgrid(xcord, ycord)
    
    # 绘制曲面图
    ax.plot_surface(xcord, ycord, range_data, rstride=1, cstride=1, cmap='rainbow')
    plt.savefig(r'C:\Users\Eason\Desktop\test.jpg')
    # plt.show()
    
    
xml_path = r'C:\Users\Eason\Desktop\210429-sample\0429-1-biaoding.xml'
dat_path = r'C:\Users\Eason\Desktop\210429-sample\0429-1-biaoding.dat'

range_data,intensity_data = parse_dat(dat_path,xml_path)


np.savetxt(r'C:\Users\Eason\Desktop\210429-sample\range_data.csv', range_data, delimiter=",")
np.savetxt(r'C:\Users\Eason\Desktop\210429-sample\intensity_data.csv', intensity_data, delimiter=",")


def surface3d_data(range_data):
    rows,cols = range_data.shape
    for t0 in range(500):
        y = t0
        for t1 in range(500):
            x = t1
            z = range_data[y,x]
            yield [x, y, z]

(
    Surface3D(init_opts=opts.InitOpts(width="1600px", height="800px"))
    .add(
        series_name="",
        shading="color",
        data=list(surface3d_data(range_data)),
        xaxis3d_opts=opts.Axis3DOpts(type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=100, height=40, depth=100),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            dimension=2,
            max_=50,
            min_=40,
            range_color=[
'#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026',
            ],
        )
    )
    .render("surface_wave.html")
)


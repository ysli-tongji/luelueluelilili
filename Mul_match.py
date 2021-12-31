# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 14:11:19 2021

@author: Eason
"""
#%%
 # 加载包 
import pandas as pd
import os
import json
from math import radians,sin,cos,asin,sqrt
from tqdm import tqdm
import numpy as np
import math
from sklearn.cluster import KMeans
import urllib
import urllib.request
from tqdm import tqdm
# from match_pairs import feature_match

#%%

def create_record(value):
    
    base_path = r'F:\TRB-2021\Chengtou_data\Records_without'
    json_name = str(value['longitude_84']) + '_' + str(value['latitude_84']) + '.json'
    # print(json_name)
    tmp={
    'image_url':value['image_url'],
    'distress':1,
    'bbox':value['bbox'],
    'detect_info':value['detect_info'],
    'event_type_name':str(value['event_type_name']),
    'collect_time':value['collect_time'],
    'GPS':[value['longitude_84'],value['latitude_84']],
    'loc_area':[value['loc_area'],value['loc_location']],
    'AZIMUTH':value['azimuth'],
    'detect_conf':value['detect_conf']
    }
    
    dirt = {
        'Location':
            {'LATITUDE':value['latitude_84'],'LONGITUDE':value['longitude_84']},
        'Records':
            [tmp]
            }
        
    with open(os.path.join(base_path,json_name),'w',encoding='utf-8') as f:
        json.dump(dirt,f,ensure_ascii=False,indent=4)
    
    return json_name

def get_geo_mid(data):
    new_lat = new_lon = 0
    coord_num = len(data)

    for coord in data:
        lat = coord[1]
        lon = coord[0]

        new_lat += lat
        new_lon += lon

    new_lat /= coord_num
    new_lon /= coord_num

    return new_lat, new_lon


def append_record (json_name,value):
    base_path = r'F:\TRB-2021\Chengtou_data\Records_without'
    json_path = os.path.join(base_path,json_name)
    if os.path.exists(json_path):   
        tmp={
        'image_url':value['image_url'],
        'distress':1,
        'bbox':value['bbox'],
        'detect_info':value['detect_info'],
        'event_type_name':str(value['event_type_name']),
        'collect_time':value['collect_time'],
        'GPS':[value['longitude_84'],value['latitude_84']],
        'loc_area':[value['loc_area'],value['loc_location']],
        'AZIMUTH':value['azimuth'],
        'detect_conf':value['detect_conf']
        }
        # 增加一个record
        with open(json_path,encoding='utf-8') as f:
            dirt = json.load(f)
            dirt['Records'].append(tmp)
            # 修改json的GPS中心
            gps_data = [record['GPS'] for record in dirt['Records']]
            new_lat, new_lon = get_geo_mid(gps_data)
            dirt['Location']['LATITUDE']=new_lat
            dirt['Location']['LONGITUDE']=new_lon
            
        new_name = str(dirt['Location']['LONGITUDE']) + '_' + str(dirt['Location']['LATITUDE']) + '.json'
        
        with open(json_path,'w',encoding='utf-8') as f:
            json.dump(dirt, f,ensure_ascii=False,indent=4)
    
        # 改名字
        os.rename(json_path,os.path.join(base_path, new_name))
    return json_name
            
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000     

def angle_to_vector(azimuth):
    r_azimuth = math.radians(azimuth)
    d_x = math.sin(r_azimuth)
    d_y = math.cos(r_azimuth)
    o_x = 0.0
    o_y = 0.0
    
    return o_x,o_y,d_x,d_y

def judge_clu(clu_data):
    clu_flag = True
    if len(clu_data)==1:
        clu_flag = False
        clu_data = np.column_stack((clu_data,0))
        return clu_flag,clu_data
    SSE=[]
    for clu_k in range(1,3):
        clf = KMeans(n_clusters = clu_k)
        clf.fit(clu_data[:,:2])        
        sse_item = clf.inertia_
        SSE.append(sse_item/len(clu_data))
    if SSE[1] == 0:
        ratio = 0.0000001
    else:
        ratio = SSE[0]/SSE[1]
    # 聚类筛选条件
    if ratio > 5:
        clf = KMeans(n_clusters = 1)
        clf.fit(clu_data[:,:2])
        distance = clf.fit_transform(clu_data[:,:2]) 
        if max(distance) < 1:
            clu_flag = False
        else:
            clu_flag = True
    else:
        clf = KMeans(n_clusters = 1)
        clf.fit(clu_data[:,:2])
        distance = clf.fit_transform(clu_data[:,:2]) 
        if max(distance) > 1:
            clu_flag = True
        else:
            clu_flag = False
    if clu_flag:
        # 当k=0时，SSE较大，且随着K的增大聚类效果突出，需要聚类
        clf = KMeans(n_clusters=2)
        clf.fit(clu_data[:,:2])
        clu_data = np.column_stack((clu_data,clf.labels_.T))
        
        return clu_flag,clu_data
    else:
        # 不需要聚类，直接输出原始数据，标签Label统一设为0
        labels = np.zeros((len(clu_data),1),dtype=np.float32)
        clu_data = np.column_stack((clu_data,labels))
        clu_flag = False
            
        return clu_flag,clu_data
#%%
#读取数据
path_1 = r'F:\TRB-2021\chengtou_data\rec_detect_results_info_device33(before0705).csv'
data_1 = pd.read_csv(path_1)
path_2 = r'F:\TRB-2021\chengtou_data\rec_detect_results_info_device33(after0705).csv'
data_2 = pd.read_csv(path_2)
data= data_1.append(data_2)
data.reset_index(drop=True, inplace=True)


csv_data = data
#%%
# GPS初筛

for i in tqdm(csv_data.index):
    if csv_data.loc[i,'event_type_name'] == '井盖' or csv_data.loc[i,'event_type_name'] == '伸缩接缝':
        continue
    file_list = os.listdir(r'F:\TRB-2021\Chengtou_data\Records_without') 
    flag = False
    for old_file in file_list:
        lon_old = float(old_file.split('.json')[0].split('_')[0])
        lat_old = float(old_file.split('.json')[0].split('_')[1])
        lon_new = float(csv_data.loc[i,'longitude_84'])
        lat_new = float(csv_data.loc[i,'latitude_84'])
        distance = haversine(lon_old,lat_old,lon_new,lat_new)
        if distance < 13:
            flag = True
            json_name = old_file
            break
    if flag:
        append_record(json_name,csv_data.loc[i])
        # print('添加第 '+str(i)+' 条数据到'+json_name)
    else:
        json_name = create_record(csv_data.loc[i])
        # print('新增： '+json_name)
    with open(r'F:\TRB-2021\Chengtou_data\records_num.txt','a') as f:
        f.writelines(str(len(file_list)))
        f.writelines('\n')

#%%
# 在完成GPS初筛之后，对已生成的json records进行方向角复筛

# 遍历已有的GPS初筛的Records，进行方向角复筛选
records_path = r'F:\TRB-2021\Chengtou_data\Records'
new_records_path = r'F:\TRB-2021\Chengtou_data\Records_GPS_Azimuth'
records_files = os.listdir(records_path)
no_change =0
for records_file in tqdm(records_files):
    file_path = os.path.join(records_path,records_file)
    with open(file_path,encoding='utf-8') as f:
        data = json.load(f)
    records = data['Records']
    num_record = len(records)
    #提取records中的方向角信息，创建聚类数组
    clu_data = np.zeros((num_record,3),dtype=np.float32)
    for i in range(num_record):
        o_x,o_y,d_x,d_y = angle_to_vector(records[i]['AZIMUTH'])
        clu_data[i,0] = d_x
        clu_data[i,1] = d_y
        clu_data[i,2] = i
    # 数据分析发现大多数方位角为0，属于异常值，为减少异常值影响，去除（0,1）的坐标点
    clu_data = np.delete(clu_data, np.where(clu_data[:,1]==1), axis = 0)
    if len(clu_data) ==0:
        # 此时的records的json文件无需修改，直接另存
        with open(os.path.join(new_records_path,records_file),'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
        no_change += 1
        continue
    clu_flag,clu_data = judge_clu(clu_data)
    if clu_flag == False:
        with open(os.path.join(new_records_path,records_file),'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
        no_change += 1
        continue
    else:
        # 此时该json文件中存在两个方向的记录，需要进行聚类，原始json文件中的records需要进行拆分
        # 先根据已有的数据，新增一个record
        new_records_list = clu_data[clu_data[:,3]==1]
        new_records = []
        for index in new_records_list[:,2]:
            new_records.append(records[int(index)])
        gps = new_records[0]['GPS']   
        dirt = {
            'Location':
                {'LATITUDE':gps[1],'LONGITUDE':gps[0]},
            'Records':
                new_records
                }
        json_name = str(gps[0]) + '_' + str(gps[1]) + '.json'
        
        with open(os.path.join(new_records_path,json_name),'w',encoding='utf-8') as f:
            json.dump(dirt,f,ensure_ascii=False,indent=4)
        # print('拆分并写入文件：'+json_name)
        # 然后根据聚类结果，修改现有的data文件，写入file_path中
        del_list = clu_data[clu_data[:,3]==0]
        retain_records = []
        for index in del_list[:,2]:
            retain_records.append(records[int(index)])
        dirt = {
            'Location':data['Location'],
            'Records':retain_records
            }
        
        with open(os.path.join(new_records_path,records_file),'w',encoding='utf-8') as f:
            json.dump(dirt,f,ensure_ascii=False,indent=4)
        # print('修改并写入文件：'+records_file)        


#%%
# 下载聚类后的图片
def change_url(url):
    cache_url = {}
    url = url.split('/')[-1]
    device = url.split('_')[0][0:6]
    date = url.split('_')[0][7:]
    hour = url.split('_')[1].split('-')[0]
    minute = url.split('_')[1].split('-')[1]
    new_url = 'http://47.116.78.108:8071/tly_realtime/' + str(device) + '/front/' + str(date) +'/'+hour+'/'+minute+'/'+url
    cache_url['device'] = device
    cache_url['date'] = date
    cache_url['hour'] = hour
    cache_url['minute'] = minute
    
    return new_url,cache_url

def download_img(url,img_path):
    # img_path = r'G:\SODIC\train\train\xuhui_det_data\images'
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        get_img = response.read()
        name = url.split('/')[-1]
        img_name = os.path.join(img_path,name)
        with open(img_name,'wb') as fp:
            fp.write(get_img)
            #print('图片下载完成')
    except:
        with open(r'F:\TRB-2021\download_error.txt', 'a') as f:
            f.writelines(url)
            f.writelines('\n')
        print(url)
        
        

records_path = r'F:\TRB-2021\Records_GPS_Azimuth'
record_files = os.listdir(records_path)
for record_file in tqdm(record_files):
    record_path = os.path.join(records_path,record_file)
    with open(record_path,encoding='utf-8') as f:
        data = json.load(f)
    records = data['Records']
    # 一个record文件对应一个图片文件夹
    img_path = os.path.join(r'F:\TRB-2021\Images_GPS_Azimuth',record_file.split('.json')[0])
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    # 拉取标注url的列表
    url_list = []
    new_url_list = []
    for record in records:
        url = record['image_url']
        if url not in url_list:
            url_list.append(url)
            new_url,cache_url = change_url(url)
            new_url_list.append(new_url)
    length = len(new_url_list)
    for i in range(length):
        download_img(new_url_list[i],img_path) 
        print('Download: '+str(i)+'/'+str(length))
        
    


#%%
# 完成方向角复筛之后，进行特征匹配的终筛

def judge_feature_matching(json_path,viz_flag=False):
    with open(json_path) as f:
        data = json.load(f)
    records = data['Records']
    url_list =[]
    for record in records:
        if record['image_url'] not in url_list:
            url_list.append(record['image_url'].split('/')[-1])
    # 建立匹配对，输入特征匹配网络进行匹配（匹配对为一个list，每一个元素是长为2的list，分别是匹配的两个图片名
    pairs_list = []
    for url in url_list:
        pairs_list.append([url_list[0],url])
    # 待匹配图片的基础路径
    img_dir = os.path.join(r'E:\Image_matching\Timeline-matching\img_download',os.path.basename(json_path).split('.json')[0])
    feature_match_results = feature_match(pairs_list,img_dir,viz_flag)
    
    
    # with open(r'E:\Image_matching\Timeline-matching\pairs_list.txt','a') as f:       
    #     for url in url_list:
    #         item = url_list[0]+' '+url
    #         f.writelines(item)
    #         f.writelines('\n')
records_path = r'E:\Image_matching\Timeline-matching\Records_kmeans_azimuth'
records_files = os.listdir(records_path)
img_base_path = r'E:\Image_matching\Timeline-matching\img_download'

for file in records_files:
    json_file = os.path.join(records_path,file)
    url_list =[]
    with open(json_file) as f:
        data = json.load(f)
    records = data['Records']
    img_path = os.path.join(img_base_path,file.split('.json')[0])
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    for record in records:
        if record['image_url'] not in url_list:
            url_list.append(record['image_url'])
            download_img(record['image_url'],img_path)        
            
            
record_file =r'E:\Image_matching\Timeline-matching\Records_kmeans_azimuth\121.425386_31.15352.json'   
with open(record_file) as f:
    data = json.load(f)
records = data['Records']
url_list =[]
for record in records:
    if record['image_url'] not in url_list:
        url_list.append(record['image_url'].split('/')[-1])
with open(r'E:\Image_matching\Timeline-matching\pairs_list.txt','a') as f:
    
    for url in url_list:
        item = url_list[0]+' '+url
        f.writelines(item)
        f.writelines('\n')

results = feature_match(r'E:\Image_matching\Timeline-matching\pairs_list.txt',r'E:\Image_matching\Timeline-matching\img_download\121.425386_31.15352',viz_flag=True)
for result in results:
    print(np.sum(result['matches']>-1))
        


second_day = csv_data[csv_data['date']=='2020/11/04']     
file_list = os.listdir(r'E:\Image_matching\Timeline-matching\Records') 
for i in second_day.index:

    flag = False
    for old_file in file_list:
        lon_old = float(old_file.split('.json')[0].split('_')[0])
        lat_old = float(old_file.split('.json')[0].split('_')[1])
        lon_new = float(second_day.loc[i,'LONGITUDE'])
        lat_new = float(second_day.loc[i,'LATITUDE'])
        distance = haversine(lon_old,lat_old,lon_new,lat_new)
        if distance < 15:
            flag = True
            json_name = old_file
            break
    if flag:
        append_record(json_name,second_day.loc[i])
        print('添加第 '+str(i)+' 条数据到'+json_name)
    else:
        json_name = create_record(second_day.loc[i])
        print('新增： '+json_name)
      
total_gps = []
for gps,value in gps_collect:
    total_gps.append(gps)
    if len(value) >1:
        print(str(gps)+str(len(value)))
for index,value in first_day.iterrows():
    create_record(value)

  
    
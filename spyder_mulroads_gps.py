# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 10:22:40 2021

@author: lenovo
"""

import requests
import re
import pandas as pd
from tqdm import tqdm
import time

path = r'C:\Users\lenovo\Desktop\linggang_roads.xlsx'
roads_data = pd.read_excel(path)

total_gps = pd.DataFrame(columns={'lng','lat','lng_lat','id','road'})
for index in roads_data.index:
    time.sleep(30)
    key = roads_data.iloc[index,0]
    print( time.ctime() + key)
    
    

    url = 'https://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12.73&city=310000&geoobj=121.21449%7C31.228426%7C121.314108%7C31.326332&keywords={key}'.format(key=key)
    myheaders = {'authority': 'ditu.amap.com',
    'method': 'GET',
    'path': '/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=11.62&city=310000&geoobj=121.154726%7C31.18119%7C121.369094%7C31.391865&keywords=%E4%B8%8A%E6%B5%B7%E5%B8%82%E7%BB%BF%E8%8B%91%E8%B7%AF',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'amapuuid': 'f284e71d-2cd4-4acb-aca3-9290a385a1ed',
    'cookie': 'UM_distinctid=178cfd97963332-095489eb9430cd-e323069-144000-178cfd97964242; cna=1az9GL643QcCAW+7Huro5G2r; xlly_s=1; guid=6590-71d6-5490-e255; CNZZDATA1255626299=400336097-1618390959-https%253A%252F%252Fcn.bing.com%252F%7C1618465945; x5sec=7b22617365727665723b32223a223935383031373630633365363131666464343166363230646237386366633062434c363233344d47454c37697638624c2f4e75677377456f416a447675594159227d; tfstk=cKMABdNjGUYmQZE-YjdlfkqZLqL1aKIYSiaOBndYHb4Nui6lUsbqKvu8bIZNk8KR.; l=eBgj_Z57jwmlWRxFBO5Z-urza77OyIdfG5VzaNbMiInca1lpOFsOzNCQrGjO5dtjgtCUbI-zC__QeREHJQUdgtrsywzdDt9xnxvO.; isg=BD09iFv3ASs3m6VG3mEPESt5TJk32nEsX9JPQ_-DyRTDNllo-CoR_Cmg4Gpwj4nk',
    'referer': 'https://ditu.amap.com/search?query=%E6%9B%B9%E5%AE%89%E5%85%AC%E8%B7%AF&city=310000&geoobj=121.317443%7C30.797754%7C122.24865%7C31.713199&zoom=9.5',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'x-csrf-token': 'null',
    'x-requested-with': 'XMLHttpRequest',
      }
    r=requests.get(url,headers=myheaders).text
    pattern = re.compile(r'"value":"([\d,_.|]*)","name":"roadaoi"')
    res=re.findall(pattern,r)[0]
    res=res.split('|')
    data=pd.DataFrame(columns={'lng','lat','lng_lat','id','road'})
    for i in tqdm(range(len(res))):
        temp=res[i].split('_')
        for j in temp:
            data.loc[len(data)]=[j.split(',')[0],j.split(',')[1],j,i,key]
    
    total_gps = total_gps.append(data)
    print(key+'over')


    
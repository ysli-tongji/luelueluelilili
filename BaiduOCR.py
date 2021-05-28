# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 20:47:35 2020

@author: lenovo
"""

import sys
import json
import base64
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus


# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'cG47kSeV6RhghubuUIvjPNpi'

SECRET_KEY = '24YyR1GnhxcN2MCOAn05KkDiCkfCulk6'


OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)    
    result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    读取文件
"""
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()       
        result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)

if __name__ == '__main__':

    # 获取access token
    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    text = ""

    # 读取书籍页面图片
    file_content = read_file(r'C:\Users\lenovo\test.jpg')

    # 调用文字识别服务
    result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))

    # 解析返回结果
    result_json = json.loads(result)
    for words_result in result_json["words_result"]:
        text = text + words_result["words"]

    # 打印文字
    print(text)
    
   
import requests 
import base64

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=cG47kSeV6RhghubuUIvjPNpi&client_secret=24YyR1GnhxcN2MCOAn05KkDiCkfCulk6'
response = requests.get(host)
if response:
    token=response.json()['access_token']


'''
表格文字识别(同步接口)
'''
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/form"
# 二进制方式打开图片文件
f = open(r'C:\Users\lenovo\Desktop\test.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
request_url = request_url + "?access_token=" + token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())
    
    

request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
# 二进制方式打开图片文件
f = open(r'C:\Users\lenovo\Desktop\test.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = token
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    result=response.json()
    print (response.json())

excle_url="https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result"+ "?access_token=" + access_token
parameters={'request_id':result['result'][0]['request_id']}
response_excel=requests.post(excle_url,data=parameters,headers=headers)
if response_excel:
    excel_result=response_excel.json()
    print(excel_result)
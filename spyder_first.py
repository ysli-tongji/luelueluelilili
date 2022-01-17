# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 10:39:30 2021

@author: Eason
"""

import urllib.request 
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import time

with open(r'C:\Users\Eason\Desktop\urls.txt','r') as f:
    lines = f.readlines()
content = []
for line in tqdm(lines):
    time.sleep(5)
    url = line
    response = urllib.request.urlopen(url)
    print(response.getcode())
    html = response.read()
    soup = BeautifulSoup(html)
    #soup.find_all('div', {'class': re.compile('view TRS_UEDITOR trs_paper_default')})
    div = soup.find_all('div', {'class': re.compile('view TRS_UEDITOR trs_paper_default')})
    p_list = div[0].find_all('p')
    test ='Header:'
    test += soup.find_all('h1')[0].text
    test +='------'
    for p in p_list:
        
        test += p.text
    content.append(test)
    

url_total = 'https://www.mot.gov.cn/2021zhengcejd/'
response = urllib.request.urlopen(url_total)
print(response.getcode())
html = response.read()
soup = BeautifulSoup(html)
links = soup.find_all('a')
urls = []
for link in links:
    urls.append(link.get('href'))
    
url = r'https://www.mot.gov.cn/2021zhengcejd/nongcunglsj_jd/index.html'
response = urllib.request.urlopen(url)
print(response.getcode())
html = response.read()
soup = BeautifulSoup(html)
div = soup.find_all('div', {'class': 'view TRS_UEDITOR trs_paper_default'})
p_list = div[0].find_all('p')
test ='Header:'
test += soup.find_all('h1')[0].text
test +='------'
for p in p_list:
    
    test += p.text

with open(r'C:\Users\Eason\Desktop\ZC.txt','a',encoding='utf-8') as f:
    for cont in content:
        f.writelines(cont)
        f.writelines('\n')

with open(r'C:\Users\Eason\Desktop\ZC_noline.txt','a',encoding='utf-8') as f:
    for cont in content:
        f.writelines(cont)

import jieba
txt = open(r'C:\Users\Eason\Desktop\ZC_noline.txt', 'r', encoding='utf-8').read()
words = jieba.lcut(txt)
import pandas as pd
result = pd.value_counts(words)
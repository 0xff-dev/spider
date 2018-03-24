#!/usr/bin/env python
# coding=utf-8

import os
import urllib.request
import requests
from random import choice
from bs4 import BeautifulSoup
from config.config import *


HEADERS = {
    'User-Agent': USER_AGENT,
    'Referer': BASE_URL,
    }


def get_page_urls_name(num):
    url = BASE_URL if num == 1 else BASE_URL+'/home/'+str(num)
    resp = requests.get(url, headers=HEADERS).content
    soup = BeautifulSoup(resp, 'html.parser')
    tag_a = soup.select('li > a')
    page_urls = [(tag['href'], tag.img['alt']) for tag in tag_a]
    return page_urls


def get_all_image(page_urls):
    for url, name in page_urls:
        print ('请求的url:  '+url)
        resp = requests.get(url, headers=HEADERS).content
        soup = BeautifulSoup(resp, 'html.parser')
        image_num = int(soup.select('#page > a')[-2].string)
        
        # 创建一个存储目录
        BASE_DIR = './images/'+name
        try:
            os.mkdir(BASE_DIR)
        except os.error as e:
            pass

        for index in range(1, image_num+1):
            image_url = url+'/'+str(index)
            resp = requests.get(image_url, headers=HEADERS).content
            sp = BeautifulSoup(resp, 'html.parser')
            image_url_tag = sp.select('#content > a > img')
            detail_url = image_url_tag[0]['src']
            
            filename = BASE_DIR+'/'+name+str(index)+'.jpg'
            print ('Downloading -----  '+filename+'    %s/%s' % (index, image_num))
            with open(filename, 'wb') as fp:
                fp.write(requests.get(detail_url, headers=HEADERS, proxies=choice(PROXYS)).content)
for i in range(1, 3):
    get_all_image(get_page_urls_name(i))


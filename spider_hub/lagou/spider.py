#!/usr/bin/env python
# coding=utf-8

import json
import sys
import asyncio
from time import sleep
import multiprocessing as mp
import requests
from random import choice

from proxy import proxies
from judge_ip import judge
from model import DBManager
from config import BASE_URL, HEADERS


kd = sys.argv[1]
db = DBManager(kd)


def login(username, password):
    login_url = 'https://passport.lagou.com/login/login.json'
    pass


def crawl(url: str, _data, db):
    sleep(1)
    resp = requests.post(url,
                        data=_data,
                        headers=HEADERS)
    results = resp.json().get('content').get('positionResult').get('result')
    for result in results:
        print(result)
        db.insert_one({'companyFullName': result.get('companyFullName'),
                       'positionName': result.get('positionName'),
                       'salary': result.get('salary'),
                       'workYear': result.get('workYear')})


for i in range(1, 6):
    crawl(BASE_URL.format(city="北京"), {'first': True, 'pn': i, 'kd': kd}, db)

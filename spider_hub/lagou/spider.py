#!/usr/bin/env python
# coding=utf-8

import json
import sys
import asyncio
import time
from time import sleep
import multiprocessing as mp
import requests
import gevent
from gevent.event import Event
from random import choice

from proxy import proxies
from judge_ip import judge
from model import DBManager
from config import BASE_URL, HEADERS


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


if __name__ == '__main__':

    start = time.time()
    city = sys.argv[2]
    kd = sys.argv[1]
    db = DBManager(kd)
    url = BASE_URL.format(city=city)
    pages = sys.argv[3]
    tasks = []
    for index in range(1, int(pages)+1):
        if index == 1:
            _data = {'firsrt': True, 'pn': index, 'kd': kd}
        else:
            _data = {'first': False, 'pn': index, 'kd': kd}
        tasks.append(gevent.spawn(crawl, url, _data, db))
    gevent.joinall(tasks)
    print('Exec {}'.format(time.time()-start))

#!/usr/bin/env python
# coding=utf-8

import requests
from config import HEADERS
from proxy import proxies

def judge(proxy) -> bool:
    resp = requests.get('https://www.lagou.com', 
                        headers=HEADERS,
                        proxies={'http': proxy})
    if resp.status_code == 200:
        return True
    return False

print(judge('190.2.144.104:1080'))


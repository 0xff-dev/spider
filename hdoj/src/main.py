#!/usr/bin/env python
# coding=utf-8

import time
from datetime import datetime

import gevent
from selenium import webdriver
from lxml import etree

from models import DBManager, User


BASE_URL = 'http://acm.hdu.edu.cn/'
xpath = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/p[3]'
REQUEST_URL = 'http://acm.hdu.edu.cn/userstatus.php?user={user}'


brower = webdriver.PhantomJS()
db = DBManager()


def crawl_single_problem(p_id, url, _data: dict, db: DBManager):
    """
    return: date 2018-01-01 define
    """
    brower.get(url)
    lxml_html = etree.HTML(brower.page_source)
    xpath = '//*[@id="fixed_table"]/table/tbody/tr[2]/td[2]'
    date = lxml_html.xpath(xpath)[0].text.split(' ')[0]
    print(date)
    # 获取提交的时间
    if date not in _data['date_ps'].keys():
        _data['date_ps'][date] = []
    _data['date_ps'][date].append(p_id)
    #db.insert(_data)
    print(_data)


def crawl(user, db):
    """
    date: 2018-01-01
    """
    url = REQUEST_URL.format(user=user)
    today = datetime.now().strftime("%Y-%m-%d")
    brower.get(url)
    page_source = brower.page_source
    lxml_html = etree.HTML(page_source)
    tag_p = lxml_html.xpath(xpath)
    print(tag_p)
    print(tag_p[0].get('align'))
    tag_as = tag_p[0].findall('.//a')
    #user = User(user, " ")
    _data = {"user": user, "nick_name": " ", "date_ps": {}}
    tasks = []
    for tag_a in tag_as:
        problem_id = tag_a.get('href').split('&')[1][4:]
        # 抛出id, +问题的url
        tasks.append(gevent.spawn(crawl_single_problem(problem_id,
                                  BASE_URL+tag_a.get('href'),
                                  _data, db)))
    gevent.joinall(tasks)


if __name__ == '__main__':
    # give me user list [(user, nick_name)]
    crawl('DayDayUp', db)

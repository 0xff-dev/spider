#!/usr/bin/env python
# coding=utf-8

import re
import requests
import pytesseract
from datetime import datetime
from bs4 import BeautifulSoup
from model.mongoDb import DBManager
from num_identify_code.identify_code import get_code_cookies
from config.cs_config import *


def login(WebUserNO: str, Password: str) -> None:
    while True:
        try:
            captcha, cookies = get_code_cookies(BASE_URL+CAPTCHA_METHOD)
            login_data = {
                    'WebUserNO': WebUserNO,
                    'Password': Password,
                    'Agnomen': int(captcha)
                }
            login_request = requests.post(BASE_URL+LOGIN_METHOD,
                                          headers=HEADERS, data=login_data,
                                          cookies=cookies)
            res_data = login_request.content.decode('GBK')
            if '正确的附加码' in res_data:
                print ('验证码错误')
            elif '错误的用户名' in res_data:
                print ('用户名或者密码错误')
            elif '欢迎您登录' in res_data:
                print ('All right')
                return cookies
        except Exception as e:
            print ('There are some wrong {}'.format(e))


def get_term() -> int:
    first_term_months = set([i for i in range(3, 9)])
    second_term_months = set([i for i in range(1, 13)]) - first_term_months
    date = datetime.now()
    year, month = date.year, date.month
    year -= 2010
    if month in second_term_months:
        return year*2+2
    else:
        return year*2-1


def download_class_info(_class_id: str) -> dict:
    cookies = login(TEACHER_ID, TEACHER_ID_PASSWORD)
    post_data = {'ClassNO': _class_id}
    res = requests.post(BASE_URL+CLASS_METHOD, headers=HEADERS,
                        data=post_data, cookies=cookies)
    sp_obj = BeautifulSoup(res.content, 'html.parser')
    db_obj = DBManager()
    for tr in sp_obj.find_all('table')[1].findAll('tr')[1:-1]:
        row = tr.find_all('td')[1:4]
        row_dict = dict(zip(CLASS_ID, [row_data.string for row_data in row]))
        post_data = {"ByStudentNO": row[0]}
        res = requests.post(BASE_URL+STUDENT_IDCARD, headers=HEADERS,
                            data=post_data, cookies=cookies)
        tmp_obj = BeautifulSoup(res.content, 'html.parser')
        table = tmp_obj.find_all('table')[0]
        tr = table.find_all('tr')[5]
        td = tr.find_all('td')[3].string
        # db_obj.insert_class_info(row_dict)
        row_dict['IDCARD'] = td
        print (row_dict)
        db_obj.insert_class_info(row_dict)


def get_student_term_info(student_ID,  end_year_term_no):
    flag = True
    db = DBManager()
    cookies = login(TEACHER_ID, TEACHER_ID_PASSWORD)
    post_data = {
            'YearTermNO': end_year_term_no,
            'EndYearTermNO': end_year_term_no,
            'ByStudentNO': int(student_ID)
        }
    student_name = db.get_student_name(student_ID)[0]['姓名']
    try:
        data_dcit = db.get_student_info_by_id(student_ID)[0]
    except Exception as e:
        falg = False
        data_dcit = {'姓名': student_name, '学号': student_ID}
    response = requests.post(BASE_URL+RESULT_METHOD, headers=HEADERS,
                             data=post_data, cookies=cookies)
    sp_obj = BeautifulSoup(response.content, 'html.parser')
    all_tables = sp_obj.find_all('table')[4].find_all('tr')[1:]
    for tr in all_tables:
        tds = tr.find_all('td')
        if tds[0].string is None:
            break
        else:
            if tds[0].string not in data_dcit.keys():
                data_dcit[tds[0].string] = {}
            data_dcit[tds[0].string][tds[2].string] = {
                    '开课模式': tds[3].srting,
                    '总成绩': tds[-2].string,
                    '绩点': tds[-1].string,
                }
    if not flag:
        db.insert_sutdent_info(data_dcit)
    else:
        db.update_student_info(student_ID, data_dcit)
    print (data_dcit)
    return data_dcit


def download_all_term_info(ByStudentNO: str) -> None:
    flag = True
    cookies = login(TEACHER_ID, TEACHER_ID_PASSWORD)
    db = DBManager()
    post_data = {
            'ByStudentNO': ByStudentNO,
        }
    res = requests.post(BASE_URL+ALL_TERM_METHOD, headers=HEADERS,
                        data=post_data,
                        cookies=cookies)
    sp_obj = BeautifulSoup(res.content, 'html.parser')
    GPA = sp_obj.find('script',
                      {'defer': '',
                       'language': 'JavaScript'}).string.split(';')[0]
    GPA = GPA[GPA.find('=')+1:]
    if GPA.startswith('='):
        GPA = GPA[1:]
    student_name = db.get_student_name(ByStudentNO)[0]["姓名"]
    try:
        data_dcit = db.get_all_term_info_by_id(ByStudentNO)[0]
    except Exception as e:
        flag = False
        data_dcit = {
                "姓名": student_name,
                "学号": ByStudentNO,
                "学分绩点": GPA,
                }
    for tr in sp_obj.find_all('table')[-1].find_all('tr')[1:]:
        tds = tr.find_all('td')
        # 数据进入数据库
        if tds[1].string not in data_dcit.keys():
            data_dcit[tds[1].string] = {}
        data_dcit[tds[1].string][tds[4].string] = {
                "成绩": tds[-2].string,
                "课程性质": tds[-1].string,
            }
    if not flag:
        db.insert_all_term_info(data_dcit)
    else:
        db.update_all_term_info_by_id(ByStudentNO, data_dcit)


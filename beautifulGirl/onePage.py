#!/usr/bin/env python
# coding=utf-8

import sys
import os
import requests
import tarfile
import datetime
from random import randint, choice
from bs4 import BeautifulSoup
from config.config import *


HEADERS = {
        'User-Agent': USER_AGENT,
        'Referer': BASE_URL,
        }

def get_all_img(url):
    resp = requests.get(url, headers=HEADERS).content
    soup = BeautifulSoup(resp, 'html.parser')
    image_num = int(soup.select("#page > a")[-2].string)
    name = soup.select('div.article > h2')[0].string
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
        print ('Downloading:  '+filename+'  {}/{}'.format(index, image_num))
        with open(filename, 'wb') as fp:
            fp.write(requests.get(detail_url, headers=HEADERS).content)
    # 方便打包压缩
    return name


def sendEmial(targz_file):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    

    msg = MIMEMultipart()
    msg['Subject'] = 'Beautiful Girl Images'
    msg['From'] = EMAIL_HOST_USER
    receivers = ','.join(['2521895377@qq.com', '944417037@qq.com', '745146218@qq.com'])
    msg['To'] = receivers

    puretext = MIMEText('lalala')
    msg.attach(puretext)
    targz_part = MIMEApplication(open(targz_file, 'rb').read())
    targz_part.add_header('Content-Disposition', 'attachment', filename=targz_file[10:])
    msg.attach(targz_part)

    try:
        client = smtplib.SMTP()
        client.connect(EMAIL_HOST)
        client.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        client.sendmail(EMAIL_HOST_USER, receivers, msg.as_string())
        client.quit()
    except smtplib.SMTPRecipientsRefused:
        pass
    except smtplib.SMTPAuthenticationError:
        pass
    except smtplib.SMTPException as e:
        print (e)

    
if __name__ == '__main__':
    base_url = 'http://www.mmjpg.com/mm/'
    pages = [i for i in range(1, 1261) if i != 1200]
    
    url = base_url+str(choice(pages))
    name = get_all_img(url)
    tar_img = './images/img{}.tar.gz'.format(datetime.date.today())
    with open(tar_img, 'wb') as fp:
        pass
    tar = tarfile.open(tar_img, 'w')
    for file in os.listdir('./images/{}'.format(name)):
        tar.add('./images/{}/{}'.format(name, file), arcname=file)
    tar.close()
    
    # 将打包的邮件发送给人。
    sendEmial(tar_img)


#!/usr/bin/env python
# coding=utf-8

import pytesseract
import requests
import PIL.ImageOps
from PIL import Image


def init(split: int=140) -> list:
    '''
    二值化
    '''
    table = []
    for i in range(256):
        if i<split:
            table.append(0)
        else:
            table.append(1)
    return table


def get_code_cookies(captcha_url: str) -> tuple:
    '''
    要对图片进行一下处理，能更准确的得到验证码
    @param image_path
    return str
    '''
    response = requests.get(captcha_url)
    if response.status_code == 200:
        with open('./code.jpg', 'wb') as fp:
            fp.write(response.content)
    cookies = response.cookies
    image = Image.open('./code.jpg')
    image = image.convert('L')
    binary_image = image.point(init(), '1')
    image = PIL.ImageOps.invert(binary_image.convert('L')).convert('1').convert('L')
    # 获取的图片的像素是60*20
    box = (0, 0, 60, 20)
    res = image.crop(box)
    # 将图片放大方成功的几率更大
    out_image = res.resize((120, 30))
    code = pytesseract.image_to_string(out_image)
    print (code)
    return code, cookies


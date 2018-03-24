#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from functions import *


if __name__ == '__main__':
    '''
    commons
        1. download sutdent person info,  func download_class_info(_class_id: str)
        2. get sutdent term score info, func get_student_term_info(student_id: str, term: int)
        3. get student all score info get_student_all_term_info(student_id: str)

    options
        DBManager
        1. insert_class_info(data:dict)
        2. insert__student_info(data: dict)
        3. get_class_info() return list
        4. get_student_name(student_id: str)
        5. get_student_info()
        6. get_student_info_by_id(student_id: str)
        7. update_student_info(student_id: str, data: dict)

    '''
    # 下载好班级学生的数据
    #for class_id in ['1504052', '1504053']:
        #download_class_info(class_id)

    db = DBManager()
    for student_info in db.get_class_info():
        get_student_term_info(student_info['学号'], get_term())
    

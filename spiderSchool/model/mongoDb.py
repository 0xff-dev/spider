#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient
class DBManager():

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db  = self.client.student
        self.class_info = self.db.Class
        self.student_info = self.db.Student

    
    # 插入操作
    def insert_class_info(self, data: dict) -> None:
        self.class_info.insert(data)
    
    def insert_sutdent_info(self, data: dict) -> None:
        self.student_info.insert(data)

    # 获取信息
    def get_class_info(self) -> list:
        return list(self.class_info.find({}, {'学号': 1}))
    
    def get_student_name(self, student_id: str) -> str:
        return list(self.class_info.find({"学号": student_id}, {"姓名": 1}))

    def get_student_info(self) -> list:
        return list(self.student_info.find())

    # 更新使用
    def get_student_info_by_id(self, student_id: str) -> list:
        return list(self.student_info.find({"学号": student_id}))
    
    def update_student_info(self, student_id: str, data: dict) -> None:
        self.student_info.update({"学号": student_id}, data)

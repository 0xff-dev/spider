#!/usr/bin/env python
# coding=utf-8

import pymongo



class DBManager(object):
    def __init__(self, type_name: str):
        """
        param: type_name python, java, cpp
        """
        self.__client = pymongo.MongoClient('localhost', 27017)
        self.__db = self.__client.lagou
        if type_name == 'c++':
            self.__collection = self.__db.cpp
        else:
            self.__collection = self.__db[type_name]

    def insert_one(self, job: dict):
        self.__collection.insert_one(job)

    def insert(self, *args):
        self.__collection.insert_many(*args)

    def delete(self, flag: dict):
        self.__collection.delete_one(flag)


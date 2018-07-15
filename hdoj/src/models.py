from pymongo import MongoClient

# model后续完成即可

class DBManager(object):
    def __init__(self):
        self.__client = MongoClient('localhost', 27017)
        self.__db = self.__client.SADRA
        self.__collection = self.__db.user

    def insert(self, user: dict):
        self.__collection.insert_one(user)
 
    def find_one(self, user):
        # 查询一个用户的全部信息
        return list(self.__collection.find_one({'user': user}))[0]

    def options_find(sefl, **kwargs):
        pass

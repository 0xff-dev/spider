from pymongo import MongoClient

# model后续完成即可

class DBManager(object):
    def __init__(self):
        self.__client = MongoClient('localhost', 27017)
        self.__db = self.__client.SADRA
        self.__collection = self.__db.user

    def insert(self, user: dict):
        self.__collection.insert_one(user)

    def insert_many(self, *args):
        """
        params: [User, User]
        """
        pass

    def find(self, **kwargs):
        """
        默认查询所有的
        param: kwargs 过滤参数
        """
        try:
            return self.__db.find()
        except Exception as e:
            raise (e.args)

    def find_one(self, **kwargs):
        pass

    def update(self,  **kwargs):
        """跟新个人信息, 主要是增加题数"""
        pass


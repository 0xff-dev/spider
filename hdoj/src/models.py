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
    
    def is_exists(self, user, p_id, date):
        try:
            result = list(self.__collection.find({'user': user},
                                                {'date_ps.{}'.format(date)}))[0]
            if p_id in result['date_ps'][date]:
                return True
            return False
        except Exception as e:
            # 数据中没有数据
            return False

    def options_find(sefl, **kwargs):
        pass

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
        return self.__collection.find_one({'user': user})
    
    def is_exists_in_date(self, user, p_id, date):
        # 同一天做一道题，提交了若干次, 之记录一次
        try:
            result = list(self.__collection.find({'user': user},
                                                {'date_ps.{}'.format(date)}))[0]
            if p_id in result['date_ps'][date]:
                return True
            return False
        except Exception as e:
            # 数据中没有数据
            return False
    
    def is_exists_in_db(self, user, p_id):
        # 查看这道题在数据库中是否存在
        data = self.find_one(user)
        for _, values in data['date_ps'].items():
            if p_id in values:
                return True
        return False

    def update(self, user, _data: dict):
        self.__collection.update_one({"user": user},
                                     {'$set': {"date_ps": _data['date_ps'],
                                               'count': _data['count']}})


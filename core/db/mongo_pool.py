"""
    在init中建立数据库连接，获取要操作的集合
"""
from settings import MONGO_URL
from pymongo import MongoClient
from utils.log import MyLog
from domain import Proxy
import pymongo


class MongoPool(object):
    def __init__(self):
        # 在init中，建立数据连接，获取要操作的集合
        self.client = MongoClient(MONGO_URL)
        # 要获取的集合
        self.proxies = self.client['proxies_pool']['proxies']

    def __del__(self):
        # 关闭数据库连接
        self.client.close()

    def insert_one(self, proxy):
        # 实现插入数据功能
        count = self.proxies.count_documents({'ip': proxy.ip})
        # 如果数据库中ip地址不存在，插入此ip地址
        if count == 0:
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            MyLog().debug("插入新的的代理地址:{}".format(proxy))
        else:
            MyLog().warning("已经存在的代理:{}".format(proxy))

    def update_one(self, proxy):
        """实现修改数据库的功能"""
        self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})

    def delete_one(self, proxy):
        """实现数据库的删除功能"""
        self.proxies.delete_one({'_id': proxy.ip})
        MyLog.debug("此id已经被删除：{}".format(proxy))

    def find_all(self):
        """数据库的查询操作"""
        cursor = self.proxies.find()
        for item in cursor:
            # 删除item中的“_id”
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        """
        :param conditions:
        :param count:
        :return:返回一个满足要求的一个代理ip列表
        """
        # 对代理池的ip进行排序，score降序，speed升序
        cursor = self.proxies.find(conditions, limit=count).sort(
            [('score', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)])
        proxy_list = []
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list


if __name__ == '__main__':
    mongo = MongoPool()
    # proxy = Proxy("192.168.1.42", speed=2)
    # mongo.update_one(proxy)
    # for i in mongo.find_all():
    #     print(i)
    for i in mongo.find({'protocol': -1}):
        print(i)
    mongo.__del__()

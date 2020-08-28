"""
    在init中建立数据库连接，获取要操作的集合
"""
import random
import pymongo
from settings import MONGO_URL
from pymongo import MongoClient
from utils.log import MyLog
from domain import Proxy


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
        :param conditions: 要查询的key：value
        :param count: 显示的数量
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

    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        实现根据协议类型和要访问网站的域名，获取代理IP列表
        :param protocol: 协议：http， https
        :param domain: 域名：jd.com
        :param count: 用于限制获取多个代理IP，默认是获取所有
        :param nick_type:匿名类型，默认获取高匿名的代理Ip
        :return:满足要求代理Ip
        """
        conditions = {"nick_type": nick_type}
        if protocol is None:
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {"$in": [0, 2]}
        else:
            conditions['protocol'] = {"$in": [1, 2]}

        if domain:
            conditions['disable_domains'] = {'$nin': ['domain']}
            print(conditions)

        return self.find(conditions, count=count)

    def random_proxy(self, protocol=None, domain=None, count=0, nick_type=0):
        """
                实现根据协议类型和要访问网站的域名，获取代理IP列表
                :param protocol: 协议：http， https
                :param domain: 域名：jd.com
                :param count: 用于限制获取多个代理IP，默认是获取所有
                :param nick_type:匿名类型，默认获取高匿名的代理Ip
                :return:满足要求代理Ip
                """
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, count=count, nick_type=nick_type)
        # 随机返回一个代理IP
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        """
        实现把制定域名添加到指定IP的disable_domain列表中
        :param ip:IP地址
        :param domain:域名地址
        :return:如果返回True，就表示添加成功了
        """
        if self.proxies.count_documents({'_id': ip, 'disable_domains': domain}) == 0:
            # 如果disable_domains字段中没有这个，就添加进去
            self.proxies.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
        else:
            print("domain已经存在")


if __name__ == '__main__':
    mongo = MongoPool()
    proxy = Proxy(ip='220.249.149.180', port='9999')
    mongo.insert_one(proxy)
    # proxy = Proxy("194.168.1.42", speed=2)
    # print(mongo.insert_one(proxy))
    # proxy = Proxy("192.168.1.43", protocol=2, )
    # mongo.insert_one(proxy)
    # mongo.update_one(proxy)
    # mongo.disable_domain("192.168.1.43", "淘宝.com")
    for i in mongo.find_all():
        print(i)
    # for i in mongo.find({'protocol': -1}, count=0):
    #     print(i)
    # for i in mongo.get_proxies(domain=1):
    #     print(i)
    # proxy = Proxy(ip='192.168.1.42')
    # mongo.delete_one(proxy)

    mongo.__del__()

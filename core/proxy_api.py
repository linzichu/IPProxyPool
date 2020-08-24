from pymongo import MongoClient

client = MongoClient("127.0.0.1")
proxies = client['proxies_pool']["proxies"]
conditions = {'speed': {"$nin": [-1]}}
cursor = proxies.find(conditions)
for i in cursor:
    i.pop('_id')
    print(i)

# 
"""
    MongoDB数据库调试
"""

from pymongo import MongoClient

conn_ali = '47.92.72.108:28010'
conn_rs = '192.168.5.236:28010'

c = MongoClient(host=conn_rs)
db = c.iTRODB_20170411
co = db.iTRO_Product

result = co.find({},{'_id':0})

conn = MongoClient(host=conn_rs.host)
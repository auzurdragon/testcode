# -*- coding=utf-8 -*-
"""
    公共方法
    to_flowlog(), 记录流水日志
"""

def to_flowlog(userid, orderid, ordertype,
               logtype, amount, remain, memo,
               logtype2=int(0), goldtype=int(3),
               mongo=""):
    """记录日志记录"""
    from pymongo import MongoClient
    from time import time
    # 默认使用本地的MongoDB
    if mongo == "":
        mongo = {
            "HOST":"localhost",
            "PORT":28010,
            "DB":"iTROLogdb",
            "CO":"iTRO_FlowLog"
        }
    try:
        logdict = {
            "userid" : userid,
            "orderid" : orderid,
            "ordertype" : int(ordertype),
            "logtype" : int(logtype),
            "logtype2" : int(logtype2),
            "goldtype" : int(goldtype),
            "amount" : int(amount),
            "remain" : int(remain),
            "memo" : memo,
            "date" : str(int(time()))
        }
        conn = MongoClient(host=mongo["HOST"], port=mongo["PORT"])
        db = conn.get_database(mongo["DB"])
        coll = db.get_collection(mongo["CO"])
        coll.insert_one(logdict)
        return True
    except:
        return False
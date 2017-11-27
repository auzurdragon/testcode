#coding:utf8
"""
    数据统计脚本
    依赖包：time, pymongo, pandas
"""
__auth__ = "胡岸"
class Statistic(object):
    """生产环境数据统计脚本"""
    def __init__(self, strdate=""):
        from datetime import datetime, timedelta
        self.db = {
            "HOST":"localhost",
            "PORT":28010,
        }
        # 获得查询日期的开始和结束时间戳
        self.sdate = {
            "stime":int(0), # 查询日期的开始时间戳
            "etime":int(0)  # 查询日期的结束时间戳
        }
        if strdate:
            self.sdate = {
                "sdate":strdate,
                "stime":int(datetime.strptime(strdate, "%Y-%m-%d").timestamp()),
                "etime":int(datetime.strptime(strdate, "%Y-%m-%d").timestamp() + 86400)
            }
        else:
            self.sdate = {
                "sdate":datetime.strftime(datetime.now() + timedelta(days=-1), "%Y-%m-%d"),
                "stime":int(datetime.strptime((datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp()),
                "etime":int(datetime.strptime((datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp() + 86400)
            }
        self.result = {
            "date": self.sdate["sdate"],    # 日期
            "totaluser":int(0),     # 累计注册用户
            "newuser":int(0),       # 新增注册用户
            "newstore":int(0),      # 新增商户，即新开店的账号
            "loginuser":int(0),     # 登录用户数量
            "loginip":int(0),       # 登录ip数量
            "loginnum":int(0),      # 登录记录数
            "chargenum":int(0),     # 充值次数
            "chargesum":int(0),     # 充值金额
            "chargeuser":int(0),    # 充值账号数
            "mallview":int(0),      # 商城访问次数，商品和店铺页面打开次数合计
            "storeview":int(0),     # 店铺访问次数，只包括店铺页面的访问记录
            "topstore":[],          # 店铺访问top10
            "waresview":int(0),     # 商品访问次数，商品页面打开次数合计
            "topwares":[],          # 商品访问次数TOP10
        }
        self.client = ""    # 保存数据库连接
        self.conn = ""      # 保存数据连接
    
    def mongo_conn(self, dbname="iTROdb", coname="iTRO_User"):
        """建立数据库连接"""
        from pymongo import MongoClient
        try:
            self.client.server_info()
        except Exception as errinfo:
            self.client = MongoClient(host=self.db["HOST"], port=self.db["PORT"])
        finally:
            self.conn = self.client.get_database(dbname)
            self.conn = self.conn.get_collection(coname)

    def to_mongo(self):
        """写入数据到108数据库"""
        from pymongo import MongoClient
        client = MongoClient("172.26.143.73", 28010)
        # client = MongoClient("47.92.72.108", 28010)
        conn = client.iTROdb.iTRO_Statistic
        conn.update(
            {"sdate":self.sdate["sdate"]},
            {"$set":{
                "totaluser":self.result["totaluser"],
                "newuser":self.result["newuser"],
                "newstore":self.result["newstore"],
                "loginuser":self.result["loginuser"],
                "loginip":self.result["loginip"],
                "loginnum":self.result["loginnum"],
                "chargenum":self.result["chargenum"],
                "chargesum":self.result["chargesum"],
                "chargeuser":self.result["chargeuser"],
                "mallview":self.result["mallview"],
                "storeview":self.result["storeview"],
                "topstore":self.result["topstore"],
                "waresview":self.result["waresview"],
                "topwares":self.result["topwares"],
            }},
            upsert=True
        )

    def s_totaluser(self):
        """指定日期查询累计用户数量"""
        self.mongo_conn(dbname="iTROdb", coname="iTRO_User")
        self.result["totaluser"] = self.conn.find({"CreateDt":{"$lt":self.sdate["etime"]}}).count()

    def s_newuser(self):
        """指定日期查询新增注册用户"""
        self.mongo_conn(dbname="iTROdb", coname="iTRO_User")
        self.result["newuser"] = self.conn.find({"CreateDt":{"$gte":self.sdate["stime"], "$lt":self.sdate["etime"]}}).count()
    
    def s_newstore(self):
        """查询新增商户，iTRO_OpenShopOrder.status=2，以支付保证金订单成功为准"""
        self.mongo_conn(dbname="iTROdb", coname="iTRO_OpenShopOrder")
        self.result["newstore"] = self.conn.find({"paydatee":{"$gte":self.sdate["stime"], "$lt":self.sdate["etime"]}}).count()

    def s_charge(self):
        """查询充值次数、金额合计和充值账号数量，以充值成功为准"""
        self.mongo_conn(dbname="iTROdb", coname="iTRO_CzOrder")
        t = self.conn.aggregate([
            {"$match":{"date":{"$gte":self.sdate["stime"],"$lt":self.sdate["etime"]},"status":True}},
            {"$project":{"orderid":"$orderid","userid":"$userid","ordermoney":"$ordermonry"}},
            {"$group":{
                "_id":"null",
                "chargenum":{"$sum":1},
                "chargesum":{"$sum":"$ordermoney"},
                "chargeuser":{"$addToSet":"$userid"}
            }}
        ])
        t = list(t)
        if t :
            tmp = t[0]
            self.result["chargenum"] = tmp["chargenum"]
            self.result["chargesum"] = tmp["chargesum"]
            self.result["chargeuser"] = len(tmp["chargeuser"])
        else:
            self.result["chargenum"] = int(0)
            self.result["chargesum"] = int(0)
            self.result["chargeuser"] = int(0)

    def s_login(self):
        """登录用户数、IP数统计和登录记录数"""
        self.mongo_conn(dbname="iTROdb", coname="iTRO_Log")
        t = self.conn.find(
            {"LogTime":{"$regex":self.sdate["sdate"]}, "SType":1},
            {"_id":0, "UserId":1, "LogTime":1, "LogIp":1}
        )
        t = list(t)
        counter = set([i["UserId"] for i in t])
        self.result["loginuser"] = len(counter)
        counter = set([i["LogIp"] for i in t])
        self.result["loginip"] = len(counter)
        self.result["loginnum"] = len(t)

    def s_mallview(self):
        """网页访问数据，包括商品访问次数和店铺页面访问次数"""
        from pandas import DataFrame as df
        self.mongo_conn(dbname="iTROdb", coname="iTRO_CNZZ")
        t = self.conn.find(
            {"date":self.sdate["sdate"]},
            {"_id":0,"type":1,"ip":1,"sid":1,"pid":1}
        )
        t = df(list(t))
        if len(t) == 0:
            print("%s, s_mallview no data" % self.sdate["sdate"])
            return
        else:
            # 商城访问次数，包括店铺和商品
            self.result["mallview"] = len(t)
            # 店铺访问次数，只包括店铺的访问记录
            t_store = t[t["type"]==2]
            self.result["storeview"] = len(t_store)
            tmp = t_store.sid.value_counts()
            # 记录店铺页面访问次数的top10
            j = 10 if len(tmp) > 10 else len(tmp)
            for i in range(j):
                self.result["topstore"].append(tmp.index[i])
            # 商品访问次数，只统计商品页面的记录次数
            # 提取商品页面访问记录
            t_wares = t[t["type"]==1]
            # 商品页面的全部访问次数
            self.result["waresview"] = len(t_wares)
            # 统计商品页面访问次数的top10
            j = 10 if len(tmp) > 10 else len(tmp)
            for i in range(j):
                self.result["topwares"].append(tmp.index[i])
     
    def s_order(self):
        """统计交易子订单"""

# 查询数据
def get_data(self,sdate,edate):
    """查询数据"""
from pandas import DataFrame as df
from pymongo import MongoClient
sdate = "2017-11-20"
edate = "2017-11-22"
client = MongoClient("47.92.72.108",28010)
conn = client.iTROdb.iTRO_Statistic
td = conn.find({"sdate":{"$gte":sdate, "$lte":edate}},{"_id":0,"totaluser":1,"newuser":1,"loginuser":1,"loginnum":1,"loginip":1,"newstore":1,"chargeuser":1,"chargesum":1,"chargenum":1,"mallview":1,"storeview":1,"waresview":1,"sdate":1})
td = list(td)
td = df(td)
td.index = td["sdate"]
td = td.ix[:,["totaluser","newuser","loginuser","loginnum","loginip","newstore","chargeuser","chargesum","chargenum","mallview","storeview","waresview"]]
td.T.to_clipboard()


if __name__ == "__main__":
    # from itro_scripts.itro_statistic import Statistic
    import sys
    sdate = "" if len(sys.argv) == 1 else sys.argv[1]
    s = Statistic(sdate)
    s.s_totaluser()
    s.s_newuser()
    s.s_newstore()
    s.s_charge()
    s.s_login()
    s.s_mallview()
    s.to_mongo()
    print(s.result)

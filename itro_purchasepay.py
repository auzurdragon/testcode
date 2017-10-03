# -*- coding=utf-8 -*-
"""
#   public class iTRO_Purchase
#     {
#         public ObjectId _id { get; set; } = ObjectId.GenerateNewId();
#         public long date { get; set; } = ObjectId.GenerateNewId().Timestamp;
#         /// <summary>
#         /// 订单编号
#         /// </summary>
#         public string ordersn { get; set; }
#         /// <summary>
#         /// 下单用户id
#         /// </summary>
#         public string userid { get; set; }
#         /// <summary>
#         /// 店铺id
#         /// </summary>
#         public string storeid { get; set; }
#         /// <summary>
#         /// 支付方式 0货到付款 1在线支付
#         /// </summary>
#         public int paytype { get; set; } = 0;
#         /// <summary>
#         /// 是否已经支付 1已支付 0未支付
#         /// </summary>
#         public int ispay { get; set; } = 0;
#         public int paymongy { get; set; } = 0;
#         /// <summary>
#         /// 备注
#         /// </summary>
#         public string desc { get; set; }
#         /// <summary>
#         /// 商品列表
#         /// </summary>
#         public List<orderlist> orderlist { get; set; }
#         /// <summary>
#         /// 订单状态默认0:下单状态 1:待发货 2:已发货 3:已收货
#         /// </summary>
#         public int orderstatus { get; set; } = 0;
#         /// <summary>
#         /// 快递名称
#         /// </summary>
#         public string kdname { get; set; } = string.Empty;
#         /// <summary>
#         /// 快递单号
#         /// </summary>
#         public string kdnum { get; set; } = string.Empty;
# 		/// <summary>
#         /// 服务是否已经付款默认0未付款 1付款
#         /// </summary>
#         public int paystatus { get; set; } = 0;
#     }

# 	iTROdb.iTRO_Purchase  (商家进货订单表)
# 	paystatus ==0 & paytype==1 & ispay == 1 & orderstatus == 3 & date <= 15天前
# 	获得 paymongy  (单位：分)
	
# 	iTRO_Purchase.storeid == iTRO_store._id
#   iTRO_store.userid == iTRO_User.NId
#   按照 storeid 在 iTRO_store.userid, 对应iTRO_User中的NId
# 	按照 userid 在 iTRO_User 表查询 _id  (Money, useMoney)
	
# 	修改完后，将 paymoney 修改为1
# 	记日志iTROLogdb.iTRO_FlowLog

依赖包
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymongo
time
pywin32
"""
import win32serviceutil
import win32service
import win32event


class do_purchasepay(object):
    """经销商进货系统，处理15天的订单"""
    def __init__(self):
        self.mongo = {
            'HOST':'localhost',
            'PORT':28010,
            'DB':'iTROdb',
            'COPurchase':'iTRO_Purchase',
            'COStore':'iTRO_Store',
            'COUser':'iTRO_User',
            'DBFlow':'iTROLogdb',
            'COFlow':'iTRO_FlowLog',
        }
        self.result = [
            # {
            # "purchaseid":iTROdb.iTRO_Purchase._id,    # 表记录_id，用于回写
            # "storeid":iTROdb.iTRO_Purchase.storeid,   # 店铺ID
            # "amount":iTROdb.iTRO_Purchase.paymongy,   # 进货订单的金额
            # "orderid":iTROdb.iTRO_Purchase.ordersn,   # 进货单ID
            # "nid":iTROdb.iTRO_Store.UserId,           # 店铺对应的商户NID
            # "userid":iTROdb.iTRU_User._id,            # 店铺对应的商户ID
            # "remain":iTROdb.iTRU_User.UseMomey+self.money,    # 商户收款后的账户余额
            # "log":errormsg,                           # 保存错误信息
            # },
        ]

    def get_paylist(self):
        """
            访问iTROdb.iTRO_Purchase, 获得storeid和paymongy
            查询条件：paystatus ==0(未付款) & paytype==1(在线支付) & ispay == 1(已支付) & orderstatus == 3(已收货) & date <= 15天前
        """
        from pymongo import MongoClient
        from time import time
        try:
            conn = MongoClient(host=self.mongo["HOST"], port=self.mongo["PORT"])
            db = conn.get_database(self.mongo["DB"])
            coll = db.get_collection(self.mongo["COPurchase"])
            # 查询记录，条件：paystatus:0 未完成付款; paytype:1 在线支付; ispay:1 已付款; orderstatus:3 已收货
            tmp = coll.find(
                {"date":{"$lte":int(time()) - 1296000}, 
                 "paystatus":0, 
                 "paytype":1, 
                 "ispay":1, 
                 "orderstatus":3},
                {"_id":1, "storeid":1, "paymongy":1, "ordersn":1})
            tmp = list(tmp)
            for i in tmp:
                self.result.append({
                    "purchaseid":i["_id"],
                    "storeid":i["storeid"],
                    "amount":i["paymongy"],
                    "orderid":i["ordersn"]                    
                })
            return True
        except:
            return False

    def get_nid(self):
        """按照storeid查询发货店铺在iTRO_store表中对应的商户ID，即iTRO_store.UserId"""
        from pymongo import MongoClient
        from bson import ObjectId
        try:
            conn = MongoClient(host=self.mongo["HOST"], port=self.mongo["PORT"])
            db = conn.get_database(self.mongo["DB"])
            coll = db.get_collection(self.mongo["COStore"])
            for i in self.result:
                try:
                    i["nid"] = coll.find_one(
                        {"_id":(ObjectId(i["storeid"]))},
                        {"_id":0, "UserId":1})["UserId"]
                except:
                    i["log"] = "get_nid failed"
                    continue
        except:
            return False

    def do_addmoney(self, nid, amount):
        """按照paymongy和商户id，修改iTROdb.iTRO_User, 增加发货商户的账号余额, 返回增加后的money，即账号当前余额 """
        from pymongo import MongoClient
        try:
            conn = MongoClient(host=self.mongo["HOST"], port=self.mongo["PORT"])
            db = conn.get_database(self.mongo["DB"])
            coll = db.get_collection(self.mongo["COUser"])
            tmp = coll.find_one({"NId":nid}, {"_id":1, "UseMomey":1})
            res = {
                "userid":tmp["_id"],
                "usemoney":tmp["UseMomey"]
            }
            coll.update_one({"NId":nid},{"$inc":{"Money":int(amount), "UseMomey":int(amount)}})
            return res
        except:
            return False

    def upd_paylog(self, logid):
        """
            修改iTROdb.iTRO_Purchase表中记录的paystatus，修改为1(已付款)
            需要传入_id, 按_id查找记录
        """
        from pymongo import MongoClient
        try:
            conn = MongoClient(host=self.mongo["HOST"], port=self.mongo["PORT"])
            db = conn.get_database(self.mongo["DB"])
            coll = db.get_collection(self.mongo["COPurchase"])
            coll.update_one(
                {"_id":logid},
                {"$set":{"paystatus":int(1)}})
            return True
        except:
            return False

def to_flowlog(userid, orderid, ordertype, logtype, amount, remain, memo, logtype2=int(0), goldtype=int(3)):
    """记录日志记录"""
    from pymongo import MongoClient
    from time import time
    try:
        logdict = {
            "userid" : userid,
            "orderid" : orderid,
            "ordertype" : ordertype,
            "logtype" : logtype,
            "logtype2" : logtype2,
            "goldtype" : goldtype,
            "amount" : amount,
            "remain" : remain,
            "memo" : memo,
            "date" : int(time())
        }
        conn = MongoClient(host=self.mongo["HOST"], port=self.mongo["PORT"])
        db = conn.get_database(self.mongo["DBFlow"])
        coll = db.get_collection(self.mongo["COFlow"])
        coll.insert_one(logdict)
        return True
    except:
        return False


if __name__ == "__main__":
    s = do_purchasepay()
    s.get_paylist()
    s.get_nid()
    for i in s.result:
        res_do_addmoney = s.do_addmoney(nid=i["nid"],amount=i["amount"])
        if res_do_addmoney:
            i["userid"] = res_do_addmoney["userid"]
            i["remain"] = res_do_addmoney["usemoney"] + i["amount"]
        else:
            i["log"] = "do_addmoney failed"
            continue
        res_upd_paylog = s.upd_paylog(i["purchaseid"])
        if res_upd_paylog:
            to_flowlog(
                userid=i["userid"], orderid=i["orderid"], ordertype=int(2),
                logtype=int(10602), amount=i["amount"], remain=i["remain"],
                memo="“商家进货付款", logtype2=int(0), goldtype=int(3)
                )
        else:
            i["log"] = "upd_paylog failed"
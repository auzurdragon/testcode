"""
    1. redis, 47.92.72.108:6394, db0
    2. Redraingetprice
    3. redveid:红包ID, getuid:领取用户id, val:领取的金额,
    4. 按 getuid 访问iTROdb.iTRO_User, 获得用户当前的 Money, 将Money修改为 Money+val, 同时Money+val保存入记录,做为remain
    5. 按 redveid 访问 iTRO_SocialDb.iTRO_RedPacket, 将 getuid, val 分别push到数组getuid, getAmount。
    6. 访问 iTROLogdb.iTRO_FlowLog, insert 记录。

    所依赖的包
    python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymongo,redis
    json,time,bson
"""

class iTRO_redPacket(object):
    """
        红包记录处理
        1. redis, 47.92.72.108:6394, db0
        2. Redraingetprice
        3. redveid:红包ID, getuid:领取用户id, val:领取的金额,
        4. 按 getuid 访问iTROdb.iTRO_User, 获得用户当前的 Money, 将Money修改为 Money+val, 同时Money+val保存入记录,做为remain
        5. 按 redveid 访问 iTRO_SocialDb.iTRO_RedPacket, 将 getuid, val 分别push到数组getuid, getAmount。
        6. 访问 iTROLogdb.iTRO_FlowLog, insert 记录。
    """
    def __init__(self):
        """定义数据库连接"""
        self.redis = {
            'HOST':'localhost',
            'PORT':6394,
            'DB':0,
            'HKEY':'RedrainGetPirce'
        }
        self.mongo = {
            'HOST':'localhost',
            'PORT':28010,
            'DBRed':'iTRO_SocialDb',
            'CORed':'iTRO_RedPacket',
            'DBLog':'iTROLogdb',
            'COLog':'iTRO_FlowLog',
            'DBUser':'iTROdb',
            'COUser':'iTRO_User'
        }
        # 用于保存处理记录的列表
        self.result = {
            # "keyname":{   # redis中的field
            #   "rkey":,    # 与field相同
            #   "redveid":, # 红包id
            #   "getuid":,  # 获得红包的用户id
            #   "val":,     # 获得的金额
            #   "money":,   # 获得红包前的账号余额
            #   "remain":,  # 获得红包后的账号余额
            #   "msg":,     # 该记录处理的情况
            # }
        }
        self.lognum = int(0)
        # 用于保存处理记录的文件夹
        self.logpath = 'E:/iTROLog/'

    def do_redpacket(self):
        """执行红包记录处理, 每次处理5000条, 则进行一次休眠，以降低压力"""
        from time import sleep
        stop = 0
        for i in self.result:
            self.get_userRemain(i)
            self.to_userRemain(i)
            self.to_redlog(i)
            self.to_flowlog(i)
            self.del_redlog(i)
            stop += 1
            if stop ==5000:
                sleep(5)
        self.to_logfile()


    def get_redField(self):
        """获得redis缓存中的field, 如果没有传入field, 则返回所有的key。否则按field返回指定的hkey值。"""
        from redis import Redis
        from json import loads
        conn = Redis(host=self.redis['HOST'], port=self.redis['PORT'], db=self.redis['DB'])
        if conn.exists(self.redis["HKEY"]):
            keys = conn.hkeys(self.redis["HKEY"])
            self.result = self.result.fromkeys([i.decode() for i in keys])
            self.lognum = len(self.result)
        else:
            print("%s is not exists" % (self.redis["HKEY"]))
            return False
        result True

    def get_redValue(self, field):
        """按field查询value"""
        from redis import Redis
        from json import loads
        conn = Redis(host=self.redis['HOST'], port=self.redis['PORT'], db=self.redis['DB']) 
        self.result[field] = loads(conn.hget(self.redis["HKEY"], field))
        return True

    def get_userRemain(self, field):
        """按userid从mongodb中获得用户的余额，每次只处理一条数据, index 为result列表的索引，即处理第几条数据"""
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['DBUser'])
        coll = db.get_collection(self.mongo['COUser'])
        T = coll.find_one({'_id':ObjectId(self.result[field]['getuid'])}, {'_id':0, 'Money':1})
        if T:
            self.result[field]['msg'] = 'get remain'
            self.result[field]['money'] = T['Money']
            self.result[field]['remain'] = self.result[field]['val'] + T['Money']
            conn.close()
            return True
        else:
            self.result[field]['msg'] = 'get remain failed'
            self.result[field]['money'] = 0
            self.result[field]['remain'] = self.result[field]['val']
            self.to_errorlog(field)
            conn.close()
            return False


    def to_userRemain(self, field):
        """
            按userid，将用户领取红包后的余额, 回写到mongodb.iTROdb.iTRO_User表中
        """
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['DBUser'])
        coll = db.get_collection(self.mongo['COUser'])
        tmp = coll.update_one(
            {'_id':ObjectId(self.result[field]['getuid'])},
            {'$set':{'Money':int(self.result[field]['remain'])}}
        )
        conn.close()
        if tmp.raw_result['updatedExisting']:
            self.result[field]['msg'] = 'update money'
            return True
        else:
            self.result[field]['msg'] = 'update money failed'
            self.to_errorlog(field)
            return False


    def to_redlog(self, field):
        """
            将记录写入 iTRO_SocialDb.iTRO_RedPacket
        """
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        # 修改账号余额为领取红包后的余额, 即money+val
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['DBRed']) 
        coll = db.get_collection(self.mongo['CORed'])
        tmp = coll.update_one(
            filter = {'$or':[{'_id':ObjectId(self.result[field]['redveid'])}, {'randomnum': self.result[field]['redveid']}]},
            update = {'$push':{'getuid':self.result[field]['getuid'], 'getAmount':int(self.result[field]['val'])}}
        )
        if tmp.raw_result['updatedExisting']:
            self.result[field]['msg'] = 'write RedPacket'
            conn.close()
            return True
        else:
            self.result[field]['msg'] = 'write redpacket failed'
            self.to_errorlog(field)
            conn.close()
            return False
    
    def to_flowlog(self, field):
        """
            访问iTROLogdb.iTRO_FlowLog, 写入金额增加记录
        """
        from pymongo import MongoClient
        from time import time
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['DBLog'])
        coll = db.get_collection(self.mongo['COLog'])
        coll.insert_one({
            "userid": self.result[field]['getuid'],
            "orderid": 'red'+str(int(time())),
            "ordertype": int(2),
            "logtype": int(10501),
            # "logtype2": int(0),
            "goldtype": int(3),
            "amount": int(self.result[field]['val']),
            "remain": int(self.result[field]['remain']),
            "memo": "红包",
            "date": str(int(time()))
        })
        conn.close()
        return True

    def del_redlog(self, field):
        """删除redis中RedrainGetPirce已处理的field"""
        from redis import Redis
        conn = Redis(host=self.redis['HOST'], port=self.redis['PORT'], db=self.redis['DB'])
        conn.hdel(self.redis['HKEY'], self.result[field]['rkey'])
        self.result[field]['msg'] = 'del log'
        return True

    def to_logfile(self):
        """保存处理结果记录"""
        from time import time
        logfile = '%slog_redpacket%d.txt' % (self.logpath, int(time()))
        with open(logfile, 'a+', encoding='utf8') as writer:
            for i in self.result:
                writer.write(str(self.result[i])+'\n\r')
        return True
    
    def to_errorlog(self, field):
        from time import time
        errorfile = "%serror_redpacket%d.txt" % (self.logpath, int(time()))
        with open(errorfile, "a+", encoding="utf-8") as write:
            writer.write(str(self.result[field]) + "\n\r")

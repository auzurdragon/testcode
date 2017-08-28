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
        self.RESULT = []
        # 用于保存处理记录的文件夹
        self.LOGPATH = 'E:/iTROLog/'

    def get_redLog(self):
        """获得redis缓存中的key, 如果没有传入field, 则返回所有的key。否则按field返回指定的hkey值。"""
        from redis import Redis
        from json import loads
        CONN = Redis(host=self.redis['HOST'], port=self.redis['PORT'], db=self.redis['DB'])
        tmp = CONN.hgetall(self.redis['HKEY'])
        for i in tmp:
            self.RESULT.append(loads(tmp[i]))
        return True

    def get_userRemain(self, index):
        """按userid从mongodb中获得用户的余额，每次只处理一条数据, index 为RESULT列表的索引，即处理第几条数据"""
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        CONN = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        DB = CONN.get_database(self.mongo['DBUser'])
        COLL = DB.get_collection(self.mongo['COUser'])
        T = COLL.find_one({'_id':ObjectId(self.RESULT[index]['getuid'])}, {'_id':0, 'Money':1})
        if T:
            self.RESULT[index]['msg'] = 'get remain'
            self.RESULT[index]['money'] = T['Money']
            self.RESULT[index]['remain'] = self.RESULT[index]['val'] + T['Money']
            CONN.close()
            return True
        else:
            self.RESULT[index]['msg'] = 'get remain failed'
            self.RESULT[index]['money'] = 0
            self.RESULT[index]['remain'] = self.RESULT[index]['val']
            CONN.close()
            return False


    def to_userRemain(self, index):
        """
            按userid，将用户领取红包后的余额, 回写到mongodb.iTROdb.iTRO_User表中
        """
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        CONN = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        DB = CONN.get_database(self.mongo['DBUser'])
        COLL = DB.get_collection(self.mongo['COUser'])
        tmp = COLL.update_one(
            {'_id':ObjectId(self.RESULT[index]['getuid'])},
            {'$set':{'Money':int(self.RESULT[index]['remain'])}}
        )
        CONN.close()
        if tmp.raw_result['updatedExisting']:
            self.RESULT[index]['msg'] = 'update money'
            return True
        else:
            self.RESULT[index]['msg'] = 'update money failed'
            return False


    def to_redlog(self, index):
        """
            将记录写入 iTRO_SocialDb.iTRO_RedPacket
        """
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        # 修改账号余额为领取红包后的余额, 即money+val
        CONN = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        DB = CONN.get_database(self.mongo['DBRed']) 
        COLL = DB.get_collection(self.mongo['CORed'])
        tmp = COLL.update_one(
            filter = {'$or':[{'_id':ObjectId(self.RESULT[index]['redveid'])}, {'randomnum': self.RESULT[index]['redveid']}]},
            update = {'$push':{'getuid':self.RESULT[index]['getuid'], 'getAmount':int(self.RESULT[index]['val'])}}
        )
        if tmp.raw_result['updatedExisting']:
            self.RESULT[index]['msg'] = 'write RedPacket'
            CONN.close()
            return True
        else:
            self.RESULT[index]['msg'] = 'write redpacket failed'
            CONN.close()
            return False
    
    def to_flowlog(self, index):
        """
            访问iTROLogdb.iTRO_FlowLog, 写入金额增加记录
        """
        from pymongo import MongoClient
        from time import time
        CONN = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        DB = CONN.get_database(self.mongo['DBLog'])
        COLL = DB.get_collection(self.mongo['COLog'])
        COLL.insert_one({
            "userid": self.RESULT[index]['getuid'],
            "orderid": 'red'+str(int(time())),
            "ordertype": int(2),
            "logtype": int(10501),
            # "logtype2": int(0),
            "goldtype": int(3),
            "amount": int(self.RESULT[index]['val']),
            "remain": int(self.RESULT[index]['remain']),
            "memo": "红包",
            "date": str(int(time()))
        })
        CONN.close()
        return True

    def del_redlog(self, index):
        """删除redis中RedrainGetPirce已处理的field"""
        from redis import Redis
        CONN = Redis(host=self.redis['HOST'], port=self.redis['PORT'], db=self.redis['DB'])
        CONN.hdel(self.redis['HKEY'], self.RESULT[index]['rkey'])
        self.RESULT[index]['msg'] = 'del log'
        return True

    def to_logfile(self):
        """保存处理结果记录"""
        from time import time
        logfile = '%slog_redpacket%d.txt' % (self.LOGPATH, int(time()))
        with open(logfile, 'a+', encoding='utf8') as writer:
            for i in self.RESULT:
                writer.write(str(i)+'\n\r')
        return True

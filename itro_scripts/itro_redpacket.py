# -*- coding=utf-8 -*-

class itro_redpacket(object):
    """
        红包记录处理
        1. redis, localhost:6394, db0
        2. Redraingetprice
        3. redveid:红包ID, getuid:领取用户id, val:领取的金额,
        4. 按 getuid 访问iTROdb.iTRO_User, 获得用户当前的 Money, 将Money修改为 Money+val, 同时Money+val保存入记录,做为remain
        5. 按 redveid 访问 iTRO_SocialDb.iTRO_RedPacket, 将 getuid, val 分别push到数组getuid, getAmount。
        6. 访问 iTROLogdb.iTRO_FlowLog, insert 记录。
    """
    def __init__(self, mongo, redis):
        """定义数据库连接"""
        self.redis = {
            'HOST':redis["HOST"],
            'PORT':redis["PORT"],
            'DB':redis["DB"],
            'HKEY':redis["HKEY"]
        }
        self.mongo = {
            'HOST':mongo["HOST"],
            'PORT':mongo["PORT"],
            'DBRed':mongo["DBSocial"],
            'CORed':mongo["CORed"],
            'DBLog':mongo["DBFlow"],
            'COLog':mongo["COFlow"],
            'DBUser':mongo["DBMain"],
            'COUser':mongo["COUser"],
            'dberror':mongo["DBFlow"],
            'coerror':mongo["COError"],
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
        self.logpath = 'D:/iTROLog/'

    def get_redField(self):
        """获得redis缓存中的field。"""
        from redis import Redis
        conn = Redis(host=self.redis['HOST'], port=self.redis['PORT'], db=self.redis['DB'])
        if conn.exists(self.redis["HKEY"]):
            keys = conn.hkeys(self.redis["HKEY"])
            self.result = self.result.fromkeys([i.decode() for i in keys])
            self.lognum = len(self.result)
            return True
        else:
            return False

    def get_redValue(self, field):
        """按field查询value"""
        from redis import Redis
        from json import loads
        conn = Redis(host=self.redis['HOST'], port=self.redis['PORT'], db=self.redis['DB']) 
        T = conn.hget(self.redis["HKEY"], field)
        if T != b'None':
            self.result[field] = loads(T.decode().replace("'", '"'))
            return True
        else:
            self.result[field]['msg'] = 'get value failed'
            self.to_errorlog(field)
            return False

    def get_userRemain(self, field):
        """按userid从mongodb中获得用户的余额，每次只处理一条数据, index 为result列表的索引，即处理第几条数据"""
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['DBUser'])
        coll = db.get_collection(self.mongo['COUser'])
        try:
            T = coll.find_one({'_id':ObjectId(self.result[field]['getuid'])}, {'_id':0, 'Money':1, 'UseMomey':1})
            if T:
                self.result[field]['money'] = T['Money']
                self.result[field]['usemoney'] = T['UseMomey'] + self.result[field]['val']
                # 账户余额计算：使用usemoney+amount
                self.result[field]['remain'] = T['UseMomey'] + self.result[field]['val']
                self.result[field]['msg'] = 'get remain'
                return True
            else:
                self.result[field]['msg'] = 'get remain failed'
                self.to_errorlog(field)
                return False
        except Exception as e:
            raise NameError("get_userRemain %s failed, %s" % (field,e))
        finally:
            conn.close()


    def to_userRemain(self, field):
        """
            按userid，将用户领取红包后的余额, 回写到mongodb.iTROdb.iTRO_User表中
        """
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['DBUser'])
        coll = db.get_collection(self.mongo['COUser'])
        try:
            tmp = coll.update_one(
                {'_id':ObjectId(self.result[field]['getuid'])},
                {'$inc':{'Money':int(self.result[field]['val']),
                         'UseMomey':int(self.result[field]['val'])}}
            )
            conn.close()
            if tmp.raw_result['updatedExisting']:
                return True
            else:
                self.result[field]['msg'] = 'update money failed'
                self.to_errorlog(field)
                return False
        except Exception as e:
            raise NameError("to_userRemain %s failed, %s " % (field, e))

    def to_redlog(self, field):
        """
            将记录写入 iTRO_SocialDb.iTRO_RedPacket
        """
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['DBRed'])
        coll = db.get_collection(self.mongo['CORed'])
        try:
            tmp = coll.update_one(
                filter={'$or':[{'_id':ObjectId(self.result[field]['redveid'])},
                               {'randomnum':self.result[field]['redveid']}]},
                update={'$push':{'getuid':self.result[field]['getuid'],
                                 'getAmount':int(self.result[field]['val'])}}
            )
            conn.close()
            if tmp.raw_result['updatedExisting']:
                return True
            else:
                self.result[field]['msg'] = 'write redpacket failed'
                self.to_errorlog(field)
                return False
        except Exception as e:
            raise NameError("to_redlog %s failed, %s" % (field, e))
        finally:
            conn.close()

    def to_flowlog(self, field):
        """
            访问iTROLogdb.iTRO_FlowLog, 写入金额增加记录
        """
        from pymongo import MongoClient
        from time import time
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['DBLog'])
        coll = db.get_collection(self.mongo['COLog'])
        try:
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
            return True
        except Exception as e:
            raise NameError("to_flowlog %s failed, %s" % (field, e))
        finally:
            conn.close()

    def del_redlog(self, field):
        """删除redis中RedrainGetPirce已处理的field"""
        from redis import Redis
        conn = Redis(host=self.redis['HOST'], port=self.redis['PORT'], db=self.redis['DB'])
        conn.hdel(self.redis['HKEY'], self.result[field]['rkey'])
        return True

    def to_errorlog(self, field):
        """将错误记录保存到mongodb"""
        from pymongo import MongoClient
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['dberror'])
        coll = db.get_collection(self.mongo['coerror'])
        try:
            coll.insert_one(self.result[field])
            self.result.pop(field)
            return True
        except Exception as e:
            raise NameError("to_errorlog %s failed, %s" % (field, e))
        finally:
            conn.close()

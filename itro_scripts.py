# -*- coding=utf-8 -*-

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
    pywin32(https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/)
"""
import win32serviceutil
import win32service
import win32event

class itroService(win32serviceutil.ServiceFramework):
    """配置windows服务"""
    _svc_name_ = "itroService"
    _svc_display_name_ = "itroService"
    _svc_description_ = "1. 读redis中RedrainGetPirce表中的数据，写入mongodb的iTRO_User, iTRO_RedPacket, iTRO_FlowLog; 2.查询高德云图中的过期红包数据, 并删除"

    def __init__(self, args):
        win32serviceUtil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    
    def SvcDoRun(self):
        do_scripts()
        # 等待服务停止
        win32event.WaitForSingleObject(self.HwaitStop, win32event.INFINITE)
    
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)


class itro_redpacket(object):
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
            'COUser':'iTRO_User',
            'dberror':'iTROLogdb',
            'coerror':'iTRO_redError'
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


    def do_redpacket(self):
        """
            执行红包记录处理, 每次处理5000条, 则进行一次休眠，以降低压力
            无记录则休眠60秒后再次查询
        """
        from time import sleep, time
        t = -1
        while t < 0:
            if self.get_redField():                 # 如果hash表不存在，则不继续执行
                stop = 0
                for i in self.result:
                    try:
                        self.get_redValue(i)
                        self.get_userRemain(i)
                        self.to_userRemain(i)
                        self.to_redlog(i)
                        self.to_flowlog(i)
                        self.del_redlog(i)
                    except:
                        print("id %s has error " % i)
                        self.to_errorlog(i)         # 保存错误的记录
                    finally:
                        stop += 1
                        if stop == 5000:
                            sleep(10)                # 每处理5000条记录后, 休眠10秒
                        # self.to_logfile()              # 保存处理后的数据
                        print ("%d :  log has been done" % (self.lognum))
            else:
                print("%d : %s not exists. next loop will do at 60s." % (int(time()), self.redis["HKEY"]))
                sleep(60)


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
        T = coll.find_one({'_id':ObjectId(self.result[field]['getuid'])}, {'_id':0, 'Money':1, 'UseMomey':1})
        if T:
            self.result[field]['money'] = T['Money']
            self.result[field]['usemoney'] = T['UseMomey'] + self.result[field]['val']
            self.result[field]['remain'] = T['Money'] + self.result[field]['val']
            self.result[field]['msg'] = 'get remain'
            conn.close()
            return True
        else:
            self.result[field]['msg'] = 'get remain failed'
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
            {'$set':{'Money':int(self.result[field]['remain']),
                     'UseMomey':int(self.result[field]['usemoney'])}}
        )
        conn.close()
        if tmp.raw_result['updatedExisting']:
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
            filter = {'$or':[{'_id':ObjectId(self.result[field]['redveid'])},
                             {'randomnum': self.result[field]['redveid']}]},
            update = {'$push':{'getuid':self.result[field]['getuid'],
                               'getAmount':int(self.result[field]['val'])}}
        )
        conn.close()
        if tmp.raw_result['updatedExisting']:
            return True
        else:
            self.result[field]['msg'] = 'write redpacket failed'
            self.to_errorlog(field)
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
        return True

    def to_logfile(self):
        """保存处理结果记录"""
        from time import time, localtime, strftime
        logfile = "%slog_redpacket%s.txt" % (self.logpath, strftime("%Y%m%d", localtime(time())))
        with open(logfile, 'a', encoding='utf-8') as writer:
            for i in self.result:
                writer.write(str(self.result[i])+'\n\r')
        return True
  
    def to_errorlog(self, field):
        """将错误记录保存到mongodb"""
        from time import time, localtime, strftime
        from pymongo import MongoClient
        conn = MongoClient(host=self.mongo['HOST'], port=self.mongo['PORT'])
        db = conn.get_database(self.mongo['dberror'])
        coll = db.get_collection(self.mongo['coerror'])
        coll.insert_one(self.result[field])
        conn.close()
        return True


class amap_redpacket(object):
    """删除高德云地图上的过期红包数据"""
    def __init__(self):
        """初始化"""
        self.requ_para = {
            "key":"62b8e269da435102bb4ae58661c5c729",
            "tableid":"58fda0687bbf197dd13f95cb",                           # 操作表的id
        }
        self.lognum = int(0)           # 记录数量
        self.result = []               # 记录需要处理的数据_id

    def get_redpacket(self, checktime=''):
        """
            查询过期的红包
            参考地址：http://lbs.amap.com/api/yuntu/reference/cloudsearch/?_=1504254449847
        """
        from time import time
        from urllib import request
        from json import loads
        checktime = str(int(time())) if checktime=='' else checktime
        self.requ_para['url'] = "http://yuntuapi.amap.com/datamanage/data/list"
        self.requ_para['filter'] = "OutTime:[1504340000,%s]" % checktime
        req = "%s?key=%s&tableid=%s&filter=%s" % (
            self.requ_para['url'],
            self.requ_para['key'],
            self.requ_para['tableid'],
            self.requ_para['filter']
            )
        try:
            tmp = loads(request.urlopen(req).read().decode())
            self.lognum = tmp['count']
            print ("taskAmap, get %d logs" % self.lognum)
            self.result = [i['_id'] for i in tmp['datas']]
            return True
        except:
            print("taskAmap, occured error")
            return False

    def del_redpacket(self):
        """
            按id删除高德云数据中的红包记录，注意一次最多只能删除1-50个记录
            请求地址：http://yuntuapi.amap.com/datamanage/data/delete 

            参考：http://lbs.amap.com/api/yuntu/reference/cloudstorage
        """
        from time import sleep
        from urllib import request
        from json import loads
        self.requ_para['url'] = "http://yuntuapi.amap.com/datamanage/data/delete"
        while len(self.result) > 0:
            ids = self.result[:30]
            self.requ_para['ids'] = ",".join(ids)
            req = "%s?key=%s&tableid=%s&ids=%s" % (
                self.requ_para['url'],
                self.requ_para['key'],
                self.requ_para['tableid'],
                self.requ_para['ids']
                )
            try:
                msg = loads(request.urlopen(req).read().decode())
                print("del result: %s" % msg['info'])
                del self.result[:30]
            except:
                sleep(10)
                print("del failed")
    
    def add_redids(self, idlist):
        """指定记录_id，以便测试"""
        self.result = idlist


def do_scripts():
    """执行脚本"""
    from time import sleep
    while True:
        # task1. 将redis缓存中的红包数据保存入数据库
        task = itro_redpacket()
        if task.get_redField():
            stop = 0
            for i in task.result:
                try:
                    task.get_redValue(i)
                    task.get_userRemain(i)
                    task.to_userRemain(i)
                    task.to_redlog(i)
                    task.to_flowlog(i)
                    task.del_redlog(i)
                except:
                    print("id %s has error " % i)
                    task.to_errorlog(i)         # 保存错误的记录
                finally:
                    stop += 1
                    if stop == 5000:
                        sleep(10)                # 每处理5000条记录后, 休眠10秒
                    # self.to_logfile()              # 保存处理后的数据
            print ("task redlog : %d logs has been done" % (task.lognum))
        else:
            print("task redlog : %s not exists. next loop will do at 60s." % task.redis["HKEY"])
        
        # task2, 删除高德云地图中过期的红包数据
        try:
            task = amap_redpacket()
            task.get_redpacket()
            task.del_redpacket()
            print("taskAmap has been done")
        except:
            print("taskAmap occured error")
        
        # 休眠60秒后继续执行
        sleep(60)

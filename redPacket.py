#! python3.6.1
"""
    1. redis, 47.92.72.108:6394, db0
    2. Redraingetprice, 
    3. redveid:红包ID, getuid:领取用户id, val:领取的金额,
    4. 按 getuid 访问iTROdb.iTRO_User, 获得用户当前的 Money, 将Money修改为 Money+val, 同时Money+val保存入记录,做为remain
    5. 按 redveid 访问 iTRO_SocialDb.iTRO_RedPacket, 将 getuid, val 分别push到数组getuid, getAmount。
    6. 访问 iTROLogdb.iTRO_FlowLog, insert 记录。
"""

redis = {
    'HOST':'47.92.112.56',
    'PORT':6394,
    'DB':0,
    'HKEY':'RedrainGetPirce'
}
# mongo = {
#     'HOST':'47.92.72.108',
#     'PORT':28010,
#     'DBSo':'iTRO_SocialDb',
#     'collSo':'iTRO_RedPacket',
#     'DBlog':'iTROLogdb',
#     'collLog':'iTRO_FlowLog'
# }
mongo = {
    'HOST':'localhost',
    'PORT':28010,
    'DBRed':'iTRO_SocialDb',
    'CORed':'iTRO_RedPacket',
    'DBLog':'iTROLogdb',
    'COLog':'iTRO_FlowLog',
    'DBUser':'iTROdb',
    'COUser':'iTRO_User'
}

# 获得redis中RedrainGetPirce的所有key
RESULT = r_redkey()
for i in range(len(RESULT)):
    T = RESULT[i]
    RESULT[i]['msg'] = 'initial'
    tmp = r_remain(getuid = T['getuid'])
    if tmp['msg']:
        RESULT[i]['remain'] = tmp['money']
        RESULT[i]['msg'] = 'get remain'
    else:
        RESULT[i]['msg'] = 'no users'
        continue
    if w_remain(remain=RESULT[i]['remain'], getuid=RESULT[i]['getuid']):
        RESULT[i]['msg'] = 'write remain + val'
    else:
        RESULT[i]['msg'] = 'write remain failed'
        continue
    if w_redlog(logid=RESULT[i]['redveid'], getuid=RESULT[i]['getuid'], getamount=RESULT[i]['val']):
        RESULT[i]['msg'] = 'write redlog'
    else:
        RESULT[i]['msg'] = 'write redlog failed'
        continue
    w_flowlog(getuid=RESULT[i]['getuid'], getamount=RESULT[i]['val'], remain=RESULT[i]['remain'])
    RESULT[i]['msg'] = 'write flowlog'
    # 删除redis中的记录
    d_redkey(RESULT[i]['rkey'])
    RESULT[i]['msg'] = 'del hkey'
    print('No %d log have done' % (i))


def d_redkey(field):
    """删除redis中RedrainGetPirce已处理的field"""
    from redis import Redis
    CONN = Redis(host=redis['HOST'], port=redis['PORT'], db=redis['DB'])
    CONN.hdel(name=redis['HKEY'], field)

def w_flowlog(getuid, getamount, remain):
    """访问iTROLogdb.iTRO_FlowLog, 写入金额增加记录"""
    from pymongo import MongoClient
    from bson.objectid import ObjectId
    from time import time
    CONN = MongoClient(host=mongo['HOST'], port=mongo['PORT'])
    DB = CONN.get_database(mongo['DBLog'])
    COLL = DB.get_collection(mongo['COLog'])
    tmp = CONN.insert_one({
        "userid": getuid,
        "orderid": 'red'+str(int(time())),
        "ordertype": int(2),
        "logtype": int(10501),
        # "logtype2": int(0),
        "goldtype": int(3),
        "amount": int(getamount),
        "remain": int(remain),
        "memo": "红包",
        "date": str(int(time()))
    })
    CONN.close()
    return



def r_redkey(field = ''):
    """获得redis缓存中的key, 如果没有传入field, 则返回所有的key。否则按field返回指定的hkey值。"""
    from redis import Redis
    from json import loads
    CONN = Redis(host=redis['HOST'], port=redis['PORT'], db=redis['DB'])
    if field == "":
        tmp = CONN.hgetall(redis['HKEY'])
        RESULT = []
        for i in tmp:
            RESULT.append(loads(tmp[i]))
    else:
        RESULT = loads(CONN.hget(redis['HKEY'], field))
    return RESULT

def r_remain(getuid = "58c7c51d6c6df528042e2f38"):
    """获得用户的余额"""
    from pymongo import MongoClient
    from bson.objectid import ObjectId
    CONN = MongoClient(host=mongo['HOST'], port=mongo['PORT'])
    DB = CONN.get_database(mongo['DBUser'])
    COLL = DB.get_collection(mongo['COUser'])
    T = COLL.find_one({'_id':ObjectId(getuid)},{'_id':0, 'Money':1})
    RESULT = {}
    if T:
        RESULT['msg'] = True
        RESULT['money'] = T['Money']
    else:
        RESULT['msg'] = False
        RESULT['money'] = 0
    CONN.close()
    return RESULT

def w_remain(remain, getuid = "58c7c51d6c6df528042e2f38"):
    """领取红包后的余额写入账号表，接收的remain是余额，不是增加额"""
    from pymongo import MongoClient
    from bson.objectid import ObjectId
    CONN = MongoClient(host=mongo['HOST'], port=mongo['PORT'])
    DB = CONN.get_database(mongo['DBUser'])
    COLL = DB.get_collection(mongo['COUser'])
    tmp = COLL.update_one(
        {'_id':ObjectId(T['getuid'])},
        {'$set':{'Money':int(T['remain'])}}
    )
    CONN.close()
    return (True if tmp.raw_result['updatedExisting'] else False)


def w_redlog(logid, getuid, getamount):
    """写入记录到 iTRO_SocialDb.iTRO_RedPacket """
    from pymongo import MongoClient
    from bson.objectid import ObjectId
    # 修改账号余额为领取红包后的余额, 即money+val
    CONN = MongoClient(host=mongo['HOST'], port=mongo['PORT'])
    DB = CONN.get_database(mongo['DBRed']) 
    COLL = DB.get_collection(mongo['CORed'])
    tmp = COLL.update_one(
        filter = {'$or':[{'_id':ObjectId(logid)}, {'randomnum': logid}]},
        update = {'$push':{'getuid':int(getuid), 'getAmount':int(getamount)}}
    )
    CONN.close()
    return (True if tmp.raw_result['updatedExisting'] else False)
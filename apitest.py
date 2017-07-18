#

"""
    接口测试数据添加
"""

def get_randorder(ordernum=20, days=1):
    """获得最近一天内的20条随机待发货订单"""
    import time
    from pymongo import MongoClient
    conn = MongoClient(host=conn_ali)
    db = conn.iTROdb
    coll = db.iTRO_UserChildOrder
    pipline = [
        {'$match':{
            'date':{
                '$gte':(int(time.time())-(days*86400))},
            'status':1,
            }},
        {'$sample':{'size':ordernum}},
        {'$project':{'_id':0, 'orderid':1, 'paymoney':1, 'storeid':1}}
    ]
    tmp = list(coll.aggregate(pipline))
    conn.close()
    print("get random ChildOrders : %s" %(len(tmp)))
    return(list(tmp))

def storeid2userid(storeset):
    """根据storeid查询userid"""
    from pymongo import MongoClient
    from bson.objectid import ObjectId
    conn = MongoClient(host=conn_ali)
    db = conn.iTROdb
    coll = db.iTRO_Store
    pipline = [
        {'$match':{'_id':{'$in':[ObjectId(i) for i in storeset]}}},
        {'$lookup':{
            'from':'iTRO_User',
            'localField':'UserId',
            'foreignField':'NId',
            'as':'itro_user'
        }},
        {'$project':{
            'storename':'$StoreName',
            'userid':'$itro_user._id'}}
    ]
    tmp = coll.aggregate(pipline)
    userid = {}
    for i in tmp:
        userid[str(i['_id'])] = str(i['userid'][0])
    conn.close()
    return(userid)

def push_turnorder(orderid, money, userid):
    """发起转发订单, orderid为子订单id, money为原单实收金额, userid为发起转发的商户id"""
    import json
    from urllib import request
    # 拼接转发接口
    apiurl = apihost+'api/turnorder/turnorder'
    # 构建post请求header
    head = {'Content-Type':'application/json'}
    # 构建发往商户的userid列表
    toid = []
    toid.append("5924d830048e8010f4bc909a") # db.iTRO_User.UserName:"test14"
    toid.append("58dcbf2d2c84501d45860445")  # db.iTRO_User.UserName:"test12"
    toid.append("58d88fd36c6df5176055c4b3")  # db.iTRO_User.UserName:"liuyuxuan"
    toid.append("58d894a66c6df5176055c4b4")  # db.iTRO_User.UserName:"tututu"
    toid.append("58db1cd16c6df5073025ce22")  # db.iTRO_User.UserName:"a123456"
    toid.append("58df648e6c6df54564e76dc1")  # db.iTRO_User.UserName:"qa123456"
    toid.append("58f03f98048e801390c0ed1c")  # db.iTRO_User.UserName:"plm123"
    # 使用接口将orderlist中的订单转发给toid
    body = {
        "userid": userid,
        "orderid": orderid,
        "money": money,
        "bid": toid
    }
    body = json.dumps(body)
    print(body)
    body = bytes(body, 'utf-8')
    req = request.Request(apiurl, data=body, headers=head)
    res = request.urlopen(req)
    print(res.read())




# 定义接口主机和数据库
apihost = 'http://47.92.72.108:10086/'
conn_ali = '47.92.72.108:28010'

orderlist = get_randorder(20,2)
storeid = set(i['storeid'] for i in orderlist)
userid = storeid2userid(storeid)
for i in orderlist:
    t = orderlist.index(i)
    try:
        orderlist[t]['userid']=userid[i['storeid']]
    except KeyError as error:
        print(error)
for i in orderlist:
    if 'userid' in i.keys():
        push_turnorder(i['orderid'], i['paymoney'], i['userid'])
        print("No. %d order: %s was pushed" %(orderlist.index(i), i['orderid']))



apihost = 'http://47.92.72.108:10086/'
conn_ali = '47.92.72.108:28010'
toid = []
toid.append("5924d830048e8010f4bc909a") # db.iTRO_User.UserName:"test14"
toid.append("58dcbf2d2c84501d45860445")  # db.iTRO_User.UserName:"test12"
toid.append("58d88fd36c6df5176055c4b3")  # db.iTRO_User.UserName:"liuyuxuan"
toid.append("58d894a66c6df5176055c4b4")  # db.iTRO_User.UserName:"tututu"
toid.append("58db1cd16c6df5073025ce22")  # db.iTRO_User.UserName:"a123456"
toid.append("58df648e6c6df54564e76dc1")  # db.iTRO_User.UserName:"qa123456"
toid.append("58f03f98048e801390c0ed1c")  # db.iTRO_User.UserName:"plm123"

storeid = ''
pid = ''
title = 'testhuan'
content = '测试消息20170718 10：51'

import json
from urllib import request
# 拼接转发接口
apiurl = apihost+'api/PushMessage/insertAct'
# 构建post请求header
head = {'Content-Type':'application/json'}
# 使用接口将orderlist中的订单转发给toid
body = {
    "userid": userid,
    "storeid": storeid,
    "pid": pid,
    "title": title,
    "content": content
}
body = json.dumps(body)
print(body)
body = bytes(body, 'utf-8')
req = request.Request(apiurl, data=body, headers=head)
res = request.urlopen(req)
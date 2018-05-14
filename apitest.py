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

def push_turnorder(orderid, money, userid, toidlist):
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
        "bid": toidlist
    }
    body = json.dumps(body)
    print(body)
    body = bytes(body, 'utf-8')
    req = request.Request(apiurl, data=body, headers=head)
    res = request.urlopen(req)
    print(res.read())




# 定义接口主机和数据库
toid = []
toid.append("5924d830048e8010f4bc909a") # db.iTRO_User.UserName:"test14"
# toid.append("58dcbf2d2c84501d45860445")  # db.iTRO_User.UserName:"test12"
# toid.append("58d88fd36c6df5176055c4b3")  # db.iTRO_User.UserName:"liuyuxuan"
# toid.append("58d894a66c6df5176055c4b4")  # db.iTRO_User.UserName:"tututu"
# toid.append("58db1cd16c6df5073025ce22")  # db.iTRO_User.UserName:"a123456"
# toid.append("58df648e6c6df54564e76dc1")  # db.iTRO_User.UserName:"qa123456"
# toid.append("58f03f98048e801390c0ed1c")  # db.iTRO_User.UserName:"plm123"

apihost = 'http://47.92.72.108:10086/'
conn_ali = '47.92.72.108:28010'

orderlist = get_randorder(20,3)
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



<<<<<<< HEAD
def post_push(userlist,typenum,contentstr,titlestr):
"""list接口推送消息"""
import json
from urllib import request

typenum=1
contentlist = [
    '',
    '（平台通知）金士顿官方旗舰店专场活动：天生强者，急速超频。'
    '（优惠活动）7.18游戏装备超级品类日：京东游戏装备超级品类日，开黑利器低至五折，去京东进化，与王者争霸。',
    '',
    '',
    '',
    '',
    '（活动消息）中午12：00冰爽红包天降，一大波红包等你来抢。',

]
titlelist = [
    '',
    '金士顿官方旗舰店专场活动',
    '7.18游戏装备超级品类日',
]
titlestr='type：1'
contentstr = ('title：%s, ' %(titlestr))

apihost = 'http://47.92.72.108:8082/'
apiurl =apihost+'api/Push/list'

head = {'Content-Type':'application/json'}
body = {
    'userid':toid,
    'type':typenum,
    'Contents':(
        contentlist[typenum]+','
        '"img":"/1500375154/2017071818193619.png",',
        '"link": "http://www.crelove.net/",',
        '"type": '+str(typenum)
    ),
    'tiltle':titlelist[typenum],
=======
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
>>>>>>> 54546a04be67fbb48f5b8207095ab93101284110
}
body = json.dumps(body)
print(body)
body = bytes(body, 'utf-8')
req = request.Request(apiurl, data=body, headers=head)
<<<<<<< HEAD
res = request.urlopen(req)
print(res.read())

toid = []
toid.append("5924d830048e8010f4bc909a") # db.iTRO_User.UserName:"test14"
toid.append("58f03f98048e801390c0ed1c")  # db.iTRO_User.UserName:"plm123"
toid.append("58df648e6c6df54564e76dc1")  # db.iTRO_User.UserName:"qa123456"
toid.append("58dcbf2d2c84501d45860445")  # db.iTRO_User.UserName:"test12"
toid.append("58d88fd36c6df5176055c4b3")  # db.iTRO_User.UserName:"liuyuxuan"
toid.append("58d894a66c6df5176055c4b4")  # db.iTRO_User.UserName:"tututu"
toid.append("58db1cd16c6df5073025ce22")  # db.iTRO_User.UserName:"a123456"

=======
res = request.urlopen(req)
>>>>>>> 54546a04be67fbb48f5b8207095ab93101284110

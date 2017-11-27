#coding:utf-8
"""注册测试账号"""
from pymongo import MongoClient
import uuid
import time
import bson
import requests
import json

def get_userid(start, nums):
    import uuid, time, bson
    from pymongo import MongoClient
    conn = MongoClient(host='47.92.72.108', port=28010)
    conn = conn.get_database('iTROdb')
    conn = conn.get_collection('iTRO_User')
    result = {}
    for i in range(start, start+nums):
        username = str(i)
        tmp = conn.find_one({'UserName':username},{'NickName':1})
        if not tmp:
            nickname = '测试%s' % username
            userinfo = {
                'NId':str(uuid.uuid3(uuid.NAMESPACE_DNS, username)), # UUID唯一数据
                'RoleId':'',                                  # 角色编号
                'ParentId':'',                                # 父级编号
                'UserName':username,
                'NickName':nickname,
                'UserPsw':'ETWOlU8T9f2SmhAlXY1JCA==',           # 密码te123456
                'Sex':int(1),
                'OpenId':'',
                'Unionid':'',
                'HeadimgUrl':'',
                'Webchat':'',
                'Qq':'',
                'Mobile':'',
                'Email':'',
                'IdCard':'',
                'Money':int(0),
                'IsLogin':int(1),
                'IsChat':int(1),
                'IsOnline':int(0),
                'LogitudeAndLat':'',
                'CreateDt':bson.Int64(int(time.time())),
                'UseMomey':int(0),
                'ExtendMan':'',
                'desc':'测试账号',
                'labletag':'无',
                'qrcode':'',
                'truename':'',
            }
            conn.insert_one(userinfo)
        else:
            nickname = tmp['NickName']
        result[username] = nickname
    return result

# 通过接口写入数据到108测试服务的redis缓存
def write_account(accountdict):
    import json, requests
    head = {'Content-Type':'application/json; charset=utf-8'}
    for username,nickname in accountdict.items():
        userbody = {
            "UserID": username,
            "Name": nickname,
            "Friends": [
                "我的好友",
                "itro11"
            ],
            "Signature": "Signature",
            "HeadImageIndex": 0,
            "HeadImageData": "",
            "Groups": "G123456",
            "CreateTime": 0,
            "DefaultFriendCatalog": "我的好友",
            "Version": 20
        }
        t = requests.post(url='http://192.168.5.238:30809/api/Social/addgguer', data=json.dumps(userbody), headers=head)
        if t.content == 'true':
            print('username: %s write success!' % username)
        else:
            print('username: %s write failed' % username)

if __name__ == '__main__':
    result = get_userid(10000, 10)
    write_account(result)
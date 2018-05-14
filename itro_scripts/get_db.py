# coding:utf-8
"""
    数据获取脚本，从bjd数据库中查询符合以下条件的手机号
    1、性别女
    2、年龄24-35岁
"""

dbinfo = {
    'host':'localhost',
    'port':28010,
    'db':'BJDdb',
    'collection':'BJD_chrid',
}

import pymongo
import pandas as pd
conn = pymongo.MongoClient(host=dbinfo['host'], port=dbinfo['port'])
conn = conn.get_database(dbinfo['db'])
conn = conn.get_collection(dbinfo['collection'])

tmp = conn.find(
    {
        'idcard':{'$nin':[None, '']},
        '$or':[{'tel':{'$ne':None}},{'lnktel':{'$ne':None}},{'bankmobile':{'$ne':None}}]        
    },
    {'_id':0, 'lnktruename':1, 'idcard':1, 'tel':1, 'lnktel':1, 'bankmobile':1}
)

result = []
for i in tmp:
    if len(i['idcard']) in (15,18):
        result.append(i)

for i in result:
    try:
        if len(i['idcard']) == 18:
            i['age'] = 2017-int(i['idcard'][6:10])
            i['sex'] = int(i['idcard'][16]) % 2
        elif len(i['idcard']) == 15:
            i['age'] = 100-int(i['idcard'][6:8])+17
            i['sex'] = int(i['idcard'][14]) % 2
        else:
            print(i)
    except Exception as err:
        print(i, err)

result = pd.DataFrame(result)

t = result[(result.age >= 24) & (result.age<=35) & (result.sex == 0)]

t.to_csv('phonenum.csv', encoding='utf8')


"""
    # mongodb查询示例
    db.bjd_chrid.find(
        {
            'idcard':{'$ne':null},
            '$or':[
                {'tel':{'$ne':null}},
                {'lnktel':{'$ne':null}},
                {'bankmobile':{'$ne':null}}
                ]
            
        },
        {'_id':0, 'lnktruename':1, 'idcard':1, 'tel':1, 'lnktel':1, 'bankmobile':1}
    )
"""
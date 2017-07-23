import pymssql,time
from pymongo import MongoClient


mongo_ali = '47.92.72.108:28010'

def get_userstats(datestr="2017/07/01"):
"""从mongodb查询数据"""
import pymssql,time
from pymongo import MongoClient
datestr = '2017/07/01'
datestamp = time.strptime(datestr+' 00:00:00', '%Y/%m/%d %H:%M:%S')
datestamp = int(time.mktime(datestamp))

mongo_ali = 'host':'47.92.72.108:28010'
conn = MongoClinet(mongo_ali)
db = conn.iTROdb
coll = db.iTRO_User
coll.aggregate([
    {'$match':{'_id'}}
])

conn_ali = pymssql.connect(host='192.168.5.237',
                       port='1433',
                       user='sa',
                       password='qwe123',
                       database='iTROdb')
sql = ('create table Stats_User ('
       'ID INT IDENtITY(1,1),'
       'sDate DATE,'
       'newUser INT,'
       ''
       ')'
)

sql = ('CREATE TABLE Stats_User('
        'ID INT IDENTITY(1,1),'
        'sDate DATE,'   # 日期
        'regUser INT,'  # 新增注册用户
        'newUser INT',  # 有效新增用户，注册当日有登录
        'actUser INT,'  # 活跃用户，当日有登录
        'ret1User INT,' # 次日留存用户，注册次日有登录
        'ret2User INT,' # 2日留存用户
        'ret3User INT,' # 3日留存用户
        'ret4User INT,' # 4日留存用户
        'ret5User INT,'
        'ret6User INT,'
        'ret7User INT,'
        'ret15User INT,'
        'ret30User INT,'
        'retMonthUser INT,' # 次月（自然月）留存用户
        'chargeUser INT,'   # 充值用户，对账户进行了充值
        'chargeNum INT,'    # 充值次数
        'chargement Money,'  # 充值金额
        'withdrawUser INT,' # 提现成功用户
        'withdrawNum INT,'  # 提现成功次数
        'withdrawnment INT,'    # 提现成功金额
        'onlineTime BIGINT,'    # 合计在线时长：秒
        'ACU INT,'  # 平均在线人数
        'PCU INT,'  # 最高在线人数
    ')'
)

sql = ('select * from Stats_User')

sql = ('insert into Stats_User(sDate,newUser) values("2017/07/17",1000)')
mlist = conn.cursor()
mlist.execute(sql)
mlist.fetchall()
print(conn)
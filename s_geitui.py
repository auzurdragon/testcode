#coding:utf-8

import requests
import hashlib,time

appid = 'RYTfVVM47e6Ccmj9n4GAK4'
appkey = 'J7AeVhhRoZ8QgeSzKI4kS1'
mastersecret = 'hqGEwDFfRB6BRcsgu45rI3'

# 获得口令接口
apiurl = 'https://restapi.getui.com/v1/%s/auth_sign' % appid
apiurl = 'http://www.5izan.site/test/'
# 生成签名
ts = int(time.time()*1000)
signstr = hashlib.sha256(('%s%d%s' % (appkey,ts,mastersecret)).encode()).hexdigest()

postdata = {
    'sign':signstr,
    'timestamp':str(int(time.time()*1000)),
    'appkey':appkey,
}

t = requests.post(url=apiurl, data=postdata, headers=header)

apiurl = "https://restapi.getui.com/v1/%s/push_single" % appid

data = {
    # object, 消息内容
    'message':{
        'appkey':appkey,
        'is_offline':True,
        'offline_expire_time':10000,
        'msgtype':"link"
    },
    # object, 点开通知打开网页模板
    'notification':{
        'style':{
            'type':0,
            'text':"test text",           # 通知内容
            'title':"test title",         # 通知标题
            'logo':"logo.png",            # 通知的图标名称，
            'logourl':"http://xxxx/a.png",    # 通知图标地址
            'is_ring':True,               # 是否响铃
            'is_vibrate':True,            # 是否振动
            'is_clearablee':True          # 通知是否可清除
        },
        'url':'www.baidu.com',            # url模板，必须与message.msgtype一致
        'duration_begin':'2017-03-22 11:40:00',
        'duration_end':'2017-03-23 11:40:00'
    },
    'cid':'d36f351071319fe2010719f06cc0d9c',
    'requestid':"12111111111111111111111",
}

header = {
    'Content-Type':'application/json',
}

cookie = {'Hm_lvt_4b9e0f131dc3ed28fc9e760c5f9f0725': '1508471547,1508982811,1509015982'}
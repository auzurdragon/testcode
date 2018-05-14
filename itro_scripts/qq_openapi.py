# -*- coding:utf8 -*-

"""
    腾讯开放API，[参考文档](http://wiki.open.qq.com)
    [腾讯云管理后台](https://cloud.tencent.com/)
"""
import requests, hashlib, base64, hmac
from time import time
url = 'wenzhi.api.qcloud.com'

method = 'TextKeywords'
# 密钥在腾讯云后台查看，
SecretId = 'AKIDgDA4qQjBIJ9LMGoUpywjOsAbw65ssuDL'
SecretKey = '86sSt9D6nJdlhR2RzMYbVGpERVNUdfWB'
appkey = 'DiXb4shJpXhUk3O4'
appid = '1105936441'
body = {
    'Action':method
    ,'SecretId':SecretId
    ,'Timestamp':int(time())
    ,'Nonce':345122
}

body = dict(body, ** {
    'title':'芙蓉王金盒20支装（盒）'
    ,'content':'芙蓉王金盒20支装（盒）'
})
body = dict(body, **{
    'SignatureMethod':'HmacSHA256'
})
# body = {
#     "Action" : "DescribeInstances",
#     "Nonce" : 11886,
#     "Region" : "ap-guangzhou",
#     "SecretId" : "AKIDz8krbsJ5yKBZQpn74WFkmLPx3gnPhESA",
#     "SignatureMethod" : "HmacSHA256",
#     "Timestamp" : 1465185768,
#     "InstanceIds.0" : "ins-09dx96dg"
# }
# SecretKey = 'Gu5t9xGARNpq86cd98joQYCN3Cozk1qA'
# url = 'cvm.api.qcloud.com'
body = {i:body[i] for i in sorted(body.keys())}
signstr = '&'.join(['%s=%s' % (i,str(body[i])) for i in body.keys()])
signstr = '%s%s%s?%s' % ('POST',url,'/v2/index.php',signstr)

signstr = base64.b64encode(hmac.new(bytes(SecretKey,encoding='utf8'),bytes(signstr,encoding='utf8'),digestmod=hashlib.sha256).digest())

body = dict(body, ** {
    'Signature':signstr
})

tmp = requests.post('https://%s' % url, data=body)
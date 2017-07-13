# 高德地图开放web接口

"""
    第一步，申请”web服务 API”密钥（Key）；
    第二步，拼接HTTP请求URL，第一步申请的Key需作为必填参数一同发送；
    第三步，接收HTTP请求返回的数据（JSON或XML格式），解析数据。
    如无特殊声明，接口的输入参数和输出数据编码全部统一为UTF-8。
    http://restapi.amap.com/v3/ip?ip=114.247.50.2&output=xml&key=1f5596da6d816e3112aa125f00e5dd9a
"""

def find_ip(fip='47.92.72.108'):
    from urllib import request
    import json
    keyname = 'myapp-webserver'
    key = '1f5596da6d816e3112aa125f00e5dd9a'
    gurl = 'http://restapi.amap.com/v3/ip?ip=%s&output=JSON&key=%s' %(gip,key)
    result = json.loads(request.urlopen(request.Request(gurl)).read())
    print(result)
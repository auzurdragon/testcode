# 高德地图开放web接口

"""
    第一步，申请”web服务 API”密钥（Key）；
    第二步，拼接HTTP请求URL，第一步申请的Key需作为必填参数一同发送；
    第三步，接收HTTP请求返回的数据（JSON或XML格式），解析数据。
    如无特殊声明，接口的输入参数和输出数据编码全部统一为UTF-8。
    http://restapi.amap.com/v3/ip?ip=114.247.50.2&output=xml&key=1f5596da6d816e3112aa125f00e5dd9a
"""

def ip2location(fip='47.92.72.108'):
    """查询ip"""
    from urllib import request
    import json
    # keyname = 'myapp-webserver'
    key = '1f5596da6d816e3112aa125f00e5dd9a'
    gurl = 'http://restapi.amap.com/v3/ip?key=%s&ip=%s&output=JSON' %(key, fip)
    result = json.loads(request.urlopen(request.Request(gurl)).read())
    return result


def adcode2weather(adcode='430100'):
    """根据adcode查天气"""
    from urllib import request
    import json
    key = '1f5596da6d816e3112aa125f00e5dd9a'
    gurl = ('http://restapi.amap.com/v3/weather/weatherInfo?'
            'key=%s'
            '&city=%s'
            '&extensions=all'
            '&output=json'
            %(key, adcode))
    print(gurl)
    result = json.loads(request.urlopen(request.Request(gurl)).read())
    return result['forecasts'][0]['casts']


def location2geo(address):
    """根据地址查询经纬度"""
from urllib import request
import json
key = '1f5596da6d816e3112aa125f00e5dd9a'
gurl = (u'http://restapi.amap.com/v3/geocode/geo?'
        'key=%s'
        'address=%s'
        'output=json'
        % (key, address)
)
result = request.urlopen(request.Request(gurl)).read()


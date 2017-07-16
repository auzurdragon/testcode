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
    import json
    from urllib import request
    from urllib.parse import quote
    address = '湖南省长沙市雨花区湖南商会大厦'
    key = '1f5596da6d816e3112aa125f00e5dd9a'
    gurl = ('http://restapi.amap.com/v3/geocode/geo'
            '?key=%s'
            '&address=%s'
            '&output=json'
            % (key, address)
    )
    gurl = quote(gurl, safe='/:?&=')
    tmp = json.loads(request.urlopen(request.Request(gurl)).read())
    result = []
    for i in tmp['geocodes']:
        result.append({'address':i['formatted_address'],
                    'province':i['province'],
                    'citycode':i['citycode'],
                    'city':i['city'],
                    'district':i['district'],
                    'township':i['township'],
                    'adcode':i['adcode'],
                    'street':i['street'],
                    'location':i['location'],
                    })
    return result

t = location2geo('湖南省长沙市雨花区芙蓉中路湖南商会大厦')

def citysearch(keywords, adcode='430102'):
    """查询指定城市, 按adcode可指定到区内的关键字位置。默认adcode=430111为长沙市芙蓉区"""
    import json
    from urllib import request
    from urllib.parse import quote
    key = '1f5596da6d816e3112aa125f00e5dd9a'
    gurl = ('http://restapi.amap.com/v3/place/text'
            '?key=%s'
            '&keywords=%s'
            '&city=%s'
            '&citylimit=true'
            '&output=JSON'
            %(key, keywords, adcode)
    )
    gurl = quote(gurl, safe='/:?&=')
    tmp = json.loads(request.urlopen(request.Request(gurl)).read())

def localsearch(keywords, location='112.986009,28.149427', radius='500000'):
    """按上传的地理位置，搜索周边。默认位置为商会大厦，周边1千米。最大范围不超过50千米"""
    import json
    from urllib import request
    from urllib.parse import quote
    key = '1f5596da6d816e3112aa125f00e5dd9a'
    gurl = ('http://restapi.amap.com/v3/place/around'
            '?key=%s'
            '&location=%s'
            '&keywords=%s'
            # '&city=%s ' # 可指定adcode
            '&radius=%s'
            '&sortrule=distance'
            '&offset=10'
            '&output=JSON'
            % (key, location, keywords, radius)
    )
    gurl = quote(gurl, safe='/:?&=')
    tmp = json.loads(request.urlopen(request.Request(gurl)).read())
    result = []
    for i in tmp['pois']:
        result.append({
            'name':i['name'],
            'address':i['address'],
            'location':i['location'],
            'tel':i['tel'],
            'distance':i['distance']
        })
    return result

td = localsearch('红烧肉')


http://restapi.amap.com/v3/place/around?parameters 
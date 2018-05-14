# 高德地图开放web接口

"""
    第一步，申请”web服务 API”密钥（Key）；
    第二步，拼接HTTP请求URL，第一步申请的Key需作为必填参数一同发送；
    第三步，接收HTTP请求返回的数据（JSON或XML格式），解析数据。
    如无特殊声明，接口的输入参数和输出数据编码全部统一为UTF-8。
    http://restapi.amap.com/v3/ip?ip=114.247.50.2&output=xml&key=1f5596da6d816e3112aa125f00e5dd9a
"""

class myamap(object):
    """高德地图接口"""
    def __init__(self):
        self.key = '1f5596da6d816e3112aa125f00e5dd9a'
        self.tableid = '596c2ba12376c11dab4f63c2'

    def ip2location(self, fip='47.92.72.108'):
        """查询ip"""
        from urllib import request
        import json
        # keyname = 'myapp-webserver'
        gurl = 'http://restapi.amap.com/v3/ip?key=%s&ip=%s&output=JSON' %(self.key, fip)
        result = json.loads(request.urlopen(request.Request(gurl)).read())
        return result


    def adcode2weather(self, adcode='430100'):
        """根据adcode查天气"""
        from urllib import request
        import json
        gurl = ('http://restapi.amap.com/v3/weather/weatherInfo?'
                'key=%s'
                '&city=%s'
                '&extensions=all'
                '&output=json'
                %(self.key, adcode))
        print(gurl)
        result = json.loads(request.urlopen(request.Request(gurl)).read())
        return result['forecasts'][0]['casts']


    def location2geo(self, address='湖南省长沙市雨花区湖南商会大厦'):
        """根据地址查询经纬度"""
        import json
        from urllib import request
        from urllib.parse import quote
        gurl = ('http://restapi.amap.com/v3/geocode/geo'
                '?key=%s'
                '&address=%s'
                '&output=json'
                % (self.key, address)
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

    def citysearch(self, keywords, adcode='430102'):
        """查询指定城市, 按adcode可指定到区内的关键字位置。默认adcode=430111为长沙市芙蓉区"""
        import json
        from urllib import request
        from urllib.parse import quote
        gurl = ('http://restapi.amap.com/v3/place/text'
                '?key=%s'
                '&keywords=%s'
                '&city=%s'
                '&citylimit=true'
                '&output=JSON'
                %(self.key, keywords, adcode)
        )
        gurl = quote(gurl, safe='/:?&=')
        tmp = json.loads(request.urlopen(request.Request(gurl)).read())

    def localsearch(self, keywords, location='112.986009,28.149427', radius='500000'):
        """按上传的地理位置，搜索周边。默认位置为商会大厦，周边1千米。最大范围不超过50千米"""
        import json
        from urllib import request
        from urllib.parse import quote
        gurl = ('http://restapi.amap.com/v3/place/around'
                '?key=%s'
                '&location=%s'
                '&keywords=%s'
                '&types=120100|120200|120300|130000|150000'
                # '&city=%s ' # 可指定adcode
                '&radius=%s'
                '&sortrule=distance'
                '&offset=10'
                '&output=JSON'
                % (self.key, location, keywords, radius)
        )
        gurl = quote(gurl, safe='/:?&=')
        tmp = json.loads(request.urlopen(request.Request(gurl)).read())
        result = []
for i in tmp['pois']:
    result.append({
        'name':i['name'],
        'type':i['type'],
        'typecode':i['typecode'],
        'address':i['address'],
        'location':{
            'type':'Point',
            'coordinates':[float(d) for d in i['location'].split(',')],
        },
        'tel':i['tel'],
        'distance':i['distance']
        var dataset =  
    })
        return result

    def yuntu_createmap(self, tablename='myaddress'):
        """在高德云图上创建表, POST请示"""
        import json
        from urllib import request
        from urllib.parse import urlencode
        if tablename == 'myaddress':
            print('table %s have created!' %(tablename))
            return
        head = {'Content-Type':'application/x-www-form-urlencoded'}
        body = {
            'key':self.key,
            'name':tablename, # 指定表名
        }
        body = urlencode(body)
        body = bytes(body,'utf-8')
        gurl = 'http://yuntuapi.amap.com/datamanage/table/create'
        req = request.Request(gurl, data=body, headers=head)
        result = request.urlopen(req).read().decode()
        result = eval(result)
        if result['status']==1:
            print ('Table : %s created! tableid :%s' %(tablename, result['tableid']))
            return result['tableid']
        else :
            print('Create table error: %s, infocode: %s, status: %s '
                %(result['info'], result['infocode'], result['status']))

    def yuntu_createaddress(self, in_name, in_address):
        """插入单条地址数据, 默认loctype=2，按地址输入"""
        import json
        from urllib import request
        from urllib.parse import urlencode
        gurl = 'http://yuntuapi.amap.com/datamanage/data/create'
        head = {'Content-Type':'application/x-www-form-urlencoded'}
        data = {
            '_name':in_name, # 数据名称
            # '_location':'经度,纬度'    # loctype=1时必须填入经纬度
            # 'coordtype':2  # 坐标类型,1-gps,2-autonavi,3-baidu
            '_address':in_address # 地址
        }
        # data = json.dumps(data)
        print(data)
        body = {
            'key':self.key,
            'tableid':self.tableid,
            'loctype':2, # 定位方式，缺省值1-输入经纬度，2-按标准地址格式定位‘北京市朝阳区望京阜通东大街6号院3号楼’
            'data':data
        }
        req = request.Request(gurl, data=body, headers=head)
        print(req)
        result = request.urlopen(req).read().decode()
        # result = eval(result)
        print(result)
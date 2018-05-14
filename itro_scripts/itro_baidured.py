# -*- encoding=utf-8 -*-
"""已弃用！！！删除高德云地图上的过期红包数据，只删除，不考虑退回金额的问题"""

class baidu_redpacket(object):
    """删除百度云地图上的过期红包数据"""
    def __init__(self):
        """初始化方法"""
        self.body = {
            'geotable_id':'179004',    # 表id
            'ak':'UvMU5Xjt21eZwABA4KigIPF52bi3qkPn',    # 密钥
        }
        self.result = []    # 记录需要处理的数据id

    def get_redpacket(self):
        """
            删除过期的红包，注意要使用v3版接口，不要使用v4版
            按表中的OutTime(Int64)值，小于当前时间戳的记录，则删除
            百度接口说明：(http://lbsyun.baidu.com/index.php?title=lbscloud/api/geodataV4)
            接口地址：(http://api.map.baidu.com/geodata/v4/poi/delete)
        """
        from time import time
        from urllib import request
        from json import loads
        self.body['OutTime'] = '-,%d' % int(time())


        checktime = int(time())
        checktime = str(int(time())) if checktime=='' else checktime        


delurl = 'http://api.map.baidu.com/geodata/v3/poi/delete'
body = {
    'geotable_id':'179004',    # 表id
    'ak':'UvMU5Xjt21eZwABA4KigIPF52bi3qkPn',    # 密钥
    'ids':'2397291956,2397291955'
    # 'OutTime':'-,1511506970',
    # 'is_total_del':'1'
}
requests.post(delurl, data=body).json()



findurl = 'http://api.map.baidu.com/geodata/v3/poi/list'
body = {
    'geotable_id':'179004',    # 表id
    'ak':'UvMU5Xjt21eZwABA4KigIPF52bi3qkPn',    # 密钥
    'OutTime':'1513072817,-' 
}
header = {"Content-Type":"application/x-www-form-urlencoded"}
findurl = findurl + '?' + '&'.join([('%s=%s' % i) for i in body.items()])
tmp = requests.get(findurl) 


create_url = 'http://api.map.baidu.com/geodata/v3/poi/create'
t = tmp[2]
for t in tmp:
    data = {
        'title':t['title'],
        'address':t['address'],
        'latitude':t['location'][1],
        'longitude':t['location'][0],
        'coord_type':int(1),
        'geotable_id':'179004',
        'ak':'UvMU5Xjt21eZwABA4KigIPF52bi3qkPn',
        'updatetime':t['updatetime'],
        'createtime':t['createtime'],
        'OutTime':t['OutTime'],
        'UserLogo':t['UserLogo'],
        'Method':t['Method'],
        'UserNickName':t['UserNickName'],
        'RedPacketAmount':t['RedPacketAmount'],
        'RedPacketUrl':t.get('RedPacketUrl'),
        'RedPacketId':t['RedPacketId'],
    }
    requests.post(createurl, data=data).json()




class amap_redpacket(object):
    """删除高德云地图上的过期红包数据"""
    def __init__(self):
        """初始化"""
        self.requ_para = {
            "key":"62b8e269da435102bb4ae58661c5c729",
            "tableid":"58fda0687bbf197dd13f95cb",                           # 操作表的id
        }
        self.lognum = int(0)           # 记录数量
        self.result = []               # 记录需要处理的数据_id

    def get_redpacket(self, checktime):
        """
            查询过期的红包
            参考地址：http://lbs.amap.com/api/yuntu/reference/cloudsearch/?_=1504254449847
        """
        from time import time
        from urllib import request
        from json import loads
        checktime = str(int(time())) if checktime=='' else checktime
        self.requ_para['url'] = "http://yuntuapi.amap.com/datamanage/data/list"
        self.requ_para['filter'] = "OutTime:[1504340000,%s]" % checktime
        req = "%s?key=%s&tableid=%s&filter=%s" % (
            self.requ_para['url'],
            self.requ_para['key'],
            self.requ_para['tableid'],
            self.requ_para['filter']
            )
        tmp = loads(request.urlopen(req).read().decode())
        self.lognum = tmp['count']
        self.result = [i['_id'] for i in tmp['datas']]

    def del_redpacket(self):
        """
            按id删除高德云数据中的红包记录，注意一次最多只能删除1-50个记录
            请求地址：http://yuntuapi.amap.com/datamanage/data/delete 

            参考：http://lbs.amap.com/api/yuntu/reference/cloudstorage
        """
        from time import sleep
        from urllib import request
        from json import loads
        self.requ_para['url'] = "http://yuntuapi.amap.com/datamanage/data/delete"
        while len(self.result) > 0:
            ids = self.result[:30]
            self.requ_para['ids'] = ",".join(ids)
            req = "%s?key=%s&tableid=%s&ids=%s" % (
                self.requ_para['url'],
                self.requ_para['key'],
                self.requ_para['tableid'],
                self.requ_para['ids']
                )
            try:
                msg = loads(request.urlopen(req).read().decode())
                del self.result[:30]
            except:
                sleep(10)
        return self.lognum
    
    def add_redids(self, idlist):
        """指定记录_id，以便测试"""
        self.result = idlist
# -*- coding=utf-8 -*-
"""
    阿里百川无线开放平台(http://baichuan.taobao.com/)
    账号:auzurdragon

    依赖包
    from time import time,localtime,strftime
    from hashlib import md5
    from urllib.request import Request,urlopen
    from urllib.parse import quote
"""
class TopAPI(object):
    """阿里百川openAPI"""
    def __init__(self):
        self.requ_para = {
            'app_key': '24598266',    # appKey，见控制台-应用管理
            # 'target_app_key': '',   # 被调用的目标AppKey，仅当被调用的API为第三方ISV提供时有效。
            'sign_method': 'md5',     # 是，签名的摘要算法，可选值：hmac, md5
            # 'session': '',          # 否，用户登录授权成功后，TOP颁发给应用的授权信息。
            'timestamp': '',          # 是, 时间，格式为yyyy-MM-dd HH:mm:ss，时区为GMT+8
            'format': 'json',         # 否，响应格式，默认为xml，可选值：xml, json
            'v': '2.0',               # 是, API协议版本，可选值：2.0
            # 'partner_id': '',       # 否，合作伙伴身份标识。
            # 'simplify': False,      # 否，boolean, 是否采用精简JSON返回格式，仅当format=json有效，默认值false
            'method':'',              # 是, 调用的接口名称
        }
        self.signstr = ''
        self.sign = ''                     # 保存签名
        self.app_secret = '1ff01eaddc7cfda3f9a6dbaeffba28bf'    # 保存app_secret
        self.url_http = 'http://gw.api.taobao.com/router/rest'  # 正式环境HTTP请求地址
        self.url_https = 'https://eco.taobao.com/router/rest'   # 正式环境HTTPS请求地址
        self.get_url = ''             # 保存GET请求
        self.recall = ''
        self.result = []              # 保存查询结果
        self.resultnum = int(0)       # 保存查询结果的总数量
        self.error = {}               # 保存错误信息

    # def tbk_uatm_favorites_get(self):
    #     """
    #     taobao.tbk.uatm.favorites.get (获取淘宝联盟选品库列表)
    #     """
    #     self.requ_para['method'] = 'taobao.tbk.uatm.favorites.get'
    #     self.requ_para['fields'] = 'favorites_title,favorites_id,type'
    #     self.requ_para['type'] = int(2)
    #     self.requ_para['page_no'] = int(1)
    #     # self.requ_para['page_size'] = int(20)

    def tbk_ju_tqg_get(self, stime="", etime=""):
        """
            taobao.tbk.ju.tqg.get (淘抢购api)
            http://open.taobao.com/doc2/apiDetail.htm?apiId=27543&scopeId=11483
        """
        from time import time, localtime, strftime
        stime = strftime("%Y-%m-%d %H:%M:%S", localtime(time())) if stime == "" else stime
        etime = strftime("%Y-%m-%d %H:%M:%S", localtime(time()+int(86400))) if etime == "" else etime
        self.requ_para['app_key'] = '24611799'
        self.app_secret = '254010333b0e1a3bf9e86dab399a2073'
        self.requ_para['method'] = 'taobao.tbk.ju.tqg.get'
        self.requ_para['adzone_id'] = int(130562660)
        self.requ_para['fields'] = "click_url,pic_url,reserve_price,zk_final_price,total_amount,sold_num,title,category_name,start_time,end_time"
        self.requ_para['start_time'] = stime
        self.requ_para['end_time'] = etime
        self.get_sign()
        if self.get_result():
            self.resultnum = self.recall[list(self.recall.keys())[0]]["total_results"]
            self.result = self.recall[list(self.recall.keys())[0]]['results']['results']
        else:
            print(self.error)

    def get_result(self):
        """接口查询"""
        from urllib.request import urlopen
        from urllib.parse import quote
        from json import loads
        # 根据参数和签名，拼接查询请求
        keys = self.requ_para.keys()
        self.get_url = ("%s?sign=%s&%s" % (
            self.url_http,
            self.sign,
            "&".join(["%s=%s" % (i, self.requ_para[i]) for i in keys])
        ))
        self.recall = loads(urlopen(quote(self.get_url, safe='/:?&=+')).read().decode())
        if "error_response" in self.recall.keys():
            self.error = self.recall
            return False
        else:
            return True

    def get_sign(self):
        """拼写签名"""
        from time import time, localtime, strftime
        from hashlib import md5
        # 将参数名转为ascii码，再进行排序
        self.requ_para['timestamp'] = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
        requ_keys = self.requ_para.keys()
        keys = [i.encode("ascii") for i in requ_keys]
        keys.sort()
        # 将参数名和参数值进行拼接，md5加密方法需要在拼接后的字符串首尾加上app_secret
        self.signstr = "%s%s%s" % (
            self.app_secret,
            str().join(
                ["%s%s" % (i.decode("utf_8"), self.requ_para[i.decode("utf_8")]) for i in keys]
            ),
            self.app_secret
        )
        # 将拼接后的字符串转为utf-8码，进行md5加密,然后转为16进制字符串。转换后的结果应为32位字符串
        self.sign = md5(self.signstr.encode("utf_8")).hexdigest().upper()
        return True

    def tbk_item_get(self, qword="尿不湿", itemloc="", sortmet="total_sales_des", page=int(0)):
        """
            # taobao.tbk.item.get   淘宝客商品查询
            # 接口说明(http://open.taobao.com/doc2/apiDetail.htm?apiId=24515&scopeId=11483)淘宝客商品查询
        """
        from time import time, localtime, strftime
        # 定义公共参数
        self.requ_para['timestamp'] = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
        self.requ_para['method'] = 'taobao.tbk.item.get'
        # 定义业务参数
        self.requ_para['fields'] = 'num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick'
        self.requ_para['q'] = qword
        # self.requ_para['cat'] =''           # 后台类目ID，用,分割，最大10个，该ID可以通过taobao.itemcats.get接口获取到
        self.requ_para['itemloc'] = itemloc
        self.requ_para['sort'] = sortmet  # 可选，排序_des（降序），排序_asc（升序），销量（total_sales），淘客佣金比率（tk_rate）， 累计推广量（tk_total_sales），总支出佣金（tk_total_commi）
        # self.requ_para['is_tmall'] = False,           # 可选，是否商城商品，设置为true表示该商品是属于淘宝商城商品，设置为false或不设置表示不判断这个属性
        # self.requ_para['is_overseas'] = False,        # 可选，是否海外商品，设置为true表示该商品是属于海外商品，设置为false或不设置表示不判断这个属性
        # self.requ_para['start_price'] = int(0),       # 可选，折扣价范围下限，单位：元
        # self.requ_para['end_price'] = int(0),         # 可选，折扣价范围上限，单位：元
        # self.requ_para['start_tk_rate'] = int(1234),  # 可选，淘客佣金比率上限，如：1234表示12.34%
        # self.requ_para['end_tk_rate'] = int(0),       # 可选，淘客佣金比率下限，如：1234表示12.34%
        # self.requ_para['platform'] = int(1),          # 可选，链接形式：1：PC，2：无线，默认：１
        self.requ_para['page_no'] = page                # 可选，第几页，默认：１
        self.requ_para['page_size'] = int(20)           # 可选，页大小，默认20，1~100
        self.get_sign()
        if self.get_result():
            self.resultnum = self.recall['tbk_item_get_response']['total_results']
            self.result = self.recall['tbk_item_get_response']['results']['n_tbk_item']
        else:
            print(self.error)

    def tbk_dg_item_coupon_get(self):
        """
            好券清单
            tbk.dg.item.coupon.get
        """
        self.requ_para[]

if __name__ == "__main__":
    s = TopAPI()
    s.tbk_ju_tqg_get()
    s.get_sign()
    s.get_result()

    # 淘宝客商品抓取
    url = 'https://ai.taobao.com/search/index.htm?fcat=50006004&key=宝宝用品&pid=mm_126044062_36508049_130588891'
    url = request.quote(url, safe=":/?&_")
    r = request.urlopen(url).read().decode()
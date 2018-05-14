#! coding:utf8
"""
    淘宝开放平台接口测试
"""

class opentb(object):
    """
        淘宝商家后台系统接口测试
    """
    def __init__(self, isv='auzur'):
        # 正式环境
        self.appinfo ={
            'cl':{
                'appkey':'24767371'
                ,'appsecret':'f56a756438663afbc3aea4beb75ef88b'
                ,'sessionkey':'61003161c40ae8b5d8199a0212db84454266c14733a75893002854148'
                ,'apiurl':'https://eco.taobao.com/router/rest'
                ,'adzone_id':''
                ,'pid':''
                ,'site_id':0
            },
            'clsand':{
                'appkey':'1024767371'
                ,'appsecret':'sandbox438663afbc3aea4beb75ef88b'
                ,'sessionkey':'6102b30f00c6b071168b55bff9cdd6a29daa731cf6a499f11508433'
                ,'apiurl':'https://gw.api.tbsandbox.com/router/rest'
                ,'adzone_id':''
                ,'pid':''
                ,'site_id':0
            },
            # auzurdragon网站应用
            'auzur':{
                'appkey':'24795664'
                ,'appsecret':'1cc8d454b613aa6f833e36fdf246bde8'
                ,'sessionkey':'6101706f71698c1e7526f71739a8fd7140cd9b825dd05df11508433'
                ,'apiurl':'https://eco.taobao.com/router/rest'
                ,'adzone_id':'248444921'    # pid最后一段
                ,'pid':'mm_68069173_42144173_248444921' # 网站推广位, 阿里妈妈
                ,'site_id':42144173 # 网站siteid, 阿里妈妈
            },
            'auzurapp':{
                'appkey':'24598079'
                ,'appsecret':'8f8a525b7396fbd40c6c4aa9d7f37151'
                ,'sessionkey':''
                ,'apiurl':'https://eco.taobao.com/router/rest'
                ,'adzone_id':''    # pid最后一段
                ,'pid':'' # 网站推广位, 阿里妈妈
                ,'site_id':0 # 网站siteid, 阿里妈妈                
            },
            'icsite':{
                'appkey':'24611799'
                ,'appsecret':'254010333b0e1a3bf9e86dab399a2073'
                ,'sessionkey':'61026169878567a82b06e44b16af250dfb2ef2e0d194d683401383880'
                ,'apiurl':'https://eco.taobao.com/router/rest'
                # 测试PID
                ,'adzone_id':286548053
                ,'pid':'mm_126044062_36508049_286548053'
                ,'site_id':36508049
            }
        }
        self.appkey = self.appinfo[isv]['appkey']
        self.appsecret = self.appinfo[isv]['appsecret']
        self.sessionkey = self.appinfo[isv]['sessionkey']   # 有效期一年，按app标签有效期不同
        self.api = self.appinfo[isv]['apiurl']
        self.adzone_id = self.appinfo[isv]['adzone_id']
        self.site_id = self.appinfo[isv]['site_id']
        self.pid = self.appinfo[isv]['pid']
        # 主账号沙箱:使用主账号的沙箱key和secret，通过沙箱工具获得sandbox_b_02的sessionkey
        # 沙箱账号sandbox_b_02
        # self.appkey = '1024767371'
        # self.appsecret = 'sandbox438663afbc3aea4beb75ef88b'
        # self.sessionkey = '6101014e8b1313c7c244611ff1ce5ad1d3e065c18e46ce22054718218'
        # self.api = 'https://gw.api.tbsandbox.com/router/rest'
        # 公共参数
        self.body = {
            'method':'',
            'app_key':self.appkey,
            'sign_method':'md5',
            'timestamp':'',
            'format':'json',
            'v':'2.0',
        }
        self.requirefield = {
            'status':'string, 交易状态。可选值: * TRADE_NO_CREATE_PAY(没有创建支付宝交易) * WAIT_BUYER_PAY(等待买家付款) * SELLER_CONSIGNED_PART(卖家部分发货) * WAIT_SELLER_SEND_GOODS(等待卖家发货,即:买家已付款) * WAIT_BUYER_CONFIRM_GOODS(等待买家确认收货,即:卖家已发货) * TRADE_BUYER_SIGNED(买家已签收,货到付款专用) * TRADE_FINISHED(交易成功) * TRADE_CLOSED(付款以后用户退款成功，交易自动关闭) * TRADE_CLOSED_BY_TAOBAO(付款以前，卖家或买家主动关闭交易) * PAY_PENDING(国际信用卡支付付款确认中) * WAIT_PRE_AUTH_CONFIRM(0元购合约中) * PAID_FORBID_CONSIGN(拼团中订单，已付款但禁止发货)',
            'type':'string, 交易类型列表，同时查询多种交易类型可用逗号分隔。默认同时查询guarantee_trade, auto_delivery, ec, cod的4种交易类型的数据 可选值 fixed(一口价) auction(拍卖) guarantee_trade(一口价、拍卖) auto_delivery(自动发货) independent_simple_trade(旺店入门版交易) independent_shop_trade(旺店标准版交易) ec(直冲) cod(货到付款) fenxiao(分销) game_equipment(游戏装备) shopex_trade(ShopEX交易) netcn_trade(万网交易) external_trade(统一外部交易)o2o_offlinetrade（O2O交易）step (万人团)nopaid(无付款订单)pre_auth_type(预授权0元购机交易)',
            'tid':'Number, 交易编号 (父订单的交易编号)',
            'seller_nick':'string, 卖家昵称',
            'has_buyer_message':'string, 判断订单是否有买家留言，有买家留言返回true，否则返回false',
            'payment':'string, 实付金额。精确到2位小数;单位:元。如:200.07，表示:200元7分',
            'received_payment':'string, 卖家实际收到的支付宝打款金额（由于子订单可以部分确认收货，这个金额会随着子订单的确认收货而不断增加，交易成功后等于买家实付款减去退款金额）。精确到2位小数;单位:元。如:200.07，表示:200元7分',
            'discount_fee':'string, 可以使用trade.promotion_details查询系统优惠系统优惠金额（如打折，VIP，满就送等），精确到2位小数，单位：元。如：200.07，表示：200元7分',
            'post_fee':'string, 邮费。精确到2位小数;单位:元。如:200.07，表示:200元7分',
            'total_fee':'string, 商品金额（商品价格乘以数量的总金额）。精确到2位小数;单位:元。如:200.07，表示:200元7分',
            'shipping_type':'string,创建交易时的物流方式（交易完成前，物流方式有可能改变，但系统里的这个字段一直不变）。可选值：free(卖家包邮),post(平邮),express(快递),ems(EMS),virtual(虚拟发货)，25(次日必达)，26(预约配送)。',
            'buyer_nick':'string, 买家昵称',
            'receiver_name':'string, 收货人的姓名',
            'receiver_address':'string, 收货人的详细地址',
            'receiver_state':'string, 收货人的所在省份',
            'receiver_city':'string, 收货人的所在城市',
            'receiver_district':'string, 收货人的所在地区',
            'receiver_mobile':'string, 收货人的手机号码',
            'receiver_phone':'string, 收货人的电话号码',
            'created':'Date, 交易创建时间。格式:yyyy-MM-dd HH:mm:ss',
            'pay_time':'Date, 付款时间。格式:yyyy-MM-dd HH:mm:ss。订单的付款时间即为物流订单的创建时间。',
            'modified':'Date, 交易修改时间(用户对订单的任何修改都会更新此字段)。格式:yyyy-MM-dd HH:mm:ss',
            'end_time':'Date, 交易结束时间。交易成功时间(更新交易状态为成功的同时更新)/确认收货时间或者交易关闭时间 。格式:yyyy-MM-dd HH:mm:ss',
            'orders':'list,订单列表',
        }
        self.result = []
        self.resultnum = int(0)
        self.has_next = False
    def get_sessionkey(self, code=''):
        """
            免费,不需要授权。不能输入非森比奥的账号，会提示'invalid_client'。只能使用森比奥旗舰店账号获得sessionkey
            输入code，则调用接口换取access_token；不输入code，则打印授权url。
            获得授权的access_token，即sessionkey, [参考](http://open.taobao.com/docs/doc.htm?spm=a219a.7395905.0.0.P5iZxl&docType=1&articleId=102635&treeId=1)
            1、拼接授权URL, 参数中的redirect_uri必须与应用的授权回调地址一致
            2、引导用户访问授权URL
            3、用户填入账号密码，进行授权后，会将授权码code发送到回调地址
            4、通过  taobao.top.auth.token.create  用code换取access_toke。[参考](http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.gXt2fe&source=search&apiId=25388)
            前三步操作需要回调地址接收code，本方法只演示第四步

            session获取工具：http://open.taobao.com/apitools/sessionPage.htm?spm=a219a.7629140.0.0.zBX01C
        """
        import requests
        from time import time, localtime, strftime
        if not code:
        # 拼接授权URL
            authurl = 'https://oauth.taobao.com/authorize?response_type=code&client_id=%s&redirect_uri=http://www.5izan.site/' % (self.appkey)
            # 印授权URL，访问获得code
            print(authurl)
        else:
            body = {
                'method':'taobao.top.auth.token.create',
                'app_key':self.appkey,
                'sign_method':'md5',
                'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
                'format':'json',
                'v':'2.0',
                'code':code,
            }
            body['sign'] = self.get_sign(body)
            # 该接口必须使用https接口地址访问
            tmp = requests.post(data=body, url='https://eco.taobao.com/router/rest')
            tmp = tmp.json()
            print(tmp)
            return (tmp)
    def get_sign(self, body):
        """
            生成签名字符串，同时添加timestamp
            body, 传入的参数字典
        """
        from hashlib import md5
        from time import strftime, localtime, time
        body['timestamp'] = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        keys = body.keys()
        keys = [i.encode('ascii') for i in body]
        keys.sort()
        signstr = '%s%s%s' % (
            self.appsecret,
            str().join(
                ["%s%s" % (i.decode("utf_8"), body[i.decode("utf_8")]) for i in keys]
            ),
            self.appsecret
        )
        print(signstr)
        signstr = md5(signstr.encode("utf_8")).hexdigest().upper()
        print(signstr)
        return signstr
    def post_api(self, body):
        """
            向open.taobao.com的API发送请求
        """
        import requests
        url = 'https://eco.taobao.com/router/rest'
        tmp = requests.post(url=url, data=body, timeout=5).json()
        return tmp
    def couponlink_convert(self, coupon_id, num_iid, dxjh=0):
        """
            按照优惠券id和商品id，拼接二合一链接
            coupon_id, 优惠券id, d62db1ab8d9546b1bf0ff49bda5fc33b
            num_iid, 商品id, 556633720749
            dxjh, 是否属于定向推广计划，1-是，2-否
            返回拼接后的二合一链接, link = 'http://uland.taobao.com/coupon/edetail?activityId=%s&pid=%s&itemId=%s&src=pgy_pgyqf&dx=1' % (activityid, pid, itemid)
        """
        pid = self.pid
        link = 'http://uland.taobao.com/coupon/edetail?activityId=%s&pid=%s&itemId=%s&src=pgy_pgyqf&dx=%d' % (coupon_id, pid, num_iid, dxjh)
        return link
    def trades_sold_get(self, page_no=int(1)):
        """
            获得交易订单,根据创建时间获得。
            [说明](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.ey6Qtw&apiId=46)
            method:taobao.trades.sold.get
        """
        import requests
        from time import time, localtime, strftime
        """
            tag:
            交易状态status,交易类型type,
            订单号tid,店铺名称seller_nick,买家留言has_buyer_message,
            实付金额payment,卖家实际收到的支付宝打款余额received_payment,优惠discount_fee,邮费post_fee,配送方式shipping_type,
            旺旺buyer_nick,收货人receiver_name,收货地receiver_address,收货省份receiver_state,收货手机receiver_mobile下单时间created,付款时间pay_time下单距今时间,
            订单列表orders,
            系统单号,订单备忘,快递公司,快递单号,快递成本,重量,
        """
        body = {
            'method':'taobao.trades.sold.get',
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'fields':','.join(list(self.requirefield.keys())),
            'page_no':page_no
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api)
        tmp = tmp.json()
        print(tmp)
        return(tmp)
    def trade_get(self, tid):
        """
            获得单笔交易的部分信息，性能高
            [taobao.trade.get](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.38faig&apiId=46)
            tid, 交易单号
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.trade.get',
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'fields':'tid,seller_nick,has_buyer_message, receiver_name,receiver_state,receiver_address,receiver_mobile,,type,status,payment,orders',
            'tid':int(tid),
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api)
        tmp = tmp.json()
        print(tmp)
        return (tmp)
    def trade_fullinfo_get(self, tid):
        """
            获得单笔交易的详细信息
            [taobao.trade.fullinfo.get](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.38faig&apiId=54)
            收货人等字段会有系统模糊，必须正式上线并报备才能解决，[参考](http://console.open.taobao.com/support/index.htm#/knowledge/1/15/378?_k=oy8rdv)
            [申请R2字段去模糊](http://console.open.taobao.com/support/index.htm#/knowledge/1/15/443?_k=t296w4)
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.trade.fullinfo.get',
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'fields':'tid,type,status,payment,orders, receiver_name, receiver_state, receiver_address, receiver_zip, receiver_mobile, receiver_phone,consign_time,created,pay_time,modified, end_time, buyer_message, buyer_memo,buyer_nick',
            'tid':int(tid),
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api)
        tmp = tmp.json()
        print(tmp)
        return (tmp)
    def trade_shippingaddress_update(self, tid):
        """
            更新收货地址，只允许更新发货前（等待卖家发货）交易的收货地址信息
            [taobao.trade.shippingaddress.update](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.iyxolN&apiId=241)
        """
        import requests
        from time import time, localtime, strftime 
        body = {
            'method':'taobao.trade.shippingaddress.update',
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'tid':int(tid),
            'receiver_name':'tt',
            'receiver_phone':'123456789',
            'receiver_mobile':'17712345678',
            'receiver_state':'北京',
            'receiver_city':'北京',
            'receiver_district':'朝阳区',
            'receiver_address':'大望路SOHO现代城',
            'receiver_zip':'100000',
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api)
        tmp = tmp.json()
        return tmp
    def trades_sold_increment_get(self, page_no=int(1)):
        """
            tag:基础，需要授权
            查询卖家已卖出的增量交易数据（根据修改时间）：taobao.trades.sold.increment.get
            [API说明](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.1RD76U&apiId=128)

        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.trades.sold.increment.get',
            'session':self.sessionkey,
            'start_modified':'2018-01-19 00:00:00',
            'end_modified':'2018-01-19 23:59:59',
            'use_has_next':'true',
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'fields':','.join(list(self.requirefield.keys())),
            'page_no':page_no,
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api)
        tmp = tmp.json()
        print(tmp)
        return tmp
    def save_pkl(self):
        """
            保存记录到本地，opentbtest.pkl
        """
        from pickle import dump
        with open('opentb.pkl', 'wb') as writer:
            dump(self.result, writer)
    def load_pkl(self):
        """
            从本地存档读取记录到result中
        """
        from pickle import load
        with open('opentb.pkl', 'rb') as reader:
            self.result = load(reader)
    def cainiao_waybill_ii_search(self, cp_code=''):
        """
            cainiao.waybill.ii.search, 查询面单服务订购及面单使用情况; 询面单订购关系及剩余单量情况;
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.8vKVRG&source=search&apiId=27125)
            cp_code，输入查询指定物流网点
            返回结果说明：
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'cainiao.waybill.ii.search',
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        # self.result = tmp['cainiao_waybill_ii_search_response']['waybill_apply_subscription_cols']['waybill_apply_subscription_info']
        print(tmp)
        return tmp
    def logistics_address_search(self):
        """
            taobao.logistics.address.search
            基础，需要授权，查询卖家地址库
            [说明](https://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.0a3eG3&apiId=10683)
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.logistics.address.search',
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def delivery_templates_get(self):
        """
            taobao.delivery.templates.get
            基础, 需要授权, 获取用户下所有模板
            [说明](https://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.am47oi&apiId=10916)
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.delivery.templates.get',
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'fields':'template_id,template_name,created,modified,supports,assumer,valuation,query_express,query_ems,query_cod,query_post',
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def taobao_delivery_template_get(self, template_ids='8465943921,8504415611'):
        """
            taobao.delivery.template.get
            基础,可选授权, 获取用户指定运费模板信息
            template_ids, 指定的模板id，可通过 delivery_templates_get() 查询
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.delivery.template.get', 
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'template_ids':template_ids,
            'fields':'template_id,template_name,created,modified,supports,assumer,valuation,query_express,query_ems,query_cod,query_post,address,consign_area_id,query_furniture,query_bzsd,query_wlb',
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def cainiao_cloudprint_stdtemplates_get(self):
        """
            cainiao.cloudprint.stdtemplates.get
            免费,需要授权, 获取所有的菜鸟标准电子面单模板
            [说明文档](https://open.taobao.com/docs/api.htm?spm=a219a.7629065.0.0.alDG6n&apiId=26756)
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'cainiao.cloudprint.stdtemplates.get', 
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        self.result = tmp['cainiao_cloudprint_stdtemplates_get_response']['result']['standard_template_result']
        return tmp
    def cainiao_cloudprint_mystdtemplates_get(self):
        """
            cainiao.cloudprint.mystdtemplates.get
            免费,需要授权,获取用户使用的菜鸟电子面单模板信息
            [说明文档](https://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.dZBoP9&apiId=26758)
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'cainiao.cloudprint.mystdtemplates.get', 
            'session':self.sessionkey,
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def product_get(self, product_id):
        """
            taobao.product.get
            基础,不需要授权,获取一个产品的信息
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.72JRnY&apiId=4)
            报错：ISV权限不足
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.product.get', 
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'fields':'product_id,name',
            'product_id':'536253934459',
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def item_detail_get(self):
        """
            taobao.item.detail.get
            免费,不需要授权
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.d4TUAF&apiId=28383)
            报错：ISV权限不足
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.item.detail.get', 
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'item_id':'536253934459',
            'fields':'item,price,delivery,skuBase,skuCore,trade,feature,props,debug ',
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def tbk_adzone_create(self, adzone_name, site_id=36508049):
        """
            taobao.tbk.adzone.create (淘宝客广告位创建API)
            免费, 不需要授权
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.HoPCHr&scopeId=11655&apiId=31372)
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.tbk.adzone.create', 
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'site_id': site_id,
            'adzone_name': adzone_name
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def tbk_rebate_order_get(self):
        """
            taobao.tbk.rebate.order.get (淘宝客返利订单查询)
            免费, 不需要授权
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.WPQ813&apiId=24526)
            {'error_response': {'code': 11, 'msg': 'Insufficient isv permissions', 'sub_code': 'isv.permission-api-package-limit', 'sub_msg': 'scope ids is 11655 11998', 'request_id': '2swi5veg6778'}}
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.tbk.rebate.order.get', 
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'fields':'tb_trade_parent_id,tb_trade_id,num_iid,item_title,item_num,price,pay_price,seller_nick,seller_shop_title,commission,commission_rate,unid,create_time,earning_time',
            'start_time':'2018-03-08 00:00:00',
            'span':600,
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def tbk_coupon_get(self,me):
        """
            taobao.tbk.coupon.get (阿里妈妈推广券信息查询)
            免费, 不需要授权
            me, 带券ID与商品ID的加密串 , 即通过好券清单搜索到的优惠券二合一链接中 e= 的值
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.k73JT3&scopeId=11655&apiId=31106)
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.tbk.coupon.get', 
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'me':me,        # 带券ID与商品ID的加密串
            # 'item_id':123,
            # 'activity_id':'sdfwe3eefsdf ',  # 券id
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def tbk_item_get(self):
        """
            taobao.tbk.item.get (淘宝客商品查询)
            免费, 不需要授权
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7629065.0.0.lnGVps&apiId=24515)
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.tbk.item.get', 
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'fields':'num_iid,title,pict_url,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick',
            'q':'女装',
            'sort':'tk_rate_desc',
            'start_tk_rate':1000
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def tbk_dg_item_coupon_get(self):
        """
            taobao.tbk.dg.item.coupon.get (好券清单API【导购】)
            免费, 不需要授权
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.vnGl5L&apiId=29821)
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.tbk.dg.item.coupon.get',
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'adzone_id':self.adzone_id,
            'q':'女装',
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        tmp = tmp['tbk_dg_item_coupon_get_response']['results']['tbk_coupon']
        print(tmp)
        return tmp
    def promotion_coupon_seller_search(self):
        """
            taobao.promotion.coupon.seller.search (查询绑定卖家优惠券相关信息)
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.Z2bhBS&source=search&apiId=25239)
            {'error_response': {'code': 11, 'msg': 'Insufficient isv permissions', 'sub_code': 'isv.permission-api-package-limit', 'sub_msg': 'scope ids is 381 11655 13168 11998', 'request_id': 'uv7dyjl5s8o'}}
        """
        import requests
        from time import time, localtime, strftime
        body = {
            'method':'taobao.promotion.coupon.seller.search',
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = requests.post(data=body, url=self.api).json()
        print(tmp)
        return tmp
    def tbk_item_guess_like(self):
        """
            taobao.tbk.item.guess.like (淘宝客商品猜你喜欢)
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.DqLHuW&apiId=29528)
            {'error_response': {'code': 11, 'msg': 'Insufficient isv permissions', 'sub_code': 'isv.permission-api-package-limit', 'sub_msg': 'scope ids is 381 11655 13168 11998', 'request_id': 'z27cu2w549ks'}}
        """
        body = {
            'method':'taobao.tbk.item.guess.like'
            ,'adzone_id':self.adzone_id
            ,'os':'other'  # 系统类型，ios, android, other 
            ,'ip':'192.168.0.1'  # 客户端ip 
            ,'ua':'Mozilla/5.0'  # userAgent, 例: Mozilla/5.0
            ,'net':'wifi' # 联网方式，wifi, cell, unknown 
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        tmp = self.post_api(body)
        print(tmp)
        return tmp
    def tbk_sc_material_optional(self,q='女装',cat='',page_size=20,page_no=1):
        """
        taobao.tbk.sc.material.optional (通用物料搜索API): 免费, 需要授权
        [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7629065.0.0.WE4VHD&apiId=35263&scopeId=13991)
        需要在淘宝开放后台申请'淘宝客-工具-超级搜索'权限，'i创网站'已申请, appke:24611799
        """
        body = {
            'method':'taobao.tbk.sc.material.optional'
            ,'adzone_id':self.adzone_id
            ,'site_id':self.site_id
            ,'session':self.sessionkey
            ,'q':q  # 参数q与cat不能都为空
            ,'cat':cat
            ,'page_size':page_size
            ,'page_no':page_no
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        print(body)
        tmp = self.post_api(body)
        if 'tbk_sc_material_optional_response' in tmp.keys():
            tmp = {
                'total_results':tmp['tbk_sc_material_optional_response']['total_results']   # 结果总数
                ,'page_size':page_size  # 当前页的结果数量
                ,'page_no':page_no      # 当前页数
                ,'result_list':tmp['tbk_sc_material_optional_response']['result_list']['map_data']  # 结果列表
            }
        return tmp
    def tbk_dg_material_optional(self,q='女装',cat='',page_size=20,page_no=1):
        """
            taobao.tbk.dg.material.optional (通用物料搜索API（导购）)：免费，不需要授权
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7629065.0.0.tIowFv&apiId=35896)
        """
        body = {
            'method':'taobao.tbk.dg.material.optional'
            ,'adzone_id':self.adzone_id
            ,'site_id':self.site_id
            # ,'session':self.sessionkey
            ,'q':q  # 参数q与cat不能都为空
            ,'cat':cat
            ,'page_size':page_size
            ,'page_no':page_no
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        print(body)
        tmp = self.post_api(body)
        if 'tbk_sc_material_optional_response' in tmp.keys():
            tmp = {
                'total_results':tmp['tbk_sc_material_optional_response']['total_results']   # 结果总数
                ,'page_size':page_size  # 当前页的结果数量
                ,'page_no':page_no      # 当前页数
                ,'result_list':tmp['tbk_sc_material_optional_response']['result_list']['map_data']  # 结果列表
            }
        return tmp

    def kelude_aps_ai_outer_extractkeyword(self, title='芙蓉王红盒20支装（盒）', content='芙蓉王红盒20支装（盒）湖南中烟工业有限责任公司', top_size=3,):
        """
            taobao.kelude.aps.ai.outer.extractkeyword (提取关键词)：免费, 不需要授权, 测试
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.BA8qUB&source=search&apiId=28770)
            {'error_response': {'code': 11, 'msg': 'Insufficient isv permissions', 'sub_code': 'isv.permission-api-package-limit', 'sub_msg': 'scope ids is 381 11655 13168 11998', 'request_id': '2f97btmp4g4b'}}
        """
        body = {
            'method':'taobao.kelude.aps.ai.outer.extractkeyword'
            ,'access_key':32
            ,'title':title
            ,'content':content
            ,'top_size':top_size
            # ,'params':{'ParamMap':{
            #     'apply_synony':False
            #     ,'new_term':False
            #     ,'depend':False
            #     ,'type':'apsfeedback'
            # }}
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        print(body)
        tmp = self.post_api(body)
        return tmp
    def nlp_word(self, content='精品芙蓉王红盒20支装（盒）湖南中烟工业有限责任公司'):
        """
            taobao.nlp.word (文本语言词法分析)：免费, 不需要授权, 测试。提供文本语言处理中的词法分析功能,开放中文分词和词权重计算功能。
            [说明文档](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.yqUa82&scopeId=11750&apiId=26129)
            注意：text参数需要转为字符串才能正常使用
        """
        import json
        body = {
            'method':'taobao.nlp.word'
            ,'w_type':1
            ,'text':json.dumps({
                'id':123
                ,'content':content
                ,'type':1
            })
        }
        body = dict(self.body, ** body)
        body['sign'] = self.get_sign(body)
        print(body)
        tmp = self.post_api(body)
        return tmp

if __name__ == '__main__':
    s = opentb('auzurapp')
    print(s.nlp_word())
# 阿里百川无线开放平台(http://baichuan.taobao.com/)
# 账号:auzurdragon

# sign签名方法
"""
    对所有API请求参数（包括公共参数和业务参数，但除去sign参数和byte[]类型的参数），根据参数名称的ASCII码表的顺序排序。如：foo=1, bar=2, foo_bar=3, foobar=4排序后的顺序是bar=2, foo=1, foo_bar=3, foobar=4。
    将排序好的参数名和参数值拼装在一起，根据上面的示例得到的结果为：bar2foo1foo_bar3foobar4。
    把拼装好的字符串采用utf-8编码，使用签名算法对编码后的字节流进行摘要。如果使用MD5算法，则需要在拼装的字符串前后加上app的secret后，再进行摘要，如：md5(secret+bar2foo1foo_bar3foobar4+secret)；如果使用HMAC_MD5算法，则需要用app的secret初始化摘要算法后，再进行摘要，如：hmac_md5(bar2foo1foo_bar3foobar4)。
    将摘要得到的字节流结果使用十六进制表示，如：hex(“helloworld”.getBytes(“utf-8”)) = “68656C6C6F776F726C64”
"""

# 公共请求参数
PUBLIC_PARAMETERS = {
    APP_KEY = '24598079'    # appKey，见控制台-应用管理
    APP_SECRET = '8f8a525b7396fbd40c6c4aa9d7f37151' # 同上
    URL_HTTP = 'http://gw.api.taobao.com/router/rest'   # 正式环境HTTP请求地址
    URL_HTTPS = 'https://eco.taobao.com/router/rest'    # 正式环境HTTPS请求地址
    METHOD = ''         # 是，API接口名称
    TARGET_APP_KEY = '' # 否，被调用的目标AppKey,仅当被调用的API为第三方ISV提供时有效。
    SIGN_METHOD = ''    # 是，签名的摘要算法，可选值：hmac, md5
    SIGN = ''           # 是，API输入参数签名结果
    SESSION = ''        # 否，用户登录授权成功后，TOP颁发给应用的授权信息。
    TIMESTAMP = ''      # 是, 时间，格式为yyyy-MM-dd HH:mm:ss，时区为GMT+8
    FORMAT = 'json'     # 否，响应格式，默认为xml，可选值：xml, json
    V = ''              # 是, API协议版本，可选值：2.0
    PARTNER_ID = ''     # 否，合作伙伴身份标识。
    SIMPLIFY = False    # 否，boolean, 是否采用精简JSON返回格式，仅当format=json有效，默认值false
}
# taobao.itemcats.get   获取后台供卖家发布商品的标准商品类目
# 接口说明(http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.6cMDin&source=search&apiId=122)
# 收费接口，需要高级权限，

def tb.itemcats.get():
    """
        类目API，淘宝类目ID查询
    """
    PUBLIC_PARAMETERS['METHOD'] = 'method=taobao.itemcats.get'
    PUBLIC_PARAMETERS['TIMESTAMP'] = '2017-08-25+11:59:A29'

# taobao.tbk.item.get (淘宝客商品查询)
# 接口说明(http://open.taobao.com/doc2/apiDetail.htm?apiId=24515&scopeId=11483)

PUBLIC_PARAMETERS['METHOD'] = 'method=taobao.tbk.item.get'
PUBLIC_PARAMETERS['TIMESTAMP'] = '2017-08-25+11:59:A29'




CIDS = (18957, 19562)       # 任选,商品所属类目ID列表, 用','分隔, cids和parent_cid至少传一个
FIELDS = (                  # 可选,需要返回的字段列表, 见itemCat, 默认返回cid,parent_cid,name,is_parent
    'cid,'                  # 
    'parent_cid,'
    'name,'
    'is_parent'
)
PARENT_CID = 0       # 父商品类目ID，0-根节点,返回所有子类目。
parameters = {
    'method':'taobao.itemcats.get',
    'app_key':APP_KEY,
    'sign_method':'md5',
    'timestamp':'2017-08-24 17:54:37',
    'format':'json',
    'v':'2.0',
    'fields':'cid,parent_cid,name,is_parent',
    'parent_cid':0
}
keys = []
[keys.append(i.encode('ascii')) for i in parameters.keys()]
keys.sort()
sign = "%s%s%s" % (APP_SECRET,
    str().join('%s%s' % (i.decode(), parameters[i.decode()]) for i in keys),
    APP_SECRET
)
sign.decode()
s = hashlib.md5(sign.encode()).hexdigest().upper()
gurl = ('%s?sign=%s'
        '&%s'
        % (URL_HTTP, s, 
            str('&').join('%s=%s' % (i, parameters[i]) for i in parameters.keys()))
)



# 响应参数
last_modified,      # Date,最近修改时间
item_cats:{         # 增量类目信息
    cid,            # 商品所属类目ID
    parent_cid,     # Number, 父类目ID=0时，代表1级类目
    name,           # String, 类目名称
    is_parent,      # Boolean, 该类目是否为父类目
    status,         # String, 状态
    sort_order      # Number, 排列序号
},
features:{          # Object,目前已有的属性
    attr_key,       # String,属性键
    attr_value,     # String,属性值
},
taosir_cat          # Boolean, 是否度量衡类目



# 无线开放百川淘客API
# taobao.tbk.item.get 	淘宝客商品查询
# taobao.tbk.item.recommend.get 	淘宝客商品关联推荐查询
# taobao.tbk.ju.tqg.get 	淘抢购api

# appName:万事屋3345



# taobao.tbk.item.get 	淘宝客商品查询
FIELDS = (                  # 需要返回的字段列表
    'num_iid,'              # Number,商品ID
    'title,'                # String,商品标题
    'pict_url,'             # String,商品主图
    'small_images,'         # Array,商品小图列表
    'reserve_price,'        # String,商品一口价
    'zk_final_price,'       # String,商品折扣价格
    'user_type,'            # Number,卖家烦死，0-集市，1-商城
    'provcity,'             # String,宝贝所在地
    'item_url,'             # String,商品地址
    'seller_id,'            # Number,卖家ID
    'volume,'               # Number,30天销量
    'nick'                  # string,卖家昵称
)
Q = ''                      # String,与cat二选一，查询词
CAT = ''                    # String,后台类目ID，用','分割，最多10个，可通过taobao.itemcats.get接口获取
ITEMLOC = '长沙'            # String,所在地
SORT = 'tk_rate_des'        # String,排序_排序_des（降序），排序_asc（升序），销量（total_sales），淘客佣金比率（tk_rate）， 累计推广量（tk_total_sales），总支出佣金（tk_total_commi）
IS_TMALL = False            # Boolean,可选,是否商城商品,false表示不判断
IS_OVERSSEAS = False        # Boolean,可选,是否海外商品
START_PRICE = 10            # Number,可选,折扣价范围下限,单位：元
END_PRICE = 10              # Number,可选,折扣价范围上限，单位：元
START_TK_RATE = 123         # Number,可选,淘客佣金比率上限，1234即12.34%
END_TK_RATE = 123           # Number,可选,淘客佣金比率下限
PLATFORM = 1                # Number,可选,链接形式, 1-PC, 2-无线
PAGE_NO = 0                 # Number,可选,第几页
PAGE_SIZE = 20              # Number,可选,页大小, 1~100

# 响应参数
# results, 淘宝客商品
# total_results, 搜索到符合条件的结果总数



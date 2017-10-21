-- 日常数据统计表
CREAtE TABLE itro_dailystat
(
    tid INT IDENTITY(1,1),
    sdate DATE NOT NULL,    -- 日期
    splat TINYINT NOT NULL, -- 0 全部平台; 10 iOS; 20 Android
    totaluser INT DEFAULT(0),   -- 累计用户
    newuser INT DEFAULT(0),    -- 新注册账号
    newstore INT DEFAULT(0),   -- 新开通店铺，以完成保证金订单为准
    loginuser INT DEFAULT(0),  -- 登录账号数量
    loginip INT DEFAULT(0),    -- 登录IP数
    loginnum INT DEFAULT(0),   -- 登录记录数
    chargenum INT DEFAULT(0),  -- 充值成功的记录数
    chargesum BIGINT DEFAULT(0),   -- 充值成功的金额合计，分
    chargeuser INT DEFAULT(0), -- 充值成功的账号数
    mallview INT DEFAULT(0),   -- 商城页面的浏览总数，不区分店铺或商品，即浏览记录数
    storeview INT DEFAULT(0),  -- 店铺页面的浏览总数
    topstore NVARCHAR(255) DEFAULT(NULL), -- 店铺浏览次数最TOP10，以|分隔
    waresview INT DEFAULT(0),  -- 商品页面的浏览总数
    topwares NVARCHAR(255) DEFAULT(NULL),    -- 商品浏览次数TOP10，以|分隔
    PRIMARY KEY (tid)
)

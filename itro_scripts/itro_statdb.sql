SELECT * FROM itro_dailystat

SELECT * FROM dbo.GGUser

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
Friends
DefaultFriendCatalog


INSERT INTO itro_dailystat (splat,chargenum,chargesum,chargeuser,loginip,loginnum,loginuser,mallview,newstore,newuser,sdate,storeview,topstore,topwares,totaluser,waresview) 
VALUES (0,0,0,0,1,41,16,13,2,24,'2017-10-10',7,'59db408fd700dc0efcf6ac13|59db3f94d700dc0efcf6ab69|596c1929048e800f281c903e|59dcaf79d700dc16c4920820|58d078236c6df51fe06a6bb5|59db3bbad700dc0efcddf0f1|59dc739bd700dc16c4c58710','59db408fd700dc0efcf6ac13|59db3f94d700dc0efcf6ab69|596c1929048e800f281c903e|59dcaf79d700dc16c4920820|58d078236c6df51fe06a6bb5|59db3bbad700dc0efcddf0f1|59dc739bd700dc16c4c58710',38,6)

INSERT INTO dbo.GGUser(UserID,Name,PasswordMD5,Friends,Signature,HeadImageIndex,Groups,CreateTime,DefaultFriendCatalog,Version)
VALUES ('10008','huang','c4ca4238a0b923820dcc509a6f75849b','我的好友:10001,10002,10003','每一天',0,'G001,G002',GETDATE(),'',20)




USE iTROStatisticLogDB
GO

--用户登录统计日志表
CREATE TABLE iTRO_UserLoginLog_201710
(
    Id INT IDENTITY(1,1) PRIMARY KEY,--主键Id
	UserId NVARCHAR(24) NOT NULL,--用户ID
	ChannelCode NVARCHAR(100) DEFAULT('other'),--渠道编码
	EquipmentType NVARCHAR(100) NULL,--设备类型
	[Version] NVARCHAR(15),--版本号
	DeviceCode NVARCHAR(40),--设备号
	IP NVARCHAR(40),--ip
	IpAddr NVARCHAR(100),--ip实际地址
	LoginTime BIGINT DEFAULT(0),--时间戳
	Location NVARCHAR(100),--经纬度
	Stype INT,--0新用户 1老用户
	[Online] INT --在线时长
)
GO
--用户充值日志表
CREATE TABLE iTRO_RechargeLog_201710
(
	Id INT IDENTITY(1,1) PRIMARY KEY,--主键Id
	UserId NVARCHAR(24) NOT NULL,--用户ID
	RechargeCode INT ,--充值渠道 1.微信 2.支付宝 3.银联
	RechargeMoney BIGINT,--充值金额，单位分
	ChannelCode NVARCHAR(100) DEFAULT('other'),--渠道编码
	EquipmentType NVARCHAR(100) NULL,--设备类型
	[Version] NVARCHAR(15),--版本号
	DeviceCode NVARCHAR(40),--设备号
	IP NVARCHAR(40),--ip
	IpAddr NVARCHAR(100),--ip实际地址
	Dates BIGINT DEFAULT(0),--时间戳
	Bank NVARCHAR(100)--银行 当充值渠道为3时，显示充值银行名称，其它""
)
GO
--用户注册日志表
CREATE TABLE iTRO_RegisterLog_201710
(
	Id INT IDENTITY(1,1) PRIMARY KEY,--主键Id
	UserId NVARCHAR(24) NOT NULL,--用户ID
	EquipmentType NVARCHAR(100) NULL,--设备类型
	[Version] NVARCHAR(15),--版本号
	DeviceCode NVARCHAR(40),--设备号
	IP NVARCHAR(40),--ip
	IpAddr NVARCHAR(100),--ip实际地址
	Dates BIGINT DEFAULT(0),--注册时间戳
	Location NVARCHAR(100)--经纬度
)
GO
--用户发布日志表
CREATE TABLE iTRO_PublishLog_201710
(
	Id INT IDENTITY(1,1) PRIMARY KEY,--主键Id
	UserId NVARCHAR(24) NOT NULL,--用户ID
	ChannelCode NVARCHAR(100) DEFAULT('other'),--渠道编码
	EquipmentType NVARCHAR(100) NULL,--设备类型
	[Version] NVARCHAR(15),--版本号
	DeviceCode NVARCHAR(40),--设备号
	IP NVARCHAR(40),--ip
	IpAddr NVARCHAR(100),--ip实际地址
	Dates BIGINT DEFAULT(0),--时间戳
	Location NVARCHAR(100),--经纬度
	Stype INT,--1.约会 2.订单 3.口令红包 4.消息
	Deposit BIGINT DEFAULT(0)--押金 发布约会使用
)
GO
--用户支付时提交订单日志表
CREATE TABLE iTRO_SubmitOrderLog_201710
(
	Id INT IDENTITY(1,1) PRIMARY KEY,--主键Id
	UserId NVARCHAR(24) NOT NULL,--用户ID
	ChannelCode NVARCHAR(100) DEFAULT('other'),--渠道编码
	EquipmentType NVARCHAR(100) NULL,--设备类型
	[Version] NVARCHAR(15),--版本号
	DeviceCode NVARCHAR(40),--设备号
	IP NVARCHAR(40),--ip
	IpAddr NVARCHAR(100),--ip实际地址
	Dates BIGINT DEFAULT(0),--时间戳
	Location NVARCHAR(100)--经纬度
)
GO

CREATE TABLE iTRO_ARPacket_201710
(
	Id INT IDENTITY(1,1) PRIMARY KEY,--主键Id
	UserId NVARCHAR(24) NOT NULL,--用户ID
	EquipmentType NVARCHAR(100) NULL,--设备类型
	[Version] NVARCHAR(15),--版本号
	DeviceCode NVARCHAR(40),--设备号
	IP NVARCHAR(40),--ip
	IpAddr NVARCHAR(100),--ip实际地址
	Dates BIGINT DEFAULT(0),--时间戳
	Location NVARCHAR(100),--经纬度
	RedPacketSumMoney BIGINT DEFAULT(0),--红包总金额
	RedPacketCount INT--红包总个数
)
GO

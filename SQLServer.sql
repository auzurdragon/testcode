# 连接SQLSERVER
tsql -H 192.168.5.237 -p 28010 -U han -P 12345678 -D iTRO

-- 查询所有数据库名称
SELECT Name FROM Master..SysDatabases ORDER BY Name
-- 连接数据库
USE <DATABASE NAME>
-- 查询所有表名
SELECT Name FROM SysObjects Where XType='U' ORDER BY Name


-- iTRO平台日常统计表
CREATE TABLE Stats_User(
    SID INT IDENTITY(1,1),
    sDate DATE NOT NULL,   --日期
    platform TINYINT NOT NULL,  -- 设备类型，0-全部, 1-PC, 10-Mobile, 11-Android,12-iOS
    regUser INT NOT NULL DEFAULT 0,  --新增注册用户
    newUser INT NOT NULL DEFAULT 0,  --有效新增用户，注册当日有登录
    actUser INT NOT NULL DEFAULT 0,  --活跃用户，当日有登录
    ret1User INT NOT NULL DEFAULT 0, --次日留存用户，注册次日有登录
    ret2User INT NOT NULL DEFAULT 0, -- 2日留存用户
    ret3User INT NOT NULL DEFAULT 0, -- 3日留存用户
    ret4User INT NOT NULL DEFAULT 0, -- 4日留存用户
    ret5User INT NOT NULL DEFAULT 0,
    ret6User INT NOT NULL DEFAULT 0,
    ret7User INT NOT NULL DEFAULT 0,
    ret15User INT NOT NULL DEFAULT 0,
    ret30User INT NOT NULL DEFAULT 0,
    retMonthUser INT NOT NULL DEFAULT 0, -- 次月（自然月）留存用户
    chargeUser INT NOT NULL DEFAULT 0,   -- 充值用户，对账户进行了充值
    chargeNum INT NOT NULL DEFAULT 0,    -- 充值次数
    chargement Money NOT NULL DEFAULT 0,  -- 充值金额
    withdrawUser INT NOT NULL DEFAULT 0, -- 提现成功用户
    withdrawNum INT NOT NULL DEFAULT 0,  -- 提现成功次数
    withdrawnment INT NOT NULL DEFAULT 0,    -- 提现成功金额
    onlineTime BIGINT NOT NULL DEFAULT 0,    -- 合计在线时长：秒
    ACU INT NOT NULL DEFAULT 0,  -- 平均在线人数
    PCU INT NOT NULL DEFAULT 0,  -- 最高在线人数
    PRIMARY KEY NONCLUSTERED(SID)
)
CREATE CLUSTERED INDEX Stats_User_CLUINDEX ON Stats_User(sDate DESC, platform)

-- 帐号注册表
CREATE TABLE iTRO_regUser(
    SID BIGINT IDENTITY(1,1),
    userId VARCHAR(24) NOT NULL,    -- 帐号的objectId
    userName NVARCHAR(30) NOT NULL,
    nickName NVARCHAR(30) NOT NULL,
    createDate DATE,
    platform TINYINT,
    extendMan VARCHAR(24)
    PRIMARY KEY NONCLUSTERED (userId)
)
CREATE CLUSTERED INDEX iTRO_regUser_CLUINDEX ON iTRO_regUser(userId)

-- 帐号登录表
CREATE TABLE iTRO_loginUser(
    SID BIGINT IDENTITY(1,1),
    loginDate DATE NOT NULL,
    userId VARCHAR(24) NOT NULL,
    loginNum INT,
    onlineSec INT,
    PRIMARY KEY NONCLUSTERED (SID)
)
CREATE CLUSTERED INDEX iTRO_loginUser_CLUINDEX ON iTRO_loginUser(loginDate,userId)
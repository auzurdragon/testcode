-- 云仓分销：推广返利统计脚本
ALTER PROC P_TuiGuangFanLi AS
-- 云仓分销：推广返利统计脚本
-- 创建时间：2018-03-02
-- 创建者：胡岸
-- P_TuiGuangFanLi.sql

-- 推广返利：新注册用户，在注册30天内的已发货订单，按总裁拿货价计算金额合计后，返利给注册用户的父级用户。
-- 1. 查询30天前注册的用户，及其父用户ID。新注册的账号UserId, 以及其ParentId( not in (0, 38))。返利给其ParentId。
-- 2. 销售订单的单种商品数量 sizeinfo.pronum * 该商品的总裁拿货价 product_price_setting.get_price( grade = 1), 金额合计 * 返利比例 0.01
-- 3. 订单统计周期为注册之日起到脚本执行时间，即注册用户的所有订单。
-- 注意事项：1. 返利类型为1；2.返利是给到注册用户的父级推广员，不是给注册用户

-- 关联表：Fx_FanliChangeLog， 记录返利日志，类型为1。 Fx_UserFanli，记录用户返利余额
BEGIN
    -- 计算注册日期
    DECLARE @st NVARCHAR(23), @et NVARCHAR(23)
    SET @st = CONVERT(NVARCHAR(10), DATEADD(DAY, -30,GETDATE()), 120)
    SET @et = @st + ' 23:59:59.997'
    SET @st = @st + ' 00:00:00'
    -- -- 指定返利订单的结束日期
    -- DECLARE @ot NVARCHAR(23)
    -- SET @ot = CONVERT(NVARCHAR(10), DATEADD(DAY, -1,GETDATE()), 120) + ' 23:59:59.997'

    -- 返利比例， 返利数量 = 返利金额 * 返利比例
    DECLARE @rate FLOAT(2)
    SET @rate = 0.01

    -- 临时表, 计算用户的返利金额, group by userid
    DECLARE @ut TABLE
    (
        userid INT                  -- 新注册的用户ID
        ,parentid INT               -- 其父级ID
        ,onum INT                   -- 每个userid包含的订单数量
        ,pricesum INT               -- 计算返利的订单金额合计值
        ,tgfanli DECIMAL(18,2)      -- 返利的数量
        ,fanliinit DECIMAL(18,2)    -- 返利前的返利余额
        ,fanliremain DECIMAL(18,2)  -- 返利后的返利余额
    )
    -- 临时算，保存注册用户的订单记录, group by userid,oid
    DECLARE @ordert TABLE
    (
        userid INT      -- 新注册的用户ID
        ,oid INT        -- 30天内的已发货订单id
        ,pnum INT       -- 每个oid包含的pid数量
        ,pricesum INT   -- 按oid汇总的返利金额合计
    )
    -- 临时表，保存注册用户的订单pid和pronum信息,group by userid,pid
    DECLARE @prot TABLE
    (
        oid INT         -- 订单id
        ,pid INT        -- 订单包含的商品id
        ,pronum INT     -- 每个pid对应的商品数量
        ,getprice INT   -- 每个pid对应的总裁拿货价
        ,pricesum AS pronum * getprice -- 返利金额，商品数量pronum * 总裁拿货价getprice
    )

    -- 查询指定日期注册的账号UserId
    INSERT INTO @ut(userid)
    SELECT Id FROM Fx_UsersBase WHERE [Date] BETWEEN @st AND @et

    -- 查询注册用户的父ID, 排除父ID 0 or 38 的注册用户
    UPDATE A SET A.parentid = B.ParentId
    FROM @ut AS A INNER JOIN Fx_UserAsset AS B ON A.userid = B.UserId
    WHERE B.ParentId not in (0, 38)

    -- 删除不符合条件的账号
    DELETE FROM @ut WHERE parentid IS NULL

    -- 如果账号数量为零，则跳出脚本，不继续执行
    IF NOT EXISTS (SELECT 1 FROM @ut)
    BEGIN
        RAISERROR ('没有符合条件的新增注册用户', 16, 1)
        RETURN
    END

    -- 查询注册用户在指定日期前的已发货订单编号,保存入临时表
    INSERT INTO @ordert(userid, oid)
    SELECT A.userid, B.Id 
    FROM @ut AS A INNER JOIN Fx_Orders AS B ON A.userid = B.UserID 
    -- WHERE B.OrderTime <= @ot AND B.OrderStatus = 2

    -- 如果订单数量为零，则跳出脚本，不继续执行
    IF NOT EXISTS (SELECT 1 FROM @ordert)
    BEGIN
        RAISERROR ('没有符合条件的用户订单', 16, 2)
        RETURN
    END

    -- 查询订单对应的子单商品数量
    INSERT INTO @prot(oid, pid, pronum)
    SELECT A.oid, b.PId, SUM(ProNum) as pronum
    FROM @ordert AS A LEFT JOIN Fx_Order_SizeInfo AS B ON A.oid = B.OrderId
    GROUP BY A.oid, b.PId

    -- 查询每个pid对应的总裁拿货价，保存入临时表
    UPDATE A SET A.getprice = B.GetPrice
    FROM @prot AS A LEFT JOIN Fx_Product_Price_Setting AS B ON A.pid = B.ProductId
    WHERE B.GradeId = 1

    -- 统计每个oid下的所有pid返利金额合计，保存入上级临时表
    UPDATE A SET A.pricesum = B.pricesum, A.pnum = B.pnum
    FROM @ordert AS A 
    LEFT JOIN (
        SELECT oid, COUNT(1) AS pnum, SUM(pricesum) AS pricesum FROM @prot GROUP BY oid
    ) AS B ON A.oid = B.oid

    -- 统计每个userid下所有oid的返利金额合计，保存入上级临时表
    UPDATE A SET A.pricesum = B.pricesum, A.onum = B.onum
    FROM @ut AS A LEFT JOIN (
        SELECT userid, COUNT(1) AS onum, SUM(pricesum) AS pricesum FROM @ordert GROUP BY userid
    ) AS B ON A.userid = B.userid

    -- 删除无订单的userid记录
    DELETE FROM @ut WHERE pricesum IS NULL

    -- 统计每个userid应得的推广返利数量，保存入临时表
    UPDATE @ut SET tgfanli = pricesum * @rate

    -- 查询父级用户的当前返利余额
    UPDATE A SET A.fanliinit = ISNULL(B.FanliRemain, 0)
    FROM @ut AS A LEFT JOIN Fx_UserFanli AS B ON A.parentid = B.UserId

    -- 计算返利后的返利余额
    UPDATE @ut SET fanliremain = fanliinit + tgfanli

    -- 保存记录到返利变化表，推广返利记录moneytype=1
    INSERT INTO Fx_FanliChangeLog (UserId, MoneyPoint, MoneyType, DTime)
    SELECT parentid, tgfanli, 1 AS MoneyType, GETDATE() AS DTime 
    FROM @ut ORDER BY parentid

    -- 保存返利后的余额到用户返利余额表,先更新Fx_UserFanli 中已存在的UserId 记录
    UPDATE A SET A.FanliRemain = B.fanliremain
    FROM Fx_UserFanli AS A INNER JOIN @ut AS B ON A.UserId=B.parentid
    -- 再补充之前没有记录的USERID
    INSERT INTO Fx_UserFanli(UserId, FanliRemain)
    SELECT B.parentid, B.fanliremain 
    FROM @ut AS B 
    WHERE NOT EXISTS (SELECT 1 FROM Fx_UserFanli WHERE UserId=B.parentid)

    SELECT * FROM @ut ORDER BY userid
    RETURN
END
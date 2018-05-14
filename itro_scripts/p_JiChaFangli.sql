-- 统计七天前的订单用户+按当前时间计算父级用户，可能会出现用户在七天内升级到与父级同级，父级多得平级返利的状态。
-- 用户在七天内超过父级的等级，父级将获得不到返利。
-- 吴总下属的用户（UserId=496, grade=7)是否给吴总计算级差和平级返利。
-- 20180315：改为按订单操作，以避免跨时间级别变化的问题
-- 等级树上出现多个平级的问题。

--测试OrderId : 201700000511,201700000564,201700001085,201700001227,201700001231


DECLARE @orderid NVARCHAR(15)
SET @orderid = '201700001085'

DECLARE @oid BIGINT, @userid INT, @puser INT

-- 设置级差返利比例
DECLARE @rate FLOAT(2)

SET @rate = 0.01 

DECLARE @usert TABLE(
    cuser INT
    ,cgrade INT
    ,puser INT
    ,sumprice INT
    ,jicha FLOAT(2)
)

DECLARE @pronumt TABLE(
    pid INT
    ,pronum INT
)

DECLARE @prot TABLE(
    grade INT
    ,sumprice INT
)

-- 按订单id查询用户id和oid信息，保存入变量
SELECT @oid = Id, @userid = UserId FROM Fx_Orders WHERE OrderId = @orderid

-- 查询该用户的父级用户id
SELECT @puser = ParentId FROM Fx_UserAsset WHERE UserId = @userid

-- 查询该订单的商品数量
INSERT INTO @pronumt (pid, pronum)
SELECT PId, ProNum FROM Fx_Order_SizeInfo WHERE OrderId = @oid

-- 查询各级拿货价格
-- grade汇总计算各等级的拿货金额级差。Fx_Product_Price_Setting 调用较少，进行联查
INSERT INTO @prot(grade, sumprice)
SELECT GradeId, SUM(sumprice)
FROM (
    SELECT L.pid, L.pronum, R.GradeId, R.GetPrice, L.pronum * R.GetPrice AS sumprice
    FROM @pronumt AS L INNER JOIN Fx_Product_Price_Setting AS R ON L.pid = R.ProductId
)T GROUP BY GradeId

-- 查询该用户的父级用户
;WITH T AS(
    SELECT @userid AS cuser, Grade AS cgrade, ParentId AS puser FROM Fx_UserAsset WHERE UserId = @userid
    UNION ALL
    SELECT T.Puser AS cuser, R.Grade AS cgrade, R.ParentId AS puser FROM T INNER JOIN Fx_UserAsset AS R ON T.puser = R.UserId
)
INSERT INTO @usert (cuser, cgrade, puser)
SELECT cuser, cgrade, puser FROM T

-- 汇总每个用户的拿货金额
UPDATE L SET L.sumprice = R.sumprice
FROM @usert AS L INNER JOIN @prot AS R ON L.cgrade = R.grade

-- 计算父级用户与子用户的等级差, 等级相等记0， 否则记1
UPDATE L SET jicha = 
    (CASE WHEN L.cuser = @puser AND L.cgrade = R.cgrade THEN 0 ELSE 1 END)
FROM @usert AS L LEFT JOIN @usert AS R ON L.cuser = R.puser



SELECT @orderid, @oid, @userid, @puser
SELECT * FROM @usert
SELECT * FROM @prot

-- 临时表，保存用户和订单id
DECLARE @cuser TABLE(
    userid INT
    ,oid BIGINT
)

-- 临时表，保存用户等级信息
DECLARE @puser TABLE(
    cuser INT
    ,tuser INT
    ,puser INT
    ,grade INT
)

-- 临时表，保存用户订单下的pid和pnum
CREATE TABLE #product (
    cuser INT
    ,oid BIGINT
    ,pid INT
    ,pnum INT
)

-- 临时表，保存计算返相关返利
CREATE TABLE #result(
    cuser INT
    ,tuser INT
    ,grade INT
    ,puser INT
    ,pid INT
    ,pnum INT
    ,getprice INT
    ,sumprice INT
    ,jicha INT
)

-- 查询一天内的有效订单（已发货）, 排除userid=38
INSERT INTO @cuser(userid, oid)
SELECT UserId, Id AS oid
FROM Fx_Orders AS L
WHERE OrderTime BETWEEN @st AND @et AND OrderStatus = 2 
ORDER BY UserId

-- 查询订单用户的上级用户id和等级
-- 排除Grade = 1 的用户，因为总裁自身不会有级差返利和平级返利
-- 排除UserId = 38 的用户，同上
-- 查询在统计当日有已发货订单的用户
-- 递归查询订单用户的上级和上级用户等级
;WITH T AS (
    SELECT L.UserId AS cuser, L.UserId AS tuser, L.Grade AS grade, L.ParentId AS puser 
    FROM Fx_UserAsset AS L 
    WHERE EXISTS (SELECT 1 FROM @cuser WHERE userid = L.UserId)
        AND L.Grade > 1 AND L.UserId <> 38
    UNION ALL
    SELECT T.cuser, L.UserId AS tuser, L.Grade AS grade, L.ParentId AS puser
    FROM Fx_UserAsset AS L INNER JOIN T ON L.UserId = T.puser
)
INSERT INTO @puser (cuser, tuser, grade, puser)
SELECT cuser,tuser,grade,puser FROM T ORDER BY cuser

-- 查询所有订单的pid和pnum
INSERT INTO #product(cuser, oid, pid, pnum)
SELECT L.userid, L.oid, R.PId, R.ProNum
FROM @cuser AS L INNER JOIN Fx_Order_SizeInfo AS R ON L.oid = R.OrderId

-- 合并订单商品数量信息和上级用户信息到#result
INSERT INTO #result(cuser, tuser, grade, puser, pid, pnum)
SELECT L.cuser, L.tuser, L.grade, L.puser, R.pid, R.pnum
FROM @puser AS L LEFT JOIN #product AS R ON L.cuser=R.cuser
ORDER BY L.cuser, L.grade DESC

-- 查询父级用户的拿货价，保存到#result
UPDATE L SET L.getprice = R.getprice
FROM #result AS L LEFT JOIN Fx_Product_Price_Setting AS R 
ON L.pid = R.ProductId AND L.grade = R.GradeId

-- 统计各级拿货价
UPDATE #result SET sumprice = pnum * getprice

-- 按照上下级的拿货价差，计算级差
UPDATE L SET L.jicha = L.sumprice - R.sumprice
FROM #result AS L LEFT JOIN #result AS R
ON L.cuser = R.cuser AND L.pid = R.pid AND L.puser = R.tuser

SELECT * FROM #result ORDER BY cuser, grade DESC
SELECT * FROM #product
SELECT * FROM @cuser
SELECT * FROM @puser
DROP TABLE #product, #result



SELECT TOP 10 * FROM Fx_Product_Price_Setting


-- 查询指定用户id的所有上级
;WITH T AS(
    SELECT UserId, ParentId, Grade FROM Fx_UserAsset WHERE UserId = 136
    UNION ALL
    SELECT T.UserId, L.ParentId, L.Grade FROM Fx_UserAsset AS L INNER JOIN T ON L.UserId=T.ParentId
    WHERE L.UserId <> 38
)
SELECT * FROM T
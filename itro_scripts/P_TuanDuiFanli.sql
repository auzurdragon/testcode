
-- 分销团队返利统计
ALTER PROC [dbo].[P_FanliStatis] AS
-- 统计需求：
-- 统计范围：1、只统计吴总下面的总裁 或 ParentId=0 的总裁记录。 2. 上个自然月的已发货订单。 3. 按总载分类汇总后，给总裁团队返利
-- 即 Fx_UserAsset.ParentId IN (0, 38) AND Grade = 1
-- 统计需求：总裁下面的团队成员，销售数量合计 * 总载的每件商品拿货价，计算出上个自然月每个总载的返利金额后，写入分销返利点变化表和余额表。。
-- 注意事项：1、返点比例写在存储过程中；2、先从余额表获得返点前的余额，返点成功后，计算返点后的余额再回写入余额表
-- 若 分销返利点变化表 中已包含有结束日期的记录，则中止脚本，以免重复写入。返回错误码16,1

-- 相关表
-- 分销返利点变化表 Fx_FanliChangeLog，记录返利变化数量和类型
-- 分销返利点余额表　Fx_UserFanli， 记录用户最新的返利点余额，每个用户只记录一条

BEGIN
	DECLARE @st DATE, @et DATE, @stime DATETIME, @etime DATETIME
	-- 计算统计周期，获得上个自然月的开始和结束时间
	SET @st = DATEADD(MONTH,-1, GETDATE())	-- 计算上个自然月的日期
	SET @st = DATEADD(DAY, -DAY(@st)+1, @st)	-- 获得上个月的起始日期
	SET @et = DATEADD(DAY, -DAY(GETDATE())+1, GETDATE())	-- 当前月的第一天
	SET @stime = @st
	SET @etime = @et
	SET @etime = DATEADD(MS, -3, @etime)	-- 用当前月的第一天减去 3 毫秒，得到上个月的结束时间
	
	-- 返利比例
	DECLARE @rate FLOAT(2)
	SET @rate = 0.02

	-- 创建表变量，用于保存每个总裁下面的团队成员的用户id
	DECLARE @userid TABLE
	(
		RootId INT		-- 总裁ID
		,UserId INT		-- 总裁下的团队成员ID
	)
	-- 表变量，保存每个用户符合条件的订单ID
	DECLARE @oid TABLE
	(
		userid INT
		,oid BIGINT
	)
	-- 建立临时表，保存查询结果
	CREATE TABLE #result
	(
		UserId INT						-- 总裁用户ID
		,UserNum INT                    -- 下属的团队成员数量，预留
		,pronum INT                   	-- 团队成员的订单笔数，预留
		,MoneySum BIGINT                -- 计算返利的金额总数，预留
		,rate FLOAT(2)					-- 按MoneySum分档计算返利比例
		,MoneyPoint DECIMAL(18,2)		-- 汇总的返利变化量
		,FanliInit DECIMAL(18,2)        -- 统计时的返利点余额
		,FanliRemain AS MoneyPoint + FanliInit   -- 统计后的返利点余额
	)
	-- 临时表，保存每个团队成员的汇总记录
	CREATE TABLE #tmp
	(
		RootId INT          -- 所属于的总裁ID
		,UserId INT         -- 团队成员的用户ID
		,OId BIGINT     	-- 订单记录ID，Fx_Orders.Id
		,PId INT            -- 商品ID，Fx_Product_Price_Setting.ProductId
		,pronum INT       	-- 商品数量，Fx_Order_SizeInfo.ProNum
		,getPrice INT      	-- 所属于的总裁的拿货价格, Fx_Product_Price_Setting.GetPrice  WHERE GradeId = 1
		,price INT			-- 按pid分类的返利金额合计
	)

	-- 查询出符合条件的总裁用户，以及其下的团队成员ID，记录保存到#tmp
	;WITH Tree AS
	(
		-- 需要排除 UserId=38 的记录，是因为该记录的 ParentId = 0， 会影响迭代的结果，产生重复。
		SELECT P.UserId, P.Grade,P.UserId AS ParentId, P.UserId AS RootId FROM dbo.Fx_UserAsset P WHERE Grade=1 AND P.ParentId IN (0,38) AND UserId<>38
		UNION ALL
		SELECT C.UserId, C.Grade,C.ParentId, T.RootId AS RootId  FROM dbo.Fx_Userasset C INNER JOIN Tree T ON C.ParentId = T.UserId
	)
	INSERT INTO @userid (RootId, UserId) 
	SELECT RootId,UserId FROM Tree ORDER BY UserId

	-- 查询团队用户的已发货订单记录，Fx_Orders.OrderStatus=2，即已发货
	INSERT INTO @oid(userid, oid)
	SELECT A.UserId, B.Id
	FROM @userid AS A INNER JOIN Fx_Orders AS B ON A.UserId = B.UserId
	WHERE B.OrderTime BETWEEN @stime AND @etime AND OrderStatus=2

	-- 按用户id查询订单的商品id,以及按商品id汇总的商品销售数量,
	INSERT INTO #tmp(UserId, OId, PId, pronum)
	SELECT L.userid, L.oid, R.PId, SUM(R.ProNum)
	FROM @oid AS L INNER JOIN Fx_Order_SizeInfo AS R ON L.oid = R.OrderId
	GROUP BY L.userid, L.oid, R.PId

	-- 查询商品的总裁拿货价格
	UPDATE A SET A.getPrice = B.GetPrice
	FROM #tmp AS A LEFT JOIN [Fx_Product_Price_Setting] AS B ON A.PId = B.ProductId WHERE B.GradeId = 1

	-- 计算每个pid的返利金额
	UPDATE #tmp SET price = pronum * getPrice

	-- 保存用户id所属的总裁id
	UPDATE L 
	SET L.RootId = R.RootId
	FROM #tmp AS L LEFT JOIN @userid AS R ON L.userid = R.userid

	-- 计算总载的返点金额并写入临时表，只查询有销售记录的
	INSERT INTO #result(UserId, UserNum, pronum, MoneySum)
	SELECT RootId
		,COUNT(DISTINCT UserId) AS UserNum
		,SUM(pronum) AS pronum
		,SUM(Price) AS MoneySum
	FROM #tmp WHERE pronum>0 GROUP BY RootId ORDER BY RootId

	-- 按汇总的返利金额计算分档的返利比例
	UPDATE #result SET rate = CASE 
		WHEN MoneySum <  20000 THEN 0.02 
		WHEN MoneySum >= 20000 AND MoneySum < 30000 THEN 0.03
		WHEN MoneySum >= 30000 AND MoneySum < 50000 THEN 0.04
		WHEN MoneySum >= 50000 AND MoneySum <100000 THEN 0.05
		WHEN MoneySum >=100000 AND MoneySum <200000 THEN 0.06
		WHEN MoneySum >=200000 AND MoneySum <300000 THEN 0.07
		WHEN MoneySum >=300000 AND MoneySum <400000 THEN 0.08
		WHEN MoneySum >=400000 AND MoneySum <500000 THEN 0.09
		WHEN MoneySum >=500000 THEN 0.10
	END
	
	-- 计算返利的数量=返利金额*比例
	UPDATE #result SET MoneyPoint = MoneySum * rate

	-- 查询总裁的当前返利余额, 自动计算统计后的返利余额
	UPDATE A SET A.FanliInit = ISNULL(B.FanliRemain, 0)
	FROM #result AS A LEFT JOIN Fx_UserFanli AS B ON A.UserId = B.UserId

	-- 将统计结果写入 分销返利点变化表 Fx_FanliChangeLog，
	INSERT INTO Fx_FanliChangeLog (UserId, MoneyPoint, MoneyType, DTime)
	SELECT UserId, MoneyPoint, 2 AS MoneyType, GETDATE() AS DTime 
	FROM #result ORDER BY UserId

	-- 将增加返利后的用户返利余额，回写入 分销返利点余额表　Fx_UserFanli
	-- 先更新Fx_UserFanli 中已存在的UserId 记录
	UPDATE A SET A.FanliRemain = B.FanliRemain
	FROM Fx_UserFanli AS A INNER JOIN #result AS B ON A.UserId=B.UserId
	
	-- 再补充之前没有记录的USERID
	INSERT INTO Fx_UserFanli(UserId, FanliRemain)
	SELECT UserId, FanliRemain FROM #result AS B WHERE NOT EXISTS (SELECT 1 FROM Fx_UserFanli WHERE UserId=B.UserId)

	-- 结束，打印结果
	SELECT * FROM #result
	DROP TABLE #tmp
	DROP TABLE #result
	RETURN
END
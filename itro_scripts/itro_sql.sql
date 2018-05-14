

ALTER PROC f_checkscores
	@stime DATETIME,
	@etime DATETIME
	AS
	-- 47.92.72.108,1449
	-- 财务对账记录查询，请输入开始时间和结束时间。
	-- 输入格式按照 '2018-01-20 00:00:00','2018-01-20 23:59:59.997'，不能超过1个月。
	-- 如果记录不全，请联系运维备份数据。
	-- 使用表: Fx_Orders, Fx_Order_SizeInfo, Fx_OrderLog, Fx_CzLog, Fx_UserInfo
	-- SizeId,SeriesId,BrandId,以及商品成本，记录在存储过程中的表变量@unitcost 
	-- 查询size,series,brand的id和名称
	-- SELECT a.Status,a.Id AS SizeId,b.SeriesId,b.BrandId,a.Name AS SizeName,b.SeriesName,b.BrandName FROM dbo.Fx_Size a LEFT JOIN
	-- (
	-- 	SELECT a.Id AS SeriesId, a.BrandId, a.Name AS SeriesName, b.Name AS BrandName FROM dbo.Fx_Series a LEFT JOIN dbo.Fx_Brand b ON a.BrandId=b.Id
	-- )b ON a.SeriesId = b.SeriesId

	BEGIN
		IF DATEDIFF(DAY,@stime,@etime) >31 
			BEGIN 
				SELECT '查询日期范围超过31天，请缩小查询范围'
				RETURN
			END
		CREATE TABLE #tmp (
			eventType SMALLINT,		-- 事件类型，0- 充值，1-订单
			DTime DATETIME,			-- 时间
			UserId INT,				-- 用户ID
			OrderId NVARCHAR(50),	-- 订单id和充值订单id
			oId INT,				-- fx_order.id
			OrderStatus INT,		-- 订单状态
			BrandId INT,			-- 品牌id
			SeriesId INT,			-- 系列id
			SizeId INT,				-- 规格id
			ProNum INT,				-- 订单商品数量
			pMoney BIGINT,			-- 积分变化数量，负数为扣除积分，正数为积分增加
			ScoresRemain BIGINT,	-- 积分余额，积分变化后的余额数量
			TrueName NVARCHAR(20),	-- 用户姓名
			BrandName NVARCHAR(50),	-- 品牌名称
			SeriesName NVARCHAR(50),	-- 系列名称
			SizeName NVARCHAR(50),	-- 规格名称
			UnitCost INT,			-- 商品单位成本，缺少成本表
			Cost AS ProNum*UnitCost,			-- 订单成本，即ProNum*UnitCost，包含了邮费
			Profit AS -(ProNum*UnitCost+pMoney*100)			-- 订单毛利，即-(Cost+pMoney),注意pMoney为负数
		)
		-- 将商品产品保存到表变量中，待用
		DECLARE @unitcost TABLE(
			SizeId Int,
			SeriesId INT,
			BrandId INT,
			BrandName NVARCHAR(50),
			SeriesName NVARCHAR(50),
			SizeName NVARCHAR(50),
			UnitCost INT
		)
		-- 保存商品成本数据，注意costunits单位成本单位为分
		INSERT INTO @unitcost VALUES
			(1,1,1,'蓝星','蓝星纸尿裤','S-24片装',1220),
			(2,1,1,'蓝星','蓝星纸尿裤','M-22片装',1242),
			(3,1,1,'蓝星','蓝星纸尿裤','L-20片装',1206),
			(4,1,1,'蓝星','蓝星纸尿裤','XL-18片装',1157),
			(5,2,1,'蓝星','蓝星纸尿片','S-34片装',1084),
			(6,2,1,'蓝星','蓝星纸尿片','M-30片装',1085),
			(7,2,1,'蓝星','蓝星纸尿片','L-28片装',1103),
			(8,2,1,'蓝星','蓝星纸尿片','XL-26片装',1117),
			(9,3,2,'星际','星际纸尿裤','S-66片装',3999),
			(10,3,2,'星际','星际纸尿裤','M-60片装',4045),
			(11,3,2,'星际','星际纸尿裤','L-56片装',4122),
			(12,3,2,'星际','星际纸尿裤','XL-52片装',4095),
			(13,4,2,'星际','星际拉拉裤','L-28片装',2072),
			(14,4,2,'星际','星际拉拉裤','XL-27片装',2036),
			(15,4,2,'星际','星际拉拉裤','XXL-26片装',1978),
			(17,5,3,'宠爱','宠爱纸尿裤','S-60片装',3525),
			(18,5,3,'宠爱','宠爱纸尿裤','M-52片装',3389),
			(19,5,3,'宠爱','宠爱纸尿裤','L-48片装',3414),
			(20,5,3,'宠爱','宠爱纸尿裤','XL-44片装',3365),
			(21,6,3,'宠爱','宠爱拉拉裤','L-42片装',3398),
			(22,6,3,'宠爱','宠爱拉拉裤','XL-40片装',3432),
			(23,6,3,'宠爱','宠爱拉拉裤','XXL-40片装',3451),
			(24,7,4,'馨爱','馨爱纸尿裤','S-40片装',1939),
			(25,7,4,'馨爱','馨爱纸尿裤','M-34片装',1847),
			(26,7,4,'馨爱','馨爱纸尿裤','L-30片装',1798),
			(27,7,4,'馨爱','馨爱纸尿裤','XL-26片装',1634),
			(28,8,4,'馨爱','馨爱纸尿片','S-50片装',1569),
			(29,8,4,'馨爱','馨爱纸尿片','M-44片装',1521),
			(30,8,4,'馨爱','馨爱纸尿片','L-40片装',1509),
			(31,8,4,'馨爱','馨爱纸尿片','XL-36片装',1473),
			(32,9,4,'馨爱','馨爱拉拉裤','L-28片装',1741),
			(33,9,4,'馨爱','馨爱拉拉裤','XL-26片装',1657),
			(34,9,4,'馨爱','馨爱拉拉裤','XXL-26片装',1744),
			(35,10,5,'婴诺惟','婴诺惟草饲奶粉','1段',10000),
			(36,10,5,'婴诺惟','婴诺惟草饲奶粉','2段',10000),
			(37,10,5,'婴诺惟','婴诺惟草饲奶粉','3段',10000),
			(38,11,3,'宠爱','宠爱纸尿裤','NB-30片装',1626),
			(39,12,3,'宠爱','宠爱湿纸巾','8包/箱',2800),
			(41,16,8,'森比奥','森比奥试用装','森比奥试用装5片装',80),
			(42,13,7,'银河','银河纸尿裤','S-44片装',2220),
			(43,13,7,'银河','银河纸尿裤','M-40片装',2237),
			(44,13,7,'银河','银河纸尿裤','L-38片装',2282),
			(45,13,7,'银河','银河纸尿裤','XL-34片装',2177),
			(46,14,7,'银河','银河纸尿片','S-76片装',2563),
			(47,14,7,'银河','银河纸尿片','M-68片装',2578),
			(48,14,7,'银河','银河纸尿片','L-62片装',2561),
			(49,14,7,'银河','银河纸尿片','XL-56片装',2516),
			(40,15,8,'森比奥','森比奥赠品','森比奥赠品',0)

		-- 查询订单表，保存记录到临时表
		INSERT INTO #tmp (eventType,DTime,UserId,OrderId,oId,OrderStatus,pMoney,ScoresRemain)
		SELECT 
			1 AS eventType,
			PayTime,
			UserId,
			CONVERT(NVARCHAR(50),OrderId) AS OrderId,
			Id AS oId,
			OrderStatus,
			-PayMoney AS pMoney,
			NULL AS ScoresRemain
		FROM dbo.Fx_Orders
		WHERE OrderStatus >0 AND PayTime BETWEEN @stime AND @etime

		-- 查询SizeId
		UPDATE a SET a.SizeId=b.SizeId,a.ProNum=b.ProNum
		FROM #tmp AS a LEFT JOIN dbo.Fx_Order_SizeInfo b ON a.oId=b.OrderId

		-- 查询品牌名称,系列名称和规格名称，以及商品成本
		UPDATE a SET a.BrandId=b.BrandId,a.BrandName=b.BrandName,a.SeriesId=b.SeriesId,a.SeriesName=b.SeriesName,a.SizeName=b.SizeName,a.UnitCost=b.UnitCost
		FROM　#tmp AS a LEFT JOIN @unitcost AS b ON a.SizeId=b.SizeId

		-- 更新下单后的积分余额
		UPDATE a SET a.ScoresRemain=b.ScoresRemain
		FROM #tmp AS a LEFT JOIN dbo.Fx_OrderLog AS b ON a.OrderId=b.OrderId

		-- 查询充值记录和充值后的积分余额，CzLog表中为成功的记录
		INSERT INTO #tmp (eventType,DTime,UserId,OrderId,oId,OrderStatus,pMoney,ScoresRemain)
		SELECT 
			0 AS eventType,
			DTime,
			UserId,
			OrderId,
			-1 AS oId,
			NULL AS OrderStatus,
			Scores AS pMoney,
			ScoresRemain
		FROM dbo.Fx_CzLog WHERE DTime BETWEEN @stime And @etime

		-- 更新用户姓名
		UPDATE a SET a.TrueName=b.TrueName
		FROM #tmp AS a LEFT JOIN dbo.Fx_UserInfo AS b ON a.UserId=b.UserId

		SELECT 
			(CASE WHEN eventType=0 THEN '充值' WHEN eventType=1 THEN '下单' ELSE '其它' END) AS 类型,
			CONVERT(NVARCHAR(19),DTime,120) AS 时间,
			TrueName AS 姓名,
			OrderId AS 订单ID,
			BrandName AS 品牌,
			SeriesName AS 系列,
			SizeName AS 规格,
			ProNum AS 商品数量,
			pMoney AS 积分金额,
			ScoresRemain AS 积分余额,
			CONVERT(DECIMAL(9,2),UnitCost)/100 AS 单位成本,
			CONVERT(DECIMAL(9,2),COST)/100 AS 成本合计,
			CONVERT(DECIMAL(9,2),Profit)/100 AS 毛利
			-- UserId,
			-- BrandId,
			-- SeriesId,
			-- SizeId
		FROM #tmp ORDER by UserId,DTime
		
		DROP TABLE #tmp
	END


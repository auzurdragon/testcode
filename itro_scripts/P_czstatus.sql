


DECLARE @orderid NVARCHAR(50)
SET @orderid= 137931720220180303131159849
DECLARE @userid INT, @money INT, @moneyinit INT, @dtime DATETIME

SELECT @userid = UserId, @money = Money FROM [dbo].[Fx_CzOrder] WHERE OrderId = @orderid
SELECT @moneyinit = FROM Fx_UserAsset WHERE UserId = @userid
SET @dtime = GETDATE()

UPDATE UPDATE [dbo].[Fx_CzOrder] SET OrderStatus = 1, PayStatus =1 
WHERE OrderId = @orderid

INSERT INTO [dbo].[Fx_ScoresLog] (UserId,OrderId,fromuser,logtype,scores,scoresremain,dtime) 
VALUES (@userid, @orderid, -1, 10, @money, @money + @moneyinit, @dtime) 

INSERT INTO [dbo].[Fx_CzLog] (UserId,OrderId,Money,Scores,ScoresRemain,DTime) 
VALUES (@userid, @orderid, @money, @money, @money+@moneyinit, @dtime)

UPDATE [dbo].[Fx_UserAsset] SET UseMoney = @money + @moneyinit WHERE UserId = @userid
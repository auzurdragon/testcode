db.iTRO_RedPacket.mapReduce(
    function(ctime){    // 定义map函数，取出 > 1499388000 的记录，进行map映射。
        if(this.date+this.outdate*3600 > 1499388000){
            emit(this._id,
                 {'sendid':this.sendid,
                  'sendAmount':NumberInt(this.sendAmount),
                  'sendCount':NumberInt(this.sendCount),
            });
        }
    },
    function(key, values){  // 定义reduce函数，对map映身的key-value进行处理
        var res = {'_id':key,
                   'value':values
                };
        return res;
    },
    {out:'tmp_f_redpacket'}
)


// 按productid分组统计销量
db.iTRO_UserChildOrder.aggregate([
    {$match:{"storeid" : "596c1929048e800f281c903e",
             "orderstatus" : 2,
             "date" : {
                 "$gte" : NumberLong(1500480000),
                 "$lte" : NumberLong(1500566399)}
            }
    },
    {$group:{
        '_id':'$productid',
        'sum':{$sum:'$num'}
    }},
])




// iTRO_CNZZ, 
db.iTRO_CNZZ.aggregate([
    {$match:{'date':'2017-07-21', 'type':2, 'sid'}},
    {$project:{'_id':0, 'sid':1, 'ip':1,}},
    {$group:{
        '_id':'$sid',
        'num':{$sum:1},
    }}
])

db.iTRO_CNZZ.distinct(
    'ip',
    {date:'2017-07-21', type:2, sid:'596dc05b048e80007cf13455'}
)


db.iTRO_UserChildOrder.aggregate([
    {$match:{'date':{$gte:NumberLong(1400000000)}}},
    {$group:{'_id':'$storeid','sum':{$sum:1}}},
    {$sort:{'sum':-1}}
])


db.iTRO_UserChildOrder.aggregate([
    {$match:{'storeid':'58d078236c6df51fe06a6bb5', 'date':{$gte:NumberLong(1400000000)}}},
    {$project:{'_id':1, 'storeid':1, 'date':{'$date'*1000}, 'stype':String('$status'), 'paymoney':'$paymoney'}},
    {$group:{'_id':{'stype':'$stype', 'date':'$date'}, 'paynum':{$sum:1}, 'paysum':{$sum:'$paymoney'}}},
    {$sort:{'paysum':-1}}
])


db.iTRO_UserChildOrder.aggregate([
	{$match:{'storeid':'58d078236c6df51fe06a6bb5','date':{$gte:1495093437}}},
	{$project:{
        'storeid':1, 
        'sdat':{
            $add:[new Date(0), {$multiply:['$date', 1000]}]}}},
])

// 按店铺id查询，最近一段时间每天已收货的订单数量和金额合计。
db.iTRO_UserChildOrder.aggregate([
    {$match:{'storeid':'58d078236c6df51fe06a6bb5','date':{$gte:1495093437}, 'status':3}},
    {$project:{
        '_id':1,
        'storeid':1,
        'sdate':{$dateToString:{
            format:'%Y-%m-%d',
            date:{$add:[new Date(28800000), {$multiply:['$date', 1000]}]},
        }},
        'syear':{$year:{$add:[new Date(28800000), {$multiply:['$date', 1000]}]}},
        'smonth':{$month:{$add:[new Date(28800000), {$multiply:['$date', 1000]}]}},
        'sday':{$dayOfMonth:{$add:[new Date(28800000), {$multiply:['$date', 1000]}]}},
        'shour':{$hour:{$add:[new Date(28800000), {$multiply:['$date', 1000]}]}},
        'sminute':{$minute:{$add:[new Date(28800000), {$multiply:['$date', 1000]}]}},
        'ssecond':{$second:{$add:[new Date(28800000), {$multiply:['$date', 1000]}]}},
        'paymoney':1
    }},
    {$group:{
        '_id':{'storeid':'storeid', 'sdate':'$sdate'},
        'paynum':{$sum:1},
        'paysum':{$sum:'$paymoney'}
    }},
    {$sort:{'_id':-1}}
])


db.iTRO_UserChildOrder.aggregate([
    {$match:{'storeid':'58d078236c6df51fe06a6bb5','date':{$gte:1495093437}, 'status':3}},
    {$project:{
        '_id':1,
        'storeid':1,
        'sdate':{$floor:{$divide:['$date',86400]}},
        'sdate2':{$dateToString:{
            format:'%Y-%m-%d',
            date:{$add:[new Date(28800000), {$multiply:['$date', 1000]}]},
        }},
    }},
    {$group:{
        '_id':{'sdate':'$sdate', 'sdate2':'$sdate2'},
        'paynum':{$sum:1},
    }}
])
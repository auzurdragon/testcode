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

// 在同个实例内转移表，不能用于集群
use admin // 必须在admin下使用
db.runCommand({renameCollection:'sourcedb.oldName', to:'targetdb.newName'})


// 发布约会
db.iTRO_publishmeet.insert({
    '_id':,         // 记录id
    'fromuser':,    // userid,发布者
    'fromtime':,       // timestamp,发布时间
    'meettime':,    // timestamp, 约会时间
    'meettitle':,   // string,约会标题
    'meetcontent':, // string,约会内容
    'meetimg':[],   // array,urlstring,约会图片链接
    'meetlimit':,   // int32,约会人数名额。
    'enlistnum':,   // int32,约会报名人数，可与enlist合并
    'membernum':,   // int32,约会参与人数，可与member合并
    'avggrade':,    // float,约会的平均评分，展示时按1位小数四舍五入。
    'meetstatus':,  // int32,约会状态，1-开始报名。2-活动进行中。3-活动结束。4-报名结束，报名人数已满。9-已关闭，活动开始7天后，不显示给前端。
    'touser':[],    // array,userid,发布对象，预留字段
    'toarea':[],    // array,string,发布地区，预留字段
    'enlist':[      // array,报名用户和报名状态。
        {
            'userid':, // string,报名用户id
            'status':, // int32,报名状态，1-报名中，等待发起者审核。2-报名成功，发起者同意。3-报名失败，发起者拒绝。0-可以报名，显示报名（按钮）
        },
    ],
    'member':[          // array,userid,参与用户，报名且由发起者同意的用户。
        {
            'userid':,  // string,参与用户id
            'grastatus':,   // int32,评价状态,1-可以评论，前端显示评价按钮。2-已评论，前端显示已评价状态
            'gratime',  // timestamp,评价时间
            'grade':,   // int32,参与用户的评分，允许空值, 5-非常满意，1-非常差
            'content':, // string,用户的评价内容。
        },
    ],
})


// 发布订单
db.iTRO_publishorder.insert({
    '_id':,         // object,记录id
    'fromuser':,    // string,发布用户id
    'fromtime':,    // timestamp,发布时间
    'ordertitle':,  //  string,发布订单标题
    'ordercontent':,    // string,发布订单内容
    'orderdictionary':,   // string,商品类目id
    'ordertype':,          // int32,订单类型，1-就近购买, 2-指定地址
    'payment':,           // int32,商品货款
    'fee':,                // int32,小费，预留字段
    'deliveryinfo':{,      // Document,配送用户信息,预留字段
        'deliveryuser':,   // string,配送用户id
        'deliverytel':,    // string,配送用户联系电话
    },
    'ordertime':,          // timestamp,送达时间要求
    'orderstatus':,        // int32,订单状态，1-接单中，等待商户接单，2-配送中，商户正在配送。3-已送达，用户已收货。4-已完成，货款已支付给商户。10-已取消，发布者取消订单，不显示给前端
    'checkinfo':{          // Document,收货人信息
        'name':,          // string,收货人姓名
        'checktel':,           // string,电话
        'address':,      // string,省市区地址
        'streets':,       // string,详细地址
    },
    'touser':[],          // array,userid,发布对象，预留字段
    'toarea':[],          // array,string,发布地区，预留字段
    'getinfo':{           // Document,收接订单的商户信息
        'storeid':,       // string,店铺ID
        'userid':,        // string,商户id
        'storename':,     // string,店铺名称
        'storelogo':,     // string,店铺logo
        'gettel':,        // string,店铺联系电话
    }
})

// 发布消息
db.iTRO_publishmessage.insert({
    '_id':,               // object,记录id
    'fromuser':,          // string,发布用户id
    'fromtime':,          // timestamp,发布时间
    'fromlocation':{
        'localtion':{
            'type':'Point',     // 地理数据类型
            'coordinates':[经度, 纬度],   // 经纬度，
        },                // geoobject, 发布时的地理坐标，
        'address':,       // string,发布时的省市区位置
        'streets':,       // string,发布时的详细位置
    },                    // Document,测试用geo对象保存地理位置信息 
    'pushtime':,          // timestamp,推送时间，预留字段，以备将来加入审核
    'messagestatus':,     // int32,消息状态，预留字段，以备将来加入审核，1-已推送，推送到个推。2-审核不通过，不进行推送。
    'messagetitle':,      // string,消息标题
    'messagecontent':,    // string,消息内容
    'messageimg':[],      // array,urlstring,附带图片
    'touser':[],          // array,string,预留字段，发布对象的用户id
    'toarea':[],          // array,string,预留字段，发布地区
})


// 在数组内嵌文档中插入一个k:v
// 创建测试数据
db.testcoll.insert({ 
    "_id" : ObjectId("599d20e571e472580cd057b3"), 
    "prolist" : [
        {
            "productid" : "599ab94171e472c3645eaa46", 
            "seriesid" : "59965e5b71e472b398c5336d", 
            "size" : "S", 
            "color" : "红色", 
            "num" : NumberInt(1), 
            "price" : NumberInt(101), 
            "seriesname" : "蓝心体验系列"
        }, 
        {
            "productid" : "599ab94171e472c3645eaa46", 
            "seriesid" : "59965e0371e472b398c5336b", 
            "size" : "S", 
            "color" : "红色", 
            "num" : NumberInt(1), 
            "price" : NumberInt(101), 
            "seriesname" : "test"
        }
    ]
})

// 在prolist数组中，seriesid:'59965e5b71e472b398c5336d'的内嵌文档，插入teststr:5336d
db.fx_order.update(
    {'prolist.seriesid':'59965e5b71e472b398c5336d'},
    {$set:{'prolist.$.teststr':'5336d'}}
)

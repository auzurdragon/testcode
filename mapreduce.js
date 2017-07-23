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



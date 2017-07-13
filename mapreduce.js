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
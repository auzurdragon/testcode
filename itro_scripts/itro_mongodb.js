Activitydb.iTRO_ActConfig
// 活动配置表
{
	_id:ObjectId(),			// 活动ID
	ActName:"",				// 活动名称
	Title:"",				// 活动主题
	StartDt:NumberLong(),	// 活动开始时间戳，秒
	EndDt:NumberLong(),		// 活动结束时间戳，秒
	ActUrl:"",				// 活动链接地址，http://www.51itro.com/act/weiguangou/index?loginid={0}&shareuserid={1}&eventid={2}
	ActCode:"",				// 活动的HTML代码
	Status:<Boolean>,		// true：活动启用；false:活动禁用。默认为true, 只展示活动入口，业务逻辑需要联合其它参数判断是否启动。
	Reward:[				// 数组类型，保存奖品内容
		"奖品名称1",
		"奖品名称2"
	],
	Chance:[				// 数组类型，保存对应位置奖品Reward的概率。必须与Reward长度一致。
		NumberInt(),		// 奖品1的概率
		NumberInt()			// 奖品2的概率
	],
	Numbers:[				// 数组类型，保存对应位置奖品Reward的数量，必须与Reward长度一致。
		NumberInt(),		// 奖品1的数量
		NumberInt()			// 奖品2的数量
	],
	Mark:[				  	// 保存活动对应的规则表名和ID
		"表名",
		"主键ID"
	]
}

// 抢围观活动配置
use Activitydb;
db.iTRO_ActConfig.insert({
	ActName:'抢围观',
	Title:'集助力得iPhone8',
	StartDt:NumberLong(1510070400),		// 11月8日00:00:00
	EndDt:NumberLong(1514735999),		// 12月31日23:59:59
	ActUrl:'',
	ActCode:'',
	Status:true,
	Reward:[
		'iPhone8优惠券4888',	// 10人围观抽奖
		'iPhone8优惠券3888',	// 100人围观抽奖
		'iPhone8优惠券1888',	// 500人围观奖励，限前3，满1000围观者不能参与500奖励
		'iPhone8优惠券888',		// 1000人围观奖励，不限名额
		'iPhone8特惠',			// 活动结束时的所有参与者抽奖
	],
	Chance:[
		NumberInt(0),			// 抽奖
		NumberInt(0),			// 抽奖
		NumberInt(0),			// 前三名获得
		NumberInt(0),			// 不限名额，满1000人围观即得
		NumberInt(0),			// 活动结束时的所有参与者抽奖
	],
	Numbers:[
		NumberInt(1),			// 1张
		NumberInt(1),			// 1张
		NumberInt(3),			// 500人围观前三名获得
		NumberInt(10),			// 1000人围奖励，暂订为10台，以后再添加
		NumberInt(1),			// 活动结束时的所有参与者抽奖
	],
	Mark:[]
});

// 活动中奖记录日志表
use Activitydb;
db.iTRO_ActRewardLog.insertOne({
  'ActId':'59fa7fc844648b9c00caa4f2',	    // 活动配置表iTRO_ActConfig中的对应活动的主键Id
  'ActName':'抢围观',			          // 活动名称
  'UserId':'58c7c51d6c6df528042e2f38',	// 中奖者的iTRO_User表中的主键Id
  'RewardDt':NumberLong(1514735999),	    // 中奖的时间戳
  'Reward':'iPhone8优惠券888',			 // 奖品名称
  'Numbers':NumberInt(1),		            // 奖品数量
  'CreateDt':NumberLong(1514735999),	    // 日志记录时间戳
  'Status':NumberInt(0)			        // 日志记录状态, 0-default,默认值'待发奖', 1-'已发奖', 10-'发奖错误'
})
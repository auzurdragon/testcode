# coding:utf-8

# 常用命令
itchat.auto_login()                 # 打开二维码，扫描登录微信
itchat.auto_login(hotReload=True)   # 如果你不想要每次运行程序都扫码，可以在登陆命令中进行设置
itchat.run()                        # 后台运行
itchat.get_friends()                # 获得联系人列表
itchat.get_contact()                # 获得群列表
itchat.get_mps()                    # 获得公众号列表

# 联系人属性
{
    'Uin': 0,
    'UserName': '@f9e0e0631d145d8dabf2321ec21ccd7d97b1e907a6a6083ca2a82d95b5512342',
    'NickName': '2018',
    'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=681730865&username=@f9e0e0631d145d8dabf2321ec21ccd7d97b1e907a6a6083ca2a82d95b5512342&skey=@crypt_8c0df6db_7a173e58dffbc19049fc3ef43b3f99fc',
    'ContactFlag': 3,
    'MemberCount': 0,
    'MemberList': [],
    'RemarkName': '胡岸',
    'HideInputBarFlag': 0,
    'Sex': 0,
    'Signature': '',
    'VerifyFlag': 0,
    'OwnerUin': 0,
    'PYInitial': '2018',
    'PYQuanPin': '2018',
    'RemarkPYInitial': 'HA',
    'RemarkPYQuanPin': 'huan',
    'StarFriend': 0,
    'AppAccountFlag': 0,
    'Statues': 0,
    'AttrStatus': 4133,
    'Province': '',
    'City': '',
    'Alias': '',
    'SnsFlag': 0,
    'UniFriend': 0,
    'DisplayName': '',
    'ChatRoomId': 0,
    'KeyWord': '',
    'EncryChatRoomId': '',
    'IsOwner': 0,
}
# 公众号属性
{
    'Uin': 0,
    'UserName': '@abc8aa0c3e90cc0193b98571ebd12e10',
    'NickName': '大众点评',
    'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=647978462&username=@abc8aa0c3e90cc0193b98571ebd12e10&skey=@crypt_8c0df6db_bc846343a96787f55160d148d4966bba', 'ContactFlag': 3, 'MemberCount': 0, 'MemberList': [], 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '大众点评服务号，为你提供身边的吃喝玩乐信息，和优质低价的团购服务。专业的中国城市消费指南：餐馆美食、购物、电影、酒店、KTV、外卖各种优惠一应俱全，实惠新潮的活动资讯不间断。',
    'VerifyFlag': 24,
    'OwnerUin': 0,
    'PYInitial': 'DZDP',
    'PYQuanPin': 'dazhongdianping',
    'RemarkPYInitial': '',
    'RemarkPYQuanPin': '',
    'StarFriend': 0,
    'AppAccountFlag': 0,
    'Statues': 0,
    'AttrStatus': 0,
    'Province': '上海',
    'City': '长宁',
    'Alias': '',
    'SnsFlag': 0,
    'UniFriend': 0,
    'DisplayName': '',
    'ChatRoomId': 0,
    'KeyWord': 'gh_',
    'EncryChatRoomId': '',
    'IsOwner': 0,
}


# 获得消息
# itchat需要先对处理消息的函数进行注册register()，在获得相应类型的消息时自动调用该函数
import itchat

# 通过装饰符@将下一行的print_content注册为处理文本消息的函数
# 微信的数据类型包括：
# 图片, itchat.content.PICTURE
# 语音, itchat.content.RECORDING
# 名片, itchat.content.CARD
# 其它类型参见[文档](http://itchat.readthedocs.io/zh/latest/)
@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg['Text'])
    itchat.send('dkdkdlslkdjkf','filehelper')

itchat.auto_login(hotReload=True)
itchat.run()

# 发送消息, toUserName 使用 'filehelper' 即向文件传输助手发消息
itchat.send('message content', 'toUserName')

# 向微软小冰发消息, UserName = '@a9108d5a20da7e902e327fbb02ae5d9e'
# 获得小冰的UserName，注意小冰属于公众号
mlist = itchat.get_mps()
for i in mlist:
    if i['NickName'] == '小冰':
        username = i['UserName']
        break
# 向小冰发消息
itchat.send('鱼香肉丝怎么做', username)




# 使用图灵机器人http://www.tuling123.com
import requests
api = 'http://www.tuling123.com/openapi/api'
data = {
    'key':'347ab74551a54885ae7d3edf7932b935',
    'info':'是字开头的成语',
    'userid':'123456',
}
t = requests.post(api, data=data)
t.json().get('text')



# 示例，自动回复消息, 将接收的消息转发到图灵机器人，再将机器人回复返回发给发送者
@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    import requests
    data = {
        'key':'347ab74551a54885ae7d3edf7932b935',
        'info':msg['Text'],
        'userid':'123456',
    }
    t = requests.post(api, data=data).json()
    t = t.get('text')
    return t



@itchat.msg_register(itchat.content.MAP)
def print_content(msg):
    print(msg['Text'])
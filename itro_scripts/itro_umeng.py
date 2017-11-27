
auth_url = 'http://api.umeng.com/authorize'
auth_data = {
    'email':'huan@crelove.net',
    'password':'clumeng0828'
}
app_info = [
    {
        'name':'iTRO_iOS',
        'platform':'iphone',
        'category':'生活',
        'appkey':'599a35e1734be41ff00000d4',
    },
    {
        'name':'iTRO_Android',
        'platform':'android',
        'category':'电子商务',
        'appkey':'599a3351677baa2591001996',        
    }
]

tmp = requests.post(url=auth_url, data=auth_data)

auth_token = tmp.json()['auth_token']

# 获得APPS列表
url = 'http://api.umeng.com/apps?auth_token=%s' % auth_token
tmp = requests.get(url)


# 获得任意日期的基本数据
url = 'http://api.umeng.com/base_data?auth_token=%s&appkey=%s&date=%s' % (auth_token, app_info[1]['appkey'], '2017-11-19')
tmp = requests.get(url)
# 响应参数
# result = {
#     'date':'2017-11-19',
#     'active_users':5,    # 活跃用户数
#     'installations':343,   # 总用户数
#     'launches':7,        # 启动次数
#     'new_users':4,       # 新用户数
# }
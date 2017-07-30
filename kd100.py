http://api.kuaidi100.com/api?id=[]&com=[]&nu=[]&show=[0|1|2|3]&muti=[0|1]&order=[desc|asc]


from urllib import request
url_id = '7fb51a3cb2a359e4'
url_com = 'zhongtong'
url_num = '765327822682'
url_show = '2'
# gurl = (
#     'http://api.kuaidi100.com/api'
#     '?id=%s'
#     '&com=%s'
#     '&nu=%s'
#     # '&valicode=%s'  # 已弃用
#     '&show=%s'
#     '&muti=1'
#     '&order=desc' 
#     % (url_id, url_com, url_num, url_show)
# )


# gurl = (
#     'http://www.kuaidi100.com/applyurl'
#     '?key=%s'
#     '&com=%s'
#     '&nu=%s'
#     % (url_id, url_com, url_num)
# )

gurl = (
    'https://m.kuaidi100.com/index_all.html'
    '?type=%s'
    '&postid=%s'
    % (url_com, url_num)
)
req = request.Request(gurl)
result = request.urlopen(req).read().decode()


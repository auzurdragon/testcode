#coding:utf-8
"""抓取小蜜新闻"""

import requests
from bs4 import BeautifulSoup as bs

url = 'http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&bs=%E5%B0%8F%E8%9C%9C&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word=%E5%BE%AE%E9%A2%86%E5%9C%B0+%E5%B0%8F%E8%9C%9C&rsv_sug3=8&rsv_sug4=440&rsv_sug1=2&rsv_sug2=0&inputT=3753'
data = requests.get(url)
data = bs(data.content)
result = data.body.select('div.result', 'html.parser')

result_list = []
for item in result:
    tmpstr = item.div.p.text
    result_list.append({
        'title':item.h3.a.text,
        'url':item.h3.a['href'],
        'sitename':tmpstr.split('\xa0\xa0')[0],
        'date':tmpstr.split('\xa0\xa0')[1],
        'brief':item.div.text[len(tmpstr):]
    })


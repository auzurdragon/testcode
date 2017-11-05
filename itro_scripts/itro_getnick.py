#coding:utf-8

import requests
from bs4 import BeautifulSoup as bs
import re

nick_list=[]
pattern = re.compile('[^a-zA-Z0-9\u4e00-\u9fa5]')

for i in range(1,21):
    url = 'https://www.yimanwu.com/nvsheng/youyade/list_60_%d.html' % i
    result = requests.get(url)
    result = bs(result.content, 'html.parser')
    result_list = result.body.select('div.list')[0]
    result_list = result_list.select('p')
    for item in result_list:
        tmp = item.text
        nick_list.append(pattern.sub('', tmp)[:6])

nickset = set(nick_list)
with open('itro_scripts/nickset.txt', 'w') as writer:
    for i in nickset:
        writer.write(i+'\n')
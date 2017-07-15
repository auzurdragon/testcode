# -*- coding: utf-8 -*-
"""
Created on Sat May  6 21:46:18 2017
@author: Andy
"""

from urllib import request
from bs4 import BeautifulSoup
import pymongo
gurl = 'http://db.h.163.com/cards/filter?filter=CardType%3D10'
tmp = request.urlopen(gurl).read().decode('utf-8')
tmp = BeautifulSoup(tmp, 'lxml')
td = tmp.body.find_all('ul',class_='nav-list')

result = []
for i in td:
    ta = i.select('a')
    for j in ta:
        h = {}
        h['game'] = '炉石传说'
        h['class'] = j.get_text()
        h['class_url'] = 'http://db.h.163.com'+j['href']
        result.append(h)

conn = pymongo.MongoClient('localhost', 28010)
coll = conn.mydata.mycard
coll.insert_many(result)
conn.close()

def get_list(class_name, class_url):
    from urllib import request
    from bs4 import BeautifulSoup
    tmp = request.urlopen(class_url).read().decode('utf-8')
    tmp = BeautifulSoup(tmp, 'lxml')
tmp = tmp.body.find('div', class_='page-number')
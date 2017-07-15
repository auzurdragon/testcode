# -*- coding=utf-8 -*-

class GetAV(object):
    """ 类 """
    def __init__(self, name):
        self.info = {'name':name,
                     'url':'',
                     'quantity':0,
                     'img':'',
                     'alias':'',
                     'birth':'',
                     'brief':'',
                     'entry':'',
                     'measurement':'',
                     'tag':[],
                     'movie':[]}
        self.conn_info = {'host':'localhost', 'port':28010}

    def get_info(self, search_name=''):
        """ 从番号库网站获得数据 """
        from urllib import request, parse
        from bs4 import BeautifulSoup
        import re
        if search_name == '':
            search_name = self.info['name']
        search = 'http://www.btdiggzw.org/fanhao/ss_'
        req = request.Request(search+parse.quote(search_name)+'.htm')
        tmp = BeautifulSoup(request.urlopen(req).read().decode('utf-8', 'ignore'))
        if len(tmp.find_all('h3')) == 0:
            print('can not search '+search_name)
            return False
        elif len(tmp.find_all('h3')) > 1:
            for i  in tmp.find_all('h3'):
                print('search result :'+i.a.get_text())
            return False
        else:
            # 重置self.info
            self.info = {'name':search_name,
                         'url':'',
                         'quantity':0,
                         'img':'',
                         'alias':'',
                         'birth':'',
                         'brief':'',
                         'entry':'',
                         'measurement':'',
                         'tag':[],
                         'movie':[]}
            self.info['name'] = search_name
            self.info['url'] = 'http://www.btdiggzw.org/fanhao/'+tmp.h3.a.get('href')
            self.info['quantity'] = int(re.sub(r'\D', '', tmp.h3.span.get_text()))
            self.info['img'] = tmp.img.get('lz_src')
            print('    Name : '+self.info['name'])
            print('     URL : '+self.info['url'])
            print('Quantity : '+str(self.info['quantity']))
            print('     img : '+self.info['img'])

    def get_detail(self):
        """ 按url获取数据"""
        from urllib import request
        from bs4 import BeautifulSoup
        tmp = request.Request(self.info['url'])
        tmp = request.urlopen(tmp).read().decode('utf-8')
        tmp = BeautifulSoup(tmp)
        # 获得简介数据
        tmp_brief = tmp.section.div.div.aside.div.div.div.find_all('h4')
        self.info['alias'] = tmp_brief[0].get_text()
        self.info['brief'] = tmp_brief[1].get_text()
        self.info['birth'] = tmp_brief[2].get_text()
        self.info['entry'] = tmp_brief[3].get_text()
        self.info['measurement'] = tmp_brief[4].get_text()
        self.info['tag'] = tmp_brief[5].get_text().replace('特点：', '').split(',')
        # 获得番号和封面
        tmp_cover = tmp.section.div.find('div', class_='box4 box').article.ul.find_all('img')
        # 获得评分
        tmp_score = tmp.section.div.find('div', class_='box4 box').article.ul
        tmp_score = tmp_score.find_all('span', class_='text-danger')
        # 获得发行日期
        tmp_publish = tmp.section.div.find('div', class_='box4 box').article.ul
        tmp_publish = tmp_publish.find_all('span', class_='text-success')
        for i in range(0, len(tmp_cover)):
            j = {'serial':tmp_cover[i].get('alt'),
                 'cover':tmp_cover[i].get('src'),
                 'score':float(tmp_score[i].get_text()),
                 'publish':tmp_publish[i].get_text()}
            self.info['movie'].append(j)
            print(self.info['name']+' : ',
                  ' get '+str(i+1)+'/'+str(len(tmp_cover))+' , ',
                  j['serial']+' , ',
                  str(j['score'])+' , ',
                  j['publish'],
                  sep='')

    def save_db(self):
        """ 保存记录到db,保存图片"""
        import pymongo
        conn = pymongo.MongoClient(host=self.conn_info['host'], port=self.conn_info['port'])
        coll = conn.mydata.avdata
        coll.update_one({'name':self.info['name']},
                        {'$set':{'name':self.info['name'],
                                 'url':self.info['url'],
                                 'quantity':self.info['quantity'],
                                 'img':self.info['img'],
                                 'alias':self.info['alias'],
                                 'birth':self.info['birth'],
                                 'brief':self.info['brief'],
                                 'entry':self.info['entry'],
                                 'measurement':self.info['measurement'],
                                 'tag':self.info['tag']}},
                        upsert=True)
        coll = conn.mydata.avcover
        for i in self.info['movie']:
            coll.update({'serial':i['serial']},
                        {'$set':{'name':self.info['name'],
                                 'serial':i['serial'],
                                 'score':i['score'],
                                 'cover':i['cover'],
                                 'publish':i['publish']}},
                        upsert=True)
        conn.close

    def save_cover(self):
        import os
        from urllib import request
        save_path = 'd:/movie-HD11/'+self.info['name']+'/'
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        if not os.path.exists(save_path+self.info['name']+'.jpg'):
            request.urlretrieve(url=self.info['img'], filename=save_path+self.info['name']+'.jpg')
        for i in self.info['movie']:
            if not os.path.exists(save_path+i['serial']+'.jpg'):
                request.urlretrieve(url=i['cover'], filename=save_path+i['serial']+'.jpg')
                print(str(self.info['movie'].index(i)+1)+' saved : '+i['cover'])
            else:
                print('the file exist : '+i['serial']+'.jpg')

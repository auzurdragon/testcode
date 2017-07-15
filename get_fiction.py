flist = ['佣兵的战争','一世之尊','吾名雷恩',]
error_list = ['庶子风流','异世界的美食家','万岁约阿希姆','艾泽拉斯圣光轨迹',]
"""
td = MyFiction()
for i in flist:
    td.__init__(i)
    td.get_url()
    td.get_web()
    td.get_content()
    td.save_db()
    td.save_txt()
"""

class MyFiction(object):
    """ 小说管理 """
    def __init__(self, name=''):
        self.content = [] # 保存抓取的章节内容
        self.info_conn = {'host':'localhost', 'port':27017}
        self.info_db = {'name':name, 'author':'', 'url':'',
                        'num':0, 'lastchapter':'', 'updatedate':''}
        self.info_web = {'name':name, 'author':'', 'url':'',
                         'num':0, 'lastchapter':'', 'updatedate':''}

    def list_db(self):
        """ 列出数据库中的小说和最后一章 """
        import pymongo
        conn = pymongo.MongoClient(self.info_conn['host'], self.info_conn['port'])
        coll = conn.mydata.fiction
        tmp = coll.find({},{'_id':0, 'name':1, 'author':1, 'num':1, 'lastchapter':1, 'updatedate':1})
        for i in tmp:
            print('fiction name : %s ' % i['name'],
                  '      author : %s ' % i['author'],
                  '         num : %d ' % i['num'],
                  '        last : %s ' % i['lastchapter'],
                  '      update : %s ' %  i['updatedate'],
                  '-------------------------------------',
                  sep='\n')
        conn.close()


    def get_db(self, name=''):
        """ 在数据库中查找本小说是否存在，以及最后一章。返回dict数据到self.db_info """
        import pymongo
        if not name:
            name = self.info_db['name']
        conn = pymongo.MongoClient(self.info_conn['host'], self.info_conn['port'])
        coll = conn.mydata.fiction
        tmp = coll.find_one({'name':name},
                            {'_id':0, 'name':1, 'author':1, 'url':1,
                             'num':1, 'lastchapter':1, 'updatedate':1})
        if tmp:
            self.info_db = tmp
            print('Fiction name : %s ' % tmp['name'],
                  ' Author name : %s ' % tmp['author'],
                  '         URL : %s ' % tmp['url'],
                  ' Chapter num : %s ' % tmp['num'],
                  'Last chapter : %s ' % tmp['lastchapter'],
                  ' Update date : %s ' % tmp['updatedate'],
                  sep='\n')
            return(True)
        else:
            print('The fiction %s not exists in DB!, Please search URL!' % name)
            return(False)
        conn.close()

    def get_url(self, name='', index=0):
        """ 在顶点小说网http://www.23us.com 搜索小说链接"""
        from urllib import request, parse
        from bs4 import BeautifulSoup
        if not name:
            name = self.info_web['name']
        gurl = 'http://zhannei.baidu.com/cse/search?s=8253726671271885340&entry=1&q='+parse.quote(name)
        tmp = request.Request(gurl)
        tmp = request.urlopen(tmp).read().decode('utf-8', 'ignore')
        tmp = BeautifulSoup(tmp, 'lxml')
        tmp = tmp.body.div.find_all('div', class_='result-item')
        self.info_web['name'] = tmp[0].find('a', class_='result-game-item-title-link').get('title')
        self.info_web['url'] = tmp[0].find('a', class_='result-game-item-title-link').get('href')
        result_brief = tmp[0].find('p').get_text()
        print(' name : %s ' % self.info_web['name'],
              '  url : %s ' % self.info_web['url'],
              'brief : %s ' % result_brief,
              sep='\n')
        print('\n')

    def get_web(self):
        """ 从顶点小说网站抓取小说的目录，保存数据到self.info_get """
        from urllib import request
        from bs4 import BeautifulSoup
        import time
        tmp = request.urlopen(request.Request(self.info_web['url'])).read().decode("gbk", 'ignore')
        tmp = BeautifulSoup(tmp, 'lxml')
        self.info_web['author'] = tmp.head.select('meta[name="og:novel:author"]')[0]['content']
        tmp_content = tmp.table.select("a")
        for i in tmp_content:
            j = {}
            j['chapter_name'] = i.get_text()
            j['chapter_url'] = self.info_web['url']+i.get('href')
            self.content.append(j)
        self.info_web['num'] = len(self.content)
        self.info_web['lastchapter'] = self.content[-1]['chapter_name']
        self.info_web['updatedate'] = time.strftime('%Y-%m-%d')
        print('  Fiction name : %s ' % self.info_web['name'],
              'Author\'s name : %s ' % self.info_web['author'],
              '  Chapter num  : %d ' % self.info_web['num'],
              '  Last chapter : %s ' % self.info_web['lastchapter'],
              'db_chapter num : %s ' % self.info_db['num'],
              'db_lastchapter : %s ' % self.info_db['lastchapter'],
              '      need get : %d ' % (self.info_web['num']-self.info_db['num']),
              sep='\n')
        self.content = self.content[self.info_db['num']:]

    def get_content(self):
        """ 按content的结果，抓取小说内容"""
        from urllib import request
        from urllib import error
        from bs4 import BeautifulSoup
        get_id = list(range(0, len(self.content)))
        chapter_num = len(get_id)
        get_num = 1
        while len(get_id) > 0:
            i = get_id.pop()
            gurl = self.content[i]['chapter_url']
            try:
                tmp = request.urlopen(request.Request(gurl)).read().decode('gbk', 'ignore')
                tmp = BeautifulSoup(tmp, 'lxml').dl.select('dd#contents')
                self.content[i]['chapter'] = ''
                for j in tmp:
                    self.content[i]['chapter'] = self.content[i]['chapter'] + j.get_text()
                self.content[i]['chapter'] = self.content[i]['chapter'].replace('\xa0\xa0\xa0\xa0', '\n\r')
                return_info = ', need get '+str(i)+' , chapter num '+str(chapter_num)
            except:
                return_info = ' , get failed : '+self.content[i]['chapter_name']
                get_id.append(i)
            print('get '+str(get_num) + return_info)
            get_num += 1

    def save_db(self):
        """ 将抓到的小说更新信息，写入MongoDB"""
        import pymongo
        conn = pymongo.MongoClient(self.info_conn['host'], self.info_conn['port'])
        coll = conn.mydata.fiction
        coll.update_one({'name':self.info_web['name']},
                        {'$set':{'name':self.info_web['name'],
                                 'author':self.info_web['author'],
                                 'url':self.info_web['url'],
                                 'num':self.info_web['num'],
                                 'lastchapter':self.info_web['lastchapter'],
                                 'updatedate':self.info_web['updatedate']}},
                        upsert=True)
        """
        # 保存章节内容到数据库
        coll = conn.mydata.chapter
        for i in self.content:
            coll.update_one({'name':self.info_web['name'], 'chapter_name':i['chapter_name']},
                            {'$set':{'name':self.info_web['name'],
                                     'chapter_name':i['chapter_name'],
                                     'chapter':i['chapter']}},
                            upsert=True)
        """
        conn.close()
        print('%s has saved %d chapter' % (self.info_web['name'], len(self.content)))

    def save_txt(self, path='h:/getfiction/'):
        """ 写入到txt文件 """
        filename = path+self.info_web['name']+'.txt'
        with open(filename, 'a+', encoding='utf8') as writer:
            for i in self.content:
                writer.write('\n\r'+i['chapter_name'])
writer.write('\n\r'+i['chapter'])
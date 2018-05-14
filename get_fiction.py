"""
    依赖包
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple lxml
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple bs4
    小说来源：http://www.x23us.com/quanben/1
    ip库66ip，xicidaili，data5u，proxydb
"""
__auth__ = "Andy"
class Fiction(object):
    """ 小说管理 
    """
    def __init__(self, name=''):
        self.fundb = {
            'host':'localhost',
            'port':28010,
            "db":"fun_db",
            "coll":"fictions",
        }
        # 保存小说目录和信息
        self.fiction = {
            'name':name,   # 小说名称
            'author':'',    # 作者
            'fromsite':'http://www.23us.com/',   # 来源网站
            'url':'',      # url
            'num':int(0),   # 章节数量
            'chapter':[
                {
                    'title':'', # 章节名称
                    'url':'',  # 章节URL
                    'status':False, # 抓取状态
                    'content':'',   # 章节内容
                },
            ],
        }
        # 保存目录
        self.fpath = "D:/Mydownload/fiction/"
        # 抓取的小说
        self.filelist = [
            '好莱坞制作', '邪神旌旗', '我的二战不可能这么萌',  
            '一世富贵', '穿越1630之崛起南美', '德意志崛起之路', '复活之战斗在第三帝国', 
            '神游', '鬼股', '灵山', '地师', '惊门', '太上章', '人欲', '烽皇', '大圣直播间', '致命武力之新世界', '无限道武者路', '黑暗王者',
            '黑夜将至', '君临诸天', '我在末世有套房', '银河霸主饲养手记', 
            '连环杀手在美国', '直播之荒野挑战', '诡神冢',  
            '交锋', '魔神乐园', '银狐', '唐砖', '阳神', '艾泽拉斯圣光轨迹', '帝国霸主', '交锋',
            '我的末世基地车', '历史粉碎机', '月之影面', '无穷重阻', '永恒国度', '剑破江山', 
            '不可思议的圣剑', '深海提督', '大艺术家', '巨星', '大偶像', '大戏骨', '第三帝国',
            '战锤40K之远东风暴', '热闹喧嚣的彪悍人生', '暴风雨中的蝴蝶', 
            '美漫之哥谭黑暗教父',
        ]
        self.urllist = [
            {'name':'', 'url':'',}
        ]
        # 代理IP池 
        self.proip = []
        self.proips = []
        # 伪造header头
        self.header = [
            {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"},
            # Chrome + Win7
            {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},
            # Firefox + Win7:
            {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'},
            # Safari + Win7:
            {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
            # Opera + Win7:
            {"User-Agent":'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'},
            # IE + Win7+ie9：
            {"User-Agent":'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'},
            # Win7+ie8：
            {"User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'},
            # WinXP+ie8：
            {"User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)'},
            # WinXP+ie7：
            {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
            # WinXP+ie6：
            {"User-Agent":'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'},
            # 傲游3.1.7在Win7+ie9,高速模式:
            {"User-Agent":'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12'},
            # 傲游3.1.7在Win7+ie9,IE内核兼容模式:
            {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'},
            # 搜狗3.0在Win7+ie9,IE内核兼容模式:
            {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)'},
            # 搜狗3.0在Win7+ie9,高速模式:
            {"User-Agent":'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0'},
            # 360浏览器3.0在Win7+ie9:
            {"User-Agent":'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'},
            # QQ浏览器6.9(11079)在Win7+ie9,极速模式:
            {"User-Agent":'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'},
            # QQ浏览器6.9(11079)在Win7+ie9,IE内核兼容模式:
            {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201'},
            # 阿云浏览器1.3.0.1724 Beta(编译日期2011-12-05)在Win7+ie9:
            {"User-Agent":'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'},
        ]
    def get_proip(self, indexn="1"):
        """获得代理IP"""
        import requests
        from bs4 import BeautifulSoup as bs
        ipurl = "http://www.xicidaili.com/wt/"+indexn
        print(ipurl)
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
        }
        tmp = requests.get(ipurl, headers = header)
        tmp = bs(tmp.content.decode(), "lxml")
        tmp = tmp.select("table")[0].find_all("tr")
        for i in tmp[1:]:
            x = i.find_all("td")
            j = ("%s:%s" % (x[1].text, x[2].text))
            try:
                t =requests.get("http://ip.cip.cc/" , headers = header, proxies={"http":j}, timeout=1)
                if t.ok:
                    print(t.content)
                    self.proip.append(j)
            except Exception as e:
                print(e)
    def geturl_qingk(self):
        """在请看小说搜索链接"""
        import requests
        import random
        from bs4 import BeautifulSoup as bs
        url = 'https://www.qingkan9.com/novel.php?action=search&searchtype=novelname&searchkey=%s' % self.fiction['name']
        url = requests.utils.quote(url, safe=':/?&=', encoding='gbk')
        tmp = bs(requests.get(url, headers=random.choice(self.header)).content, 'lxml')
        tmp = tmp.body.div.find('div', class_='ss_box')
        self.fiction['name'] = tmp.a.text
        self.fiction['url'] = tmp.a.get('href')
        self.fiction['brief'] = tmp.p.text
        self.fiction['author'] = tmp.a.next_sibling.replace(' ','').replace('/','')
        self.fiction['fromsite'] = 'https://www.qingkan9.com/'
        print('  name : %s' % self.fiction['name'],
              'author : %s' % self.fiction['author'],
              ' brief : %s' % self.fiction['brief'],
              '   url : %s' % self.fiction['url'],
              sep='\n')
    def getcatalog_qingk(self):
        """从请看小说抓取目录"""
        import requests, random
        from bs4 import BeautifulSoup as bs
        # 获得TXT下载页面的链接，网站将TXT下载链接和目录放在同个页面
        tmp = bs(requests.get(self.fiction['url'],  headers=random.choice(self.header)).content, 'lxml')
        url = tmp.body.find('div', id='Chapters').find_all('a')[3].get('href')
        # 获得TXT下载页面的内容
        tmp = bs(requests.get(url,  headers=random.choice(self.header)).content, 'lxml')
        # 抓取txt文件下载链接
        furl = tmp.body.div.find_all('a')[2].get('href')
        # 抓取目录
        tmp = tmp.body.find('div', id='Chapters')
        self.fiction['chapter'] = [{'title':item.text, 'url':item.get('href'), 'status':True} for item in tmp.find_all('a')]
        self.fiction['num'] = len(self.fiction['chapter'])
        # 保存txt文件
        tmp = requests.get(furl)
        filename = self.fpath + self.fiction['name']+'.txt'
        with open(filename, 'wb') as writer:
            writer.write(tmp.content)
        print('chapter number : %d' % len(self.fiction['chapter']),
              '  last chapter : %s' % self.fiction['chapter'][-1]['title'],
              sep='\n')
    def geturl_dingd(self):
        """ 在顶点小说网http://www.23us.com 搜索小说链接"""
        import requests, random
        from bs4 import BeautifulSoup as bs
        # 注意站内搜索的s值会变化
        url = 'http://zhannei.baidu.com/cse/search?s=5592277830829141693&q=%s' % self.fiction['name']
        tmp = bs(requests.get(
            url,
            headers=random.choice(self.header),
            # proxies={'http':random.choice(self.proip)}
        ).content, 'lxml')
        tmp = tmp.body.div.find('div', class_='result-game-item-detail')
        self.fiction['name'] = tmp.a.get('title')
        self.fiction['url'] = tmp.a.get('href')
        self.fiction['brief'] = tmp.p.text
        self.fiction['author'] = tmp.div.a.text.replace('\r\n', '').replace(' ', '')
        self.fiction['fromsite'] = 'http://www.23us.com/'
        print('  name : %s' % self.fiction['name'],
              'author : %s' % self.fiction['author'],
              ' brief : %s' % self.fiction['brief'],
              '   url : %s' % self.fiction['url'],
              sep='\n')
    def getcatalog_dingd(self):
        """从顶点小说网抓取小说目录"""
        import requests, random
        from bs4 import BeautifulSoup as bs
        tmp = requests.get(self.fiction['url'], headers=random.choice(self.header))
        tmp = bs(tmp.content, 'lxml')
        tmp = tmp.body.find('table')
        tmp = tmp.find_all('a')
        self.fiction['chapter'] = [{'title':item.text, 'url':self.fiction['url'] + item.get('href'), 'status':False} for item in tmp]
        self.fiction['num'] = len(self.fiction['chapter'])
        print('chapter number : %d' % len(self.fiction['chapter']),
              '  last chapter : %s' % self.fiction['chapter'][-1]['title'],
              sep='\n')
        return self.fiction['chapter']
    def getcontent_dingd(self):
        """从顶点小说抓取单章节内容"""
        import requests, random, time
        from bs4 import BeautifulSoup as bs
        print('getcontent_dingd %s , chapter %d' %(self.fiction['name'], self.fiction['num']))
        total = 0
        error = 0
        for item in self.fiction['chapter']:
            if not item['status']:
                try:
                    tmp = bs(requests.get(
                        item['url'], 
                        headers=random.choice(self.header), 
                        timeout=2,
                        # proxies={'http':random.choice(self.proip)}, timeout=3
                        ).content, 'lxml')
                    item['content'] = tmp.body.find('dd', id='contents').text.replace('\xa0\xa0', '\n')
                    item['status'] = True
                    print('getcontent_dingd success %s' % item['title'])
                except Exception as errorinfo:
                    item['content'] = ''
                    error += 1
                    print('getcontent_dingd failed %s' % errorinfo)
                    time.sleep(5)
                time.sleep(1)
                total += 1
        print('complete! total %d , error %d' % (total, error))
    def save_txt(self):
        """保存到文件"""
        import os
        filename = self.fpath + self.fiction['name']+'.txt'
        try:
            with open(filename, 'w+', encoding='utf8') as writer:
                for item in self.fiction['chapter']:
                    writer.write('\n\r' + item['title'] + '\n\r' + item['content'] + '\n\r')
            self.save_db()
            print('%s save success, %d chapter' % (self.fiction['name'], len(self.fiction['chapter'])))
            os.remove('%stmp.pkl' % self.fpath)
            print('tmp pkl delete.')
        except Exception as e:
            print('%s save failed, error: %s ' % (self.fiction['name'], e))
    def save_db(self):
        """保存到数据库"""
        import time
        from pymongo import MongoClient as mc
        conn = mc(host=self.fundb['host'], port=self.fundb['port'])
        conn = conn.get_database(self.fundb['db'])
        conn = conn.get_collection(self.fundb['coll'])
        conn.update(
            {'name':self.fiction['name']},
            {'$set':
                {'name':self.fiction['name'],
                 'author':self.fiction['author'],
                 'fromsite':self.fiction['fromsite'],
                 'url':self.fiction['url'],
                 'num':self.fiction['num'],
                 'update':int(time.time())
                }
            },
            upsert=True)
        for item in self.fiction['chapter']:
            if item['status']:
                conn.update(
                    {'name':self.fiction['name']},
                    {'$push':{'chapter':{'title':item['title'], 'url':item['url'], 'status':item['status']}}}
                )
    def save_tmp(self):
        """保存对象到临时文件"""
        import pickle
        filename = self.fpath + 'tmp.pkl'
        with open(filename, 'wb') as writer:
            pickle.dump(self.fiction, writer)
    def load_tmp(self):
        """加载临时文件到self.fiction"""
        import pickle
        filename = self.fpath + 'tmp.pkl'
        with open(filename, 'rb') as reader:
            self.fiction = pickle.load(reader)
    def get_dblist(self, name=''):
        """
            从数据库查询已获得的小说信息，name=小说名字，模糊查询，默认空白，查询全部列表
        """
        from pymongo import MongoClient
        conn = MongoClient(host=self.fundb['host'], port=self.fundb['port'])
        conn = conn.get_database(self.fundb['db']).get_collection(self.fundb['coll'])
        if name:
            tmp = conn.find(
                {'$or':[{'name':{'$regex':name}}, {'author':{'$regex':name}}]},
                {'_id':0, 'name':1, 'author':1, 'num':1, 'update':1})
            if tmp.count() > 0:
                for i in tmp:print(i)
                return tmp
            else:
                print('db not existed : %s' % name)
                return None
        else:
            tmp = conn.find({}, {'_id':0, 'name':1, 'author':1, 'num':1, 'update':1})
            for i in tmp: print(i)
            return tmp
    def geturl_23wx(self):
        """从 www.23wx.com 抓取小说"""
        import requests, random
        from bs4 import BeautifulSoup as bs
        url = "http://www.23wx.cm/modules/article/search.php"
        # 构造post请求
        body = {'action':'login', 'searchkey':self.fiction['name'].encode('gb2312')}
        tmp = requests.post(url=url, data=body, headers=random.choice(self.header), timeout=5)
        if tmp.url == url:
            tmp = bs(tmp.content, 'lxml')
            tmp = tmp.find('table', class_='grid')
            tmp = tmp.find_all('tr')[1:]
            result = []
            print('%s , %s , %s , %s , %s' % ('index', 'name', 'author', 'lchapter', 'wordnum'))
            for item in tmp:
                t = item.find_all('td')[0:4]
                ind = tmp.index(item)
                name = t[0].a.text
                url = t[0].a.get('href')
                author = t[2].text
                lchapter = t[1].a.text
                wordnum = t[3].text
                result.append({
                    'url':url,
                    'author':author,
                })
                print('%d , %s , %s , %s , %s' % (ind, name, author, lchapter, wordnum))
            ind = int(input('指定抓取的小说[1-9] : '))
            self.fiction['fromsite'] = 'http://www.23wx.com'
            self.fiction['url'] = result[ind]['url']
            tmp = requests.get(result[ind]['url'])
            tmp = bs(tmp.content, 'lxml')
        else:
            self.fiction['fromsite'] = 'http://www.23wx.com'
            self.fiction['url'] = tmp.url
            tmp = bs(tmp.content, 'lxml')
        self.fiction['author'] = tmp.body.find('span', class_='item red').text.replace('作者：', '')
        tmp = tmp.body.find('div', class_='book_list')
        tmp = tmp.select('a')
        for i in tmp:
            self.fiction['chapter'].append({
                'title':i.text,
                'url':'%s%s' % (self.fiction['url'][0:-10],i.get('href')),
                'status': False,
                'content': '',
            })
        self.fiction['num'] = len(self.fiction['chapter'])
        print(self.fiction['name'], self.fiction['author'], self.fiction['num'], sep='\n')
    def getcontent_23wx(self):
        """抓取小说章节"""
        import requests, random, time, pickle
        from bs4 import BeautifulSoup as bs
        errors = 0
        # 计算需要抓取的章节数量
        chapter_num = 0
        for i in self.fiction['chapter']:
            if not i['status']:
                chapter_num += 1
        for i in self.fiction['chapter']:
            if i['status']:
                continue
            else:
                try:
                    tmp = requests.get(i['url'], headers=random.choice(self.header), timeout=3)
                    time.sleep(0.5)
                    tmp = bs(tmp.content, 'lxml')
                    i['content'] = tmp.body.find('div', id='htmlContent').text.replace('\xa0', '')
                    i['status'] = True
                    current = self.fiction['chapter'].index(i)
                    if current % 100 == 0:
                        with open('%stmp.pkl' % self.fpath, 'wb') as w:
                            pickle.dump(self.fiction, w)
                    print('success %d / %d : %s ' % (current, chapter_num , i['title']))
                except Exception as e:
                    print('failed  : %s , %s' % (i['title'], e))
                    errors += 1                    
        print( 'failed sum : %d' % errors)
        return errors
    def getcontent_db(self):
        """
            从数据库中获得小说的章节,并更新等待抓取的小说章节列表。
        """
        from pymongo import MongoClient
        conn = MongoClient(host=self.fundb['host'], port=self.fundb['port'])
        conn = conn.get_database(self.fundb['db'])
        conn = conn.get_collection(self.fundb['coll'])
        tmp = conn.find_one({'name':self.fiction['name']},{'_id':0})
        chapter = tmp['chapter'][-1]['title']
        # 如果数据库中的章节数量小于待抓取的章节数量，则更新待抓取列表
        if tmp['num'] < self.fiction['num']:
            num = self.fiction['num'] - tmp['num']
            for ind in range(self.fiction['num']):
                if self.fiction['chapter'][ind]['title'] == chapter:
                    break
        self.fiction['chapter'] = self.fiction['chapter'][ind+1:-1]
        print('wait get : %d' % num)
        print('get from : %s' % self.fiction['chapter'][0]['title'])
    def getchapter_db(self, name=''):
        """
            从数据库获得指定小说的章节名称列表
        """
        from pymongo import MongoClient
        conn = MongoClient(host=self.fundb['host'], port=self.fundb['port'])
        conn = conn.get_database(self.fundb['db']).get_collection(self.fundb['coll'])
        chapter = conn.find_one(
            {'$or':[{'name':{'$regex':name}}, {'author':{'$regex':name}}]},
            {'_id':0, 'chapter':1},
        )
        if chapter:
            chapter = chapter['chapter']
            return chapter
        else: 
            print(' %s not exists' % name)
            return False
 
if __name__ == '__main__':
    import sys
    s = Fiction()
    flist = sys.argv[1:]
    if len(flist) == 0:
        print(s.filelist)
        s.get_dblist()
    else:
        for filename in flist:
            s.__init__(filename)
            s.get_dblist(filename)
            s.geturl_23wx()
            # choose = input("是否继续抓取，Yes, No : ")
            choose = "Y"
            if choose.upper() == "N":
                continue
            else:
                T = 2
                while T > 1:
                    T =  s.getcontent_23wx()
                s.save_txt()

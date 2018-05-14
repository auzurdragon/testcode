"""
    依赖包
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple lxml
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple bs4

    小说来源：http://www.x23us.com/quanben/1

"""

__auth__ = "Andy"

class Fiction(object):
    """ 小说管理 
        get_url(), 按小说名称从网站上找到目录页面的链接
        get_catalog(), 按小说目录页面链接，抓取各个章节的页面链接
        get_content(self,gurl), 抓取单章节页面的内容
        get_fiction(), 按照self.fict_cont中保存的各个章节的状态和页面链接，抓取状态false的页面内容
        save_db(), 将self.fict_cont的章节内容，保存到数据库
        save_txt(), 将self.fict_cont的各章节内容，保存到txt文件
    """
    def __init__(self, name=''):
        self.content = [] # 保存抓取的章节内容
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
        self.fpath = "d:/mydb/fiction/"
        # 抓取的小说
        self.filelist = [
            '剑与魔法与出租车', '异常生物见闻录', '影帝的日常', '儒道至圣', '熊猫人的自我修养', '守望黎明号', '美漫之大冬兵', '俗人回档',
            '完美人生', '美食供应商', '恐怖广播', '仙逆', '放开那个女巫', '暴风法神', '惊悚乐园', '超级怪兽工厂','巨星夫妻', "大影帝",
            "万岁约阿希姆", "当个法师闹革命", "娱乐之荒野食神", "材料帝国", "废土崛起", "修真聊天群", "奋斗在红楼", "文艺时代", "最佳影星",
            "好莱坞制作", "好莱坞之路", "调教大宋", "大影帝", "圣者", "当个法师闹革命", "艾泽拉斯圣光轨迹", "邪神旌旗", "我的1979",
            "莽穿新世界", "重生完美时代", "超级怪兽工厂", "重生日本当厨神", "电影教师", "一世富贵", "穿越1630之崛起南美", "德意志崛起之路",
            "唐朝工科生", "复活之战斗在第三帝国", "哈利波特与秘密宝藏", "我的魔法时代",  "神游", "鬼股", "灵山", "地师", "惊门", "太上章", "人欲" ,
            "天书奇谭", '天择', '最后一个使徒',
        ]
        self.errorlist = [
            "寻找走丢的舰娘", "革命吧女神", "漫威世界的术士", "顾道长生", "当个法师闹革命", "艾泽拉斯圣光轨迹",
            "莽穿新世界", "霜寒之翼", "大宋好屠夫", "帝国霸主", "第三帝国", "潮汐进化","吾名雷恩", "交锋",'天道图书馆',
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

    def geturl_dingd(self):
        """ 在顶点小说网http://www.23us.com 搜索小说链接"""
        import requests, random
        from bs4 import BeautifulSoup as bs
        # 注意站内搜索的s值会变化
        url = 'http://zhannei.baidu.com/cse/search?s=5592277830829141693&q=%s' % self.fiction['name']
        tmp = bs(requests.get(url, headers=random.choice(self.header)).content, 'lxml')
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
                    tmp = bs(requests.get(item['url'], headers=random.choice(self.header), timeout=3).content, 'lxml')
                    item['content'] = tmp.body.find('dd', id='contents').text.replace('\xa0\xa0', '\n')
                    item['status'] = True
                    print('getcontent_dingd success %s' % item['title'])
                except Exception as errorinfo:
                    item['content'] = ''
                    error += 1
                    print('getcontent_dingd failed %s' % errorinfo)
                time.sleep(1)
                total += 1
        print('complete! total %d , error %d' % (total, error))

    def save_txt(self):
        """保存到文件"""
        filename = self.fpath + self.fiction['name']+'.txt'
        with open(filename, 'w+', encoding='utf8') as writer:
            for item in self.fiction['chapter']:
                writer.write('\n\r' + item['title'] + '\n\r' + item['content'] + '\n\r')

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

if __name__ == "__main__":
    s = Fiction()
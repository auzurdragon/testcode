"""
    依赖包
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple lxml
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple bs4

    小说来源：http://www.x23us.com/quanben/1

"""

class Fiction(object):
    """ 小说管理 
        get_url(), 按小说名称从网站上找到目录页面的链接
        get_catalog(), 按小说目录页面链接，抓取各个章节的页面链接
        get_content(self,gurl), 抓取单章节页面的内容
        get_fiction(), 按照self.fict_cont中保存的各个章节的状态和页面链接，抓取状态false的页面内容
        save_db(), 将self.fict_cont的章节内容，保存到数据库
        save_txt(), 将self.fict_cont的各章节内容，保存到txt文件

    
    """
    def __init__(self, title=''):
        self.content = [] # 保存抓取的章节内容
        self.conn_info = {
            'host':'localhost',
            'port':28010,
            "db":"mydata",
            "coll":"web_fiction",
            "co_catalog":"fiction_catalog",
        }
        # 保存小说目录和信息
        self.fict_info = {
            'title':title, 'author':'', 'url':'',
            'num':0, 'lastchapter':'',
        }
        # 保存待抓取的章节内容
        self.fict_cont = [
            # {'_id':ObjectId(), 'title':'书名', 'chapter':'章节名', 'curl':'章节链接', 'status':false, 'content':'章节内容'},
        ]
        # 保存目录
        self.file_path = "F:/getfiction/"
        # 抓取的小说
        self.files = ["守望黎明号",]
        # 代理IP池
        self.proip = ["120.132.71.212:80", "120.7.84.59:8118","27.46.20.132:8888","117.66.87.67:8118","111.155.116.212:8123",]

    def get_proip(self):
        """获得代理IP"""
        import requests
        from bs4 import BeautifulSoup as bs
        ipurl = "http://www.xicidaili.com/wt/"
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
        }
        tmp = requests.get(ipurl, headers = header)
        tmp = bs(tmp.content.decode(), "lxml")
        tmp = tmp.select("table")[0].find_all("tr")
        for i in tmp[1:]:
            x = i.find_all("td")
            j = ("%s:%s" % (x[1].text, x[2].text))
            self.proip.append(j)
        print("get %d ip" % len(tmp[1:]))

    def get_db(self, status=False):
        """ 从数据库中查找没有抓取到的章节 """
        from pymongo import MongoClient
        conn = MongoClient(host=self.conn_info["host"], port=self.conn_info["port"])
        db = conn.get_database(self.conn_info["db"])
        # 查询小说名称是否存在，是则返回作者、最后一章，以及各章节的抓取状态
        coll = db.get_collection(self.conn_info["co_catalog"])
        check = coll.find_one({"title":self.fict_info["title"]})
        if check:
            self.fict_info["title"] = check["title"]
            self.fict_info["author"] = check["author"]
            self.fict_info["url"] = check["url"]
            self.fict_info["num"] = check["num"]
            self.fict_info["lastchapter"] = check["lastchapter"]
            print ("%s 在数据库中有记录，最后一章：%s" % (self.fict_info["title"], self.fict_info["lastchapter"]))
            # 从web_fiction表中提取抓取失败的章节记录
            coll = db.get_collection(self.conn_info["coll"])
            tmp = list(coll.find({"title":self.fict_info["title"], "status":False}, {"content":0}))
        coll = conn.get_database(self.conn_info["db"]).get_collection(self.conn_info["coll"])
        self.fict_cont = list(coll.find({"title":self.fict_info["title"], "status":status}))
        print("from mongodb get %d chapter" % len(self.fict_cont))

    def get_url(self):
        """ 在顶点小说网http://www.23us.com 搜索小说链接"""
        from urllib import request, parse
        from bs4 import BeautifulSoup
        # 注意站内搜索的s值会变化
        gurl = 'http://zhannei.baidu.com/cse/search?s=5592277830829141693&entry=1&q='+parse.quote(self.fict_info["title"])
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
        }
        req = request.Request(gurl, headers=header)
        tmp = request.urlopen(req).read().decode('utf-8', 'ignore')
        tmp = BeautifulSoup(tmp, 'lxml')
        tmp = tmp.body.div.find_all('div', class_='result-item')
        self.fict_info['title'] = tmp[0].find('a', class_='result-game-item-title-link').get('title')
        self.fict_info['url'] = tmp[0].find('a', class_='result-game-item-title-link').get('href')
        result_brief = tmp[0].find('p').get_text()
        print(' title : %s ' % self.fict_info['title'],
              '  url : %s ' % self.fict_info['url'],
              'brief : %s ' % result_brief,
              sep='\n')
        print('\n')

    def get_catalog(self):
        """ 从顶点小说网站抓取小说的目录，保存数据到self.fict_info """
        from urllib import request
        from bs4 import BeautifulSoup
        import time
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
        }
        req = request.Request(self.fict_info["url"], headers=header)
        tmp = request.urlopen(req).read().decode("gbk", 'ignore')
        tmp = BeautifulSoup(tmp, 'lxml')
        self.fict_info['author'] = tmp.head.select('meta[name="og:novel:author"]')[0]['content']
        tmp_content = tmp.table.select("a")
        for i in tmp_content:
            j = {}
            j['title'] = self.fict_info["title"]
            j['chapter'] = i.get_text()
            j['curl'] = self.fict_info['url']+i.get('href')
            j['status'] = False
            j['content'] = ""
            self.fict_cont.append(j)
        self.fict_info['num'] = len(self.fict_cont)
        self.fict_info['lastchapter'] = self.fict_cont[-1]['chapter']
        self.fict_info['updatedate'] = time.strftime('%Y-%m-%d')
        print('  Fiction name : %s ' % self.fict_info['title'],
              'Author\'s name : %s ' % self.fict_info['author'],
              '  Chapter num  : %d ' % self.fict_info['num'],
              '  Last chapter : %s ' % self.fict_info['lastchapter'],
              sep='\n')

    # def get_content(self, gurl):
    #     """ 抓取单章节小说内容 """
    #     from urllib import request
    #     from urllib import error
    #     from bs4 import BeautifulSoup
    #     import requests
    #     import random
    #     pro = self.proip
    #     try:
    #         header = {
    #            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
    #         }
    #         pro = ["120.132.71.212:80",]
    #         req = request.Request(gurl, headers=header)
    #         tmp = request.urlopen(req).read().decode('gbk', 'ignore')
    #         tmp = BeautifulSoup(tmp, 'lxml').dl.select("dd#contents")
    #         result = tmp[0].get_text().replace("\xa0\xa0\xa0\xa0", "\n\r")
    #         return result
    #     except Exception as e:
    #         print(e)
    #         return False

    def get_content(self, gurl):
        """ 抓取单章节小说内容 """
        import requests
        import random
        from bs4 import BeautifulSoup as bs
        # 构造header请求头
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
        }
        # 用于保存结果的tmp
        tmp = False
        # 判断IP池是否还有可用的代理IP，如果没有则直接使用本机的IP
        if self.proip:
            choiceip = random.choice(self.proip)
        else:
            choiceip = ""
            print("IP池为空，需要更新IP池")
        try:
            request = requests.get(
                gurl,
                proxies = {"http":choiceip},
                headers = header
            )
            if request.ok:
                tmp = request.content.decode("gbk","ignore")
                tmp = bs(tmp, "lxml").dl.select("dd#contents")[0]
                tmp = tmp.get_text().replace("\xa0\xa0\xa0\xa0", "\n\r")
            else:
                print("ip %s get failed" % choiceip)
                self.proip.remove(choiceip)
        except Exception as per:
            print("ip %s get failed, %s" % (choiceip,per))
            self.proip.remove(choiceip)
        finally:
            return tmp

    def save_db(self):
        """ 将抓到的小说章节，写入MongoDB"""
        import pymongo
        conn = pymongo.MongoClient(self.conn_info['host'], self.conn_info['port'])
        db = conn.get_database(self.conn_info["db"])
        coll = db.get_collection(self.conn_info["coll"])
        for item in self.fict_cont:
            try:
                coll.update_one(
                    {
                        "title":item["title"],
                        "chapter":item["chapter"]
                    },
                    {
                        "$set":{
                            "title":item["title"],
                            "chapter":item["chapter"],
                            "curl":item["curl"],
                            "status":item["status"],
                            "content":item["content"],
                        }
                    },
                    upsert=True
                )
                print('%s: %s has been saved' % (item['title'], item["chapter"]))
            except:
                print("%s: %s save failed" % (item["title"], item["chapter"]))
        try:
            coll = db.get_collection(self.conn_info["co_catalog"])
            coll.update_one(
                {
                    "title":self.fict_info["title"]
                },
                {
                    "$set":{
                        "author":self.fict_info["author"],
                        "url":self.fict_info["url"],
                        "num":int(self.fict_info["num"]),
                        "lastchapter":self.fict_cont[-1]["chapter"],
                    }
                },
                upsert = True
            )
            print("%s save success" % self.fict_info["title"])
        except:
            print("%s save catalog failed" % self.fict_info["title"])
        conn.close()

    def save_txt(self):
        """ 写入到txt文件 """
        filename = self.file_path+self.fict_info['title']+'.txt'
        with open(filename, 'a+', encoding='utf8') as writer:
            for i in self.fict_cont:
                writer.write('\n\r'+i["chapter"]+"\n\r"+i['content'])

    def get_fiction(self, sleept=[2, 5]):
        """抓取小说内容, sleep指定每次抓取成功或失败后的休眠时间"""
        from time import sleep
        success = int(0)
        errors = int(0)
        for i in self.fict_cont:
            if i["status"]:
                continue
            else:
                result = self.get_content(i["curl"])
                if result:
                    i["content"] = result
                    i["status"] = True
                    success += 1
                    print("成功： %s " % i["chapter"])
                    sleep(sleept[0])
                else:
                    i["status"] = False
                    errors += 1
                    print("失败： %s" % i["chapter"])
                    sleep(sleept[1])
        print("抓取：%d 章，成功：%d 章，失败：%d 章" % ((success + errors), success, errors))

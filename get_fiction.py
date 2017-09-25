"""
    依赖包
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple lxml
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple bs4

    小说来源：http://www.x23us.com/quanben/1

"""

class Fiction(object):
    """ 小说管理 """
    def __init__(self, title=''):
        self.content = [] # 保存抓取的章节内容
        self.info_conn = {
            'host':'localhost',
            'port':28010,
            "db":"mydata",
            "coll":"web_fiction"
        }
        # 保存小说目录和信息
        self.fict_info = {
            'title':title, 'author':'', 'url':'',
            'num':0, 'lastchapter':'', 'updatedate':'',
            'catalog':[
                {'name':'', 'url':''},
            ]
        }
        # 保存章节内容
        self.fict_cont = [
            # {'_id':ObjectId(), 'title':'书名', 'chapter':'章节名', 'curl':'章节链接', 'status':false, 'content':'章节内容'},
        ]

    def db_content(self):
        """ 从数据库中查找没有抓取到的章节 """
        from pymongo import MongoClient
        conn = MongoClient(host=self.info_conn["host"], port=self.info_conn["port"])
        coll = conn.get_database(self.info_conn["db"]).get_collection(self.info_conn["coll"])
        self.fict_cont = list(coll.find({"title":self.fict_info["title"], "status":False}))
        print("from mongodb get %d chapter" % len(self.fict_cont))

    def get_url(self):
        """ 在顶点小说网http://www.23us.com 搜索小说链接"""
        from urllib import request, parse
        from bs4 import BeautifulSoup
        # 注意站内搜索的s值会变化
        gurl = 'http://zhannei.baidu.com/cse/search?s=5592277830829141693&entry=1&q='+parse.quote(name)
        tmp = request.Request(gurl)
        tmp = request.urlopen(tmp).read().decode('utf-8', 'ignore')
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
        tmp = request.urlopen(request.Request(self.fict_info['url'])).read().decode("gbk", 'ignore')
        tmp = BeautifulSoup(tmp, 'lxml')
        self.fict_info['author'] = tmp.head.select('meta[name="og:novel:author"]')[0]['content']
        tmp_content = tmp.table.select("a")
        for i in tmp_content:
            j = {}
            j['title'] = self.fict_info["title"]
            j['chapter'] = i.get_text()
            j['curl'] = self.fict_info['url']+i.get('href')
            j['status'] = False
            self.fict_cont.append(j)
        self.fict_info['num'] = len(self.fict_cont)
        self.fict_info['lastchapter'] = self.fict_cont[-1]['name']
        self.fict_info['updatedate'] = time.strftime('%Y-%m-%d')
        print('  Fiction name : %s ' % self.fict_info['title'],
              'Author\'s name : %s ' % self.fict_info['author'],
              '  Chapter num  : %d ' % self.fict_info['num'],
              '  Last chapter : %s ' % self.fict_info['lastchapter'],
              sep='\n')

    def get_content(self, gurl):
        """ 抓取单章节小说内容 """
        from urllib import request
        from urllib import error
        from bs4 import BeautifulSoup
        try:
            tmp = request.urlopen(request.Request(gurl)).read().decode('gbk', 'ignore')
            tmp = BeautifulSoup(tmp, 'lxml').dl.select("dd#contents")
            result = tmp[0].get_text().replace("\xa0\xa0\xa0\xa0", "\n\r\n\r")
            return result
        except Exception as e:
            print(e)
            return False

    def save_db(self):
        """ 将抓到的小说章节，写入MongoDB"""
        import pymongo
        conn = pymongo.MongoClient(self.info_conn['host'], self.info_conn['port'])
        coll = conn.get_database(self.info_conn["db"]).get_collection(self.info_conn["coll"])
        for item in s.fict_cont:
            try:
                coll.update_one(
                    {
                        "_id":item["_id"]
                    },
                    {
                        "$set":{
                            "status":item["status"],
                            "content":item["content"],
                        }
                    },
                    upsert=True
                )
                print('%s: %s has been saved' % (item['title'], item["chapter"]))
            except:
                print("%s: %s save failed" % (item["title"], item["chapter"]))
        conn.close()

    def save_txt(self, path='h:/getfiction/'):
        """ 写入到txt文件 """
        filename = path+self.info_web['name']+'.txt'
        with open(filename, 'a+', encoding='utf8') as writer:
            for i in self.content:
                writer.write('\n\r'+i['chapter_name'])

if __name__ == "__main__":
    from get_fiction import Fiction
    from time import sleep
success = int(0)
errors = int(0)
for i in s.fict_cont:
    if i["status"]:
        continue
    else:
        result = s.get_content(i["curl"])
        if result:
            i["content"] = result
            i["status"] = True
            success += 1
            print("成功： %s " % i["chapter"])
            sleep(1)
        else:
            i["status"] = False
            errors += 1
            print("失败： %s" % i["chapter"])
            sleep(5)

print("抓取：%d 章，成功：%d 章，失败：%d 章" % ((success + errors), success, errors))

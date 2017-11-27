#coding:utf-8
"""抓取豆瓣电影资料"""

class get_douban(object):
    """抓取豆瓣电影资料"""
    def __init__(self, startnum=0): # startnum是第一条记录的位置，每次抓取20条
        self.movie_list = []
        self.db = {'host':'112.74.161.9', 'port':28010, 'db':'ha_test','collection':'movie_douban'}
        self.startnum = startnum
    
    def get_movielist(self):
        """获得电影列表"""
        import requests
        # 拼接简介列表请求的网址, startnum=0则查询0-19条记录。
        url = 'https://movie.douban.com/j/new_search_subjects?sort=T&tags=电影&start=%d' % self.startnum
        # 获得前20条的记录
        tmp = requests.get(url)
        # 转成list
        tmp = tmp.json()['data']
        # 保存所需要的数据
        for i in tmp:
            self.movie_list.append({
                'title':i['title'],
                'rate':int(float(i['rate'])*10),
                'director':i['directors'],
                'casts':i['casts'],
                'url':i['url'],
                'tags':[],
                'country':'',
                'release':'',
                'minutes':int(0)
            })
    
    def get_oneinfo(self):
        """逐个打开电影的详情页面，获得数据"""
        import requests
        from bs4 import BeautifulSoup as bs
        from time import sleep
        for item in self.movie_list:
            # 获得单部电影的页面
            tmp = requests.get(item['url'])
            # 将页面转成BeautifulSoup对象
            tmp = bs(tmp.text, 'lxml')
            # 提取<div id='info'>的部分
            tmp = tmp.body.find('div',id='info')
            # 提取类型标签
            genre = tmp.find_all('span', property='v:genre')
            item['tags'] = [i.text for i in genre]
            # 提取国家,搜索<span>制片国家/地区:</span>的下个兄弟节点
            country = tmp.find('span', text='制片国家/地区:').next_sibling[1:]
            item['country'] = country
            # 提取第一个上映日期,搜索<span property='v:initialReleaseDate'></span>中的文本值
            release = tmp.find('span', property='v:initialReleaseDate').text
            item['release'] = release[:10]
            # 提取时长,搜索<span property='v:runtime'>标签中的content属性
            minutes = tmp.find('span', property='v:runtime').get('content')
            item['minutes'] = int(minutes)
            # 休眠1秒
            sleep(1)
    
    def save_db(self):
        """保存到mongodb数据库"""
        from pymongo import MongoClient
        conn = MongoClient(host=self.db['host'], port=self.db['port'])
        conn = conn.get_database(self.db['db'])
        conn = conn.get_collection(self.db['collection'])
        for item in self.movie_list:
            conn.insert_one(item)

if __name__ == '__main__':
    # 抓取400条记录
    for i in range(20):
        s = get_douban(i*20)
        s.get_movielist()
        s.get_oneinfo()
        s.save_db()
        print('get %d - %d ' %(i*20, (i+1)*20-1))
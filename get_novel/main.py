# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
conn = MongoClient(host='localhost', port=27017)
conn = conn.get_database('mydatabase')
conn = conn.get_collection('fiction')
save_path = '~/Documents/fictions/'
weburl = 'https://www.x23us.com/'


class fiction:
    def __init__(self, name=''):
        self.name = name
        self.author = ''
        self.url = ''
        self.weburl = 'https://www.x23us.com/'
        self.chapterNum = int(0)
        self.lastchapter = ''
        self.chapterList = []
    def search_db(self,name=''):
        """
            在数据库搜索小说
        """
        pass
    def read_db(self,name):
        """
            从数据库读取小说信息
        """
        pass
    def save_db(self):
        """
            保存抓取章节链接结果到数据库
        """
        pass
    def save_txt(self):
        """
            保存抓取的章节内容到txt文件
        """
        pass
    def get_url(self, name=''):
        """
            获得小说章节页面链接和作者信息
        """
        name = name if name else self.name
        if name == '':
            return(False, 'Please input fiction name!')
        # 在网站上查找小说
        url = f'https://www.x23us.com/modules/article/search.php?searchtype=keywords&searchkey={name}'
        url = requests.utils.quote(url, safe=':/?&=', encoding='gbk')
        tmp = requests.get(url)
        if tmp.url == url:
            flist = [
                {'name':i.find_all('td')[0].text
                , 'url':i.find_all('td')[0].a.get('href')
                , 'lastchapter':i.find_all('td')[1].text
                , 'author':i.find_all('td')[2].text}
                for i in bs(tmp.content, features='html.parser').body.find('table', class_='grid').find_all('tr')[1:]
            ]
            for i in flist: print('%d ind, name: %s, author: %s, lastchapter: %s' % (flist.index(i), i['name'], i['author'], i['lastchapter']))
            ind = int(input('Please select the index : '))
            self.name = flist[ind]['name']
            self.author = flist[ind]['author']
            tmp = requests.get(flist[ind]['url'])
            self.url = bs(tmp.content, features='html.parser').body.find('a', class_='read').get('href')
        else:
            fictInfo = bs(tmp.content, features='html.parser').body
            self.name = name
            self.author = fictInfo.find('table',id='at').tr.find_all('td')[1].text.strip()
            self.url = fictInfo.find('a', class_='read').get('href')
        return (True,f'Get fiction {self.name}')
    def get_catalog(self, url=''):
        """
            从目录页面抓取小说目录
        """
        url = url if url else self.url
        if url == '':
            return(False,'Please input chapter url')
        url = 'https://www.x23us.com/html/65/65443/'
        tmp = requests.get(url)
        cList = bs(tmp.content, features='html.parser').body.find('table', id='at').find_all('a')
        for i in cList:
            self.chapterList.append(chapter(chap_name=i.text, chap_url=f'{url}{i.get("href")}'))
        return(True, f'Get chapters: {len(cList)}')
    def get_chapter(self):
        """
            批量抓取小说章节
        """
        while self.chapterNum > 0:
            for i in self.chapterList:
                if i.fetch:
                    pass
                else:
                    if i.get_content():
                        self.chapterNum -= 1


class chapter(fiction):
    """
        章节子类
    """
    def __init__(self,chap_name, chap_url):
        self.chap_name = chap_name
        self.chap_url = chap_url
        self.fetch = False
        self.chap_content = ''
    def get_content(self):
        """
            抓取章节内容
        """
        try:
            tmp = requests.get(self.chap_url)
            if tmp.ok:
                content = bs(tmp.content, features='html.parser').body.find('dd', id='contents').text
                self.chap_content = '\n'.join(content.split())
                self.fetch = True
        except Exception as e:
            print(e)
        finally:
            return(self.fetch)


if __name__ == '__main__':
    t = fiction('剑与魔法与出租车')
    t.get_url()
    t.get_catalog()
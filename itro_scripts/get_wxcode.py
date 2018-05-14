# coding:utf-8
"""百度，按关键字抓取微信号"""

class wxcode(object):
    """
        通过百度搜索 微信+关键字 ，检查搜索结果中包含有微信号的，提取其中的微信号码
        keyword, 输入关键字
        pagenum, 检查的页数，默认为100页
    """
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"}
        self.result = set()
    def get_wxcode(self, keyword='纸尿裤', pagenum=int(101)):
        """
            抓取百度搜索结果中的微信号
        """
        keyword = '微信 %s' % keyword
        import requests
        import re
        import time
        from bs4 import BeautifulSoup as bs
        for pn in range(pagenum):
            api = 'https://www.baidu.com/s?wd=%s&pn=%d' % (keyword, pn*10)
            print(api)
            tmp = requests.get(api, headers=self.headers, timeout=3)
            tmp = bs(tmp.content, 'lxml')
            tmp = tmp.body.find('div', id='content_left')
            tmp = tmp.find_all('div', class_='c-abstract')
            for i in tmp:
                print(i.text)
                j = re.search('([微信账号公众咨询])([^a-zA-Z0-9]?)([a-zA-Z0-9][a-zA-Z0-9_-]{5,19})', i.text.replace(':',''))      # 匹配微信号，微信号可使用6-20个字母、数字、下划线或减号，必须以字母或数字开头
                if j :
                    if j.group(3):
                        self.result.add(j.group(3))
    def save_result(self):
        """
            保存结果到当前目录的result.txt文件
        """
        with open('result.txt', 'w', newline='\n') as writer:
            for i in self.result:
                writer.write(i + '\n')
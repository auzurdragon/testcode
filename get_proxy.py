#! coding:utf-8

class get_proxy(object):
    """
        抓取代理ip
        数据来源，西刺代理 : http://www.xicidaili.com/nn/
    """
    def __init__(self):
        self.url = 'http://www.xicidaili.com/nn/'
        self.check_url = 'http://ip.chinaz.com/'
        self.headers = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'},
        ]
        self.proxies = []
    def get_proxy(self, page=1):
        import requests, time
        from bs4 import BeautifulSoup as bs
        from random import choice
        url = self.url + str(page) if page > 1 else self.url
        request = requests.get(url, headers = choice(self.headers), timeout=3)
        time.sleep(3)
        result = bs(request.content, 'html5lib')
        result = result.body.div.find('table', id='ip_list')
        result = result.find_all('tr')
        result = result[1:]
        for log in result:
            tmp = log.find_all('td')
            iptype = tmp[5].text.lower()
            ip = '%s://%s:%s' % (iptype, tmp[1].text, tmp[2].text)
            ipf = {iptype:ip}
            if self.check_proxy(ipf):
                self.proxies.append(ipf)
                print('check success : %s' % ip)
            else:
                print('check failed : %s' % ip)
    def check_proxy(self, proxy):
        import requests
        try:
            request = requests.get(self.check_url, proxies=proxy, timeout=1)
            if request.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False
        
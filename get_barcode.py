#! coding:utf-8
import requests, aircv, cv2, sys
from selenium import webdriver
from time import sleep, strftime, localtime, time
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
class barcode(object):
    """
    条形码信息抓取
    数据来源 http://search.anccnet.com
    依赖phantomjs,需要预先安装，并在get_cookie()中指定安装目录
    依赖opencv库, pip install opencv-python
    注意事项：
    1. 同个IP有单位时间抓取次数的限制，每次抓取sleep(2) & 每20次抓取 sleep(80) 会比较安全。
    2. bs要使用"html5lib"解析器，使用'lxml'解析会出现数据丢失的问题
    3. 首次抓取前用网页登录页面通过人机验证，记录cookie，实测每个cookie连续使用可持续一个白天。
    """
    def __init__(self):
        self.api = 'http://search.anccnet.com/searchResult2.aspx'
        self.header = {
                'Host': 'search.anccnet.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'http://search.anccnet.com/searchResult2.aspx?keyword=6901028200035',
                'Cookie': 'ASP.NET_SessionId=3awbpe3r2a5nlz45j5cwlh45',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
        }
        self.db = {
            'host':'localhost',
            'port':28010,
            'db':'web_db',
            'collection':'barcode'
        }
    def check(self, code):
        """ 计算标准条形码的校验码，返回拼接后的条形码
            code, 标准码不带校验位，共12位数, 标准码的前12位数倒序
            校验码的计算步骤如下：
            1. 将13位标准码的前12位倒序排列
            2. 从代码位置序号2开始，所有偶数位的数字代码求和。
            3. 将步骤a的和乘以3。 
            4. 从代码位置序号3开始，所有奇数位的数字代码求和。
            5. 将步骤b与步骤c的结果相加。
            6. 用大于或等于步骤d所得结果且为10最小整数倍的数减去步骤d所得结果，其差即为所求校验码的值。
        """
        clist = [int(i) for i in str(code)]
        clist.reverse()
        t = (sum(clist[1::2]) + sum(clist[0::2])*3) % 10
        c = 0 if t == 0 else 10 - t
        code = code * 10 + c
        return code
    def get_cookie_by_input(self,cookie):
        """
            输入获得cookie
        """
        self.header['Cookie'] = cookie
        result = {
            'result':True,
            'cookie':cookie
        }
        msg = 'get cookie : %s' % cookie
        self.print_log(msg=msg, type='log')
        return result
    def get_cookie_by_phantomjs(self):
        """
            获得cookie，需要selenium和phantomjs, 在建立webdriver时需要指定phantomjs的安装路径
        """
        result = {'result':False}
        params = webdriver.common.desired_capabilities.DesiredCapabilities.PHANTOMJS.copy()
        params['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0')
        url = 'http://search.anccnet.com/searchResult2.aspx'
        # windows环境指定目录driver = webdriver.PhantomJS(executable_path='phantomjs.exe', desired_capabilities=params)
        driver = webdriver.PhantomJS(executable_path='phantomjs', desired_capabilities=params) # centos环境
        driver.set_window_size(382,415)
        driver.get(url)
        sleep(10)
        if driver.title == '401 - 未授权: 由于凭据无效，访问被拒绝。':
            print (driver.title)
            sys.exit()
        iframe = driver.find_element_by_id('captcha_widget')
        driver.switch_to.frame(iframe)
        btn = driver.find_element_by_class_name('captcha-widget-event')
        btn.click()
        sleep(5)
        driver.switch_to.default_content()
        # 获得验证码图片所在iframe, iframe.size 中保存框架的height, width
        iframe = driver.find_element_by_id('captcha_frame')
        driver.switch_to.frame(iframe)
        # 从iframe中获得验证图片，并转换成aircv对象
        img = driver.find_element_by_id('lc-image-panel').find_element_by_class_name('captcha-list')
        imsrc = self.get_imsrc(img)
        # 从iframe中获得需要验证的点击步骤，可能会需要按顺序点击星形,圆点,方块
        checklist = driver.find_element_by_css_selector('span#lc-captcha-word i').text
        checklist = checklist.split(',')
        for i in checklist:
            imobj = self.get_shape(i)
            # 在验证图片中查找验证点
            pos = aircv.find_template(im_source = imsrc, im_search = imobj, threshold = 0.7)['result']
            # 点击验证点
            webdriver.ActionChains(driver).move_to_element_with_offset(iframe, pos[0], pos[1]).click().perform()
            sleep(1)
        sleep(5)
        # 获得cookie
        tmp = driver.get_cookies()
        driver.quit()
        if tmp:
            cookie = '%s=%s' % (tmp[0]['name'], tmp[0]['value'])
            print('get cookie : %s ' % cookie)
            self.header['Cookie'] = cookie
            result['result'] = True
            result['cookie'] = cookie
            return result
        else:
            print('get cookie failed! check : %s' % ','.join(checklist))
            return result
    def get_shape(self, shapename, radius=5):
        """
            绘制验证图形形状，包括'方块','圆点','星形'
            返回aricv图形对象
        """
        import math
        if shapename == '星形':
            # imobj = aircv.imread('imstar.png')
            angle = math.pi/10
            r1 = 9    # 长轴长度
            r2 = r1 * math.sin(angle) / math.cos(angle*2) # 短轴长度
            anglelist = []
            for i in range(5):
                anglelist.append(angle*4*i - angle)
                anglelist.append(angle*4*i + angle*2 - angle)
            coorlist = []
            for i in range(10):
                r = r1 if i % 2 == 0 else r2
                x = r * math.cos(anglelist[i])
                y = r * math.sin(anglelist[i])
                coorlist.append([x+r1, y+r1])
            imobj = aircv.np.zeros((r1*2, r1*2, 3), dtype='uint8')
            pts = aircv.np.array([coorlist], dtype=aircv.np.int32)
            cv2.fillPoly(img = imobj, pts=pts, color=(255,255,255))
        elif shapename == '圆点':
            r = 6
            imobj = aircv.np.zeros((r*2+2, r*2+2, 3), dtype='uint8')
            center = (r+1,r+1)
            # 在画板canvas上画实心圆
            # aircv.cv2.circle(img = imobj, center = (13,13), radius = 16, color=(240,140,240), thickness=-1)
            aircv.cv2.circle(img = imobj, center = center, radius = r, color = (255,255,255), thickness = -1)
        elif shapename == '方块':
            # 绘制方块形式
            r = 5
            imobj = aircv.np.zeros((r*2, r*2, 3), dtype='uint8')
            aircv.cv2.rectangle(imobj, pt1=(1,1), pt2=(r*2-1,r*2-1), color=(255,255,255), thickness=-1)
        else:
            return False
        return imobj
    def get_imsrc(self, iframe):
        """
            从网页上的验证图片转换成aircv图片格式
            iframe, 输入的待转换网页对象，从对象中提取验证码图形，并以aircv对象返回
        """
        imsrc = iframe.screenshot_as_png
        imsrc = aircv.np.fromstring(imsrc, dtype=aircv.np.uint8)    # aircv的图形对象为np数组格式
        imsrc = aircv.cv2.imdecode(imsrc, 1)
        return imsrc
    def get_cookie_by_firefox(self):
        """
            使用firefox -headless 模式获得cookie
        """
        result = {'result':False}   # 返回结果
        url = 'http://search.anccnet.com/searchResult2.aspx'
        try:
            options = webdriver.firefox.options.Options()
            options.add_argument('-headless')
            driver = webdriver.Firefox(firefox_options=options)
            driver.implicitly_wait(50)
            driver.get(url)
            # sleep(10)
            # iframe = driver.find_element_by_id('captcha_widget')
            iframe = driver.find_element_by_tag_name('iframe')
            iframe.click()
            # sleep(5)
            iframe = driver.find_element_by_id('captcha_frame')
            driver.switch_to.frame(iframe)
            img = driver.find_element_by_id('lc-image-panel')
            checklist = driver.find_element_by_css_selector('span#lc-captcha-word i').text.split(',')
            print(checklist)
            imsrc = self.get_imsrc(img)
            for i in checklist:
                imobj = self.get_shape(i)
                tmp = aircv.find_template(im_source = imsrc, im_search = imobj, threshold = 0.55)
                if tmp:
                    pos = tmp['result']
                else:
                    self.print_log(msg='find_template %s failed' % i, type='error')
                    sys.exit()
                webdriver.ActionChains(driver).move_to_element_with_offset(img, pos[0], pos[1]).perform()
                webdriver.ActionChains(driver).click().perform()
                sleep(5)
            cookie = driver.get_cookies()
            print(cookie)
            cookie = '%s=%s' % (cookie[0]['name'], cookie[0]['value'])
            self.header['Cookie'] = cookie
            result['result'] = True
            result['cookie'] = cookie
            self.print_log(msg='get cookie %s' % cookie, type='log')
        except Exception as E:
            self.print_log(msg=E, type='error')
        finally:
            driver.quit()
            return result
    def save_code(self, docu, update=False):
        """ 保存单条查询结果到数据库 """
        try:
            conn = MongoClient(host=self.db['host'], port=self.db['port'])
            conn = conn.get_database(name=self.db['db'])
            conn = conn.get_collection(name=self.db['collection'])
            if update:
                conn.update_one(
                    {'barcode':docu['barcode']},
                    {'$set':{
                        'status':docu['status'],
                        'img':docu['img'],
                        'url':docu['url'],
                        'name':docu['name'],
                        'size':docu['size'],
                        'brief':docu['brief'],
                        'brand':docu['brand'],
                        'supplier':docu['supplier'],}
                    },
                    upsert=True)
            else:
                conn.insert_one(docu)
            return True
        except Exception as E:
            self.print_log(msg=E,type='error')
            return False
    def scan_code(self, codeNoCheck):
        """ 
            通过api查询条形码信息
            UserWarning(0,'msg') cookie无效，提示需要人机验证。
            UserWarning(1,'msg)  requests请求失败，建议等待90秒后再试。
        """
        result = {
            'barcode':codeNoCheck,
            'status':False,
            'searchinfo':'',
            'img':'',
            'url':'',
            'name':'',
            'size':'',
            'brief':'',
            'brand':'',
            'supplier':'',
        }
        url = '%s%d' % (self.api, codeNoCheck)
        self.header.update({'Referer':url})
        try:
            t = requests.get(url, headers=self.header, timeout=5)
        except Exception as e:
            raise UserWarning(2, 'requests error : %s' % e)
        if t.status_code != 200:
            raise UserWarning(1, 'requests.status_code error : %d' % t.status_code)
        t = bs(t.content, 'html5lib')
        t = t.body.find('div', class_='mainly')
        searchinfo = t.find('div', class_='main').find('h2').text
        searchinfo = searchinfo.split('，')[-1].replace('\n', '').replace(' ', '')
        result['searchinfo'] = searchinfo
        if searchinfo[:13] == '请先点击右边的人机识别验证':
            raise UserWarning(0, 'cookie error : %s' % self.header['Cookie'])
        elif searchinfo in ['但该商品已下市。', '但编码信息未按规定通报。', '暂无相关信息。']:
            pass
        else:
            t = t.find("ol", id="results")
            img = t.find("p", class_="p-img")
            supplier = t.find("dl", class_="p-supplier").find_all("dd")
            info = t.find("dl", class_='p-info').find_all("dd")
            result = dict(result, **{
                'status':True,
                'img':img.a.img.get('src'),
                'url':info[0].a.get('href'),
                'name':info[3].text,
                'size':info[4].text,
                'brief':info[5].text,
                'brand':supplier[0].text,
                'supplier':supplier[1].text.replace('\n', '').replace(' ', ''),                
            })
        return result
    def scan_code_by_factory(self,factory,start=0):
        """
            按厂商代码批量查询
            factory , 厂商识别码
            start , 从此开始扫描
            连续500次扫描无有效条码，则退出
        """
        if factory in range(6900000, 69200000):
            code_start = factory * 100000 + start
            code_end = (factory + 1) * 100000
        elif factory in range(69200000, 69700000):
            code_start = factory * 10000 + start
            code_end = (factory + 1) * 10000
        elif factory in range(697000000,698000000): 
            code_start = factory * 1000 + start
            code_end = (factory +1) * 1000
        count = 0
        success = 0
        S = 0
        for i in range(code_start, code_end):
            code = self.check(i)
            msg = '%s , count : %d, success : %d , code : %d , ' % (strftime('%Y-%m-%d %H:%M:%S', localtime(time())), count, success, code)
            count += 1
            S += 1
            sleep(2)
            if count % 20 == 0:
                sleep(90)
            while True:
                try:
                    tmp = self.scan_code(code)
                    success += 1
                    if tmp['status']:
                        S = 0
                    msg = msg + ' status : %s , info : %s' % (tmp['status'], tmp['searchinfo'])
                    self.save_code(tmp)
                    break
                except UserWarning as e:
                    print('%d, %d, %d, error : %s ' % (count,success, code, e.args[1]))
                    if e.args[0] == 0:
                        self.print_log(msg = 'cookie error %s ' % self.header['Cookie'], type='error')
                        sys.exit()
                        # cookie = self.get_cookie_by_firefox()
                        # if cookie['result']:
                        #     pass
                        # else:
                        #     sys.exit()
                    elif e.args[0] == 1:
                        sleep(30)
                    else:
                        sleep(30)
                except Exception as e:
                    msg = msg + ' error : %s' % e
                    sleep(30)
                finally:
                    print(msg)
            if S >= 100:
                msg = msg + ' error : %s' % '连续100次扫描无结果，结束该次厂商扫描。'
                print(msg)
                break
        self.update_factory(factory, success)
        return success
    def update_factory(self,factory,count):
        """
            更新完成扫描的厂商代码状态，标记已完成
        """
        try:
            conn = MongoClient('localhost', 28010)
            conn = conn.get_database('web_db')
            conn = conn.get_collection('factory')
            conn.update_one({'factory':factory,},{'$set':{'scan':True, 'count':count}})
            return True
        except Exception as E:
            print(E)
            return False
    def save_factory(self,docu,update=False):
        """
            保存厂商代码扫描结果
            update默认False,插入新数据。True, 则update
        """
        conn = MongoClient('localhost', 28010)
        conn = conn.get_database('web_db')
        conn = conn.get_collection('factory')
        if update:
            conn.update_one(
                {'factory':docu['factory']},
                {'$set':{
                    'status':docu['status'],
                    'factory':docu['factory'],
                    'name':docu['name'],
                    'url':docu['url'],
                    'log':docu['log'],
                }},
                upsert=True
            )
            return True
        else:
            conn.insert_one(docu)
            return True
    def scan_factory(self,factory):
        """
            扫描厂商代码
            http://www.ancc.org.cn/Service/queryTools/internal.aspx
        """
        result = {
            'status':False,
            'factory':factory,
            'name':'',
            'url':'',
            'log':'',
        }
        url  = 'http://www.ancc.org.cn/Service/queryTools/internal.aspx'
        data = {
            '__EVENTARGUMENT':'',
            '__EVENTTARGET':'',
            '__EVENTVALIDATION':'/wEdAAru5ynIz9OFk4jEIDV2KP0ELTHaOnjjN9ezrJXLmfOeAMgC2mH1Ur6wyTd3BUNIcyWiyIEyfuyww71BI3NcUgXGyUF+xupvZq09IH598AhnSsYP3Gb/SPKpkHZ0LjPy1J5nadqDCyJT2jQKAtVMOsYR3YME9d0zRJHGgvbQorueN+KbMYHUXCfGFbDMtCY1pH2f54hU+oqvsO8OrtUpxY5D23bSVrv0AtRG5rHYhT9jsmd6TcyWGiN/WLsFSBgHsaU=',
            '__VIEWSTATE':'/wEPDwULLTE5NTYxNDQyMTkPZBYCAgEPZBYCAhMPFgIeB1Zpc2libGVnFgYCAQ8PFgIeBFRleHQFCTY5NzA2NjI4OGRkAgMPDxYEHwEFHuayoeacieespuWQiOadoeS7tueahOiusOW9le+8gR8AaGRkAgUPFgIfAGcWAgIDDw8WBB4LUmVjb3JkY291bnQCAR4QQ3VycmVudFBhZ2VJbmRleAJDZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgUFElJhZGlvSXRlbU93bmVyc2hpcAUNUmFkaW9JdGVtSW5mbwUGUmFkaW8xBQZSYWRpbzIFBlJhZGlvM+i5eheIMq8iF86ET5PJtItE3p122R9hb3754WHQyc/N',
            '__VIEWSTATEGENERATOR':'26301414',
            'btn_query':'查询+',
            'query-condition':'RadioItemOwnership',
            'query-supplier-condition':'Radio1',
            'Top$h_keyword':'',
            'txtcode':0,
        }
        data['txtcode'] = factory
        t = requests.post(url, data)
        t = bs(t.content, 'lxml')
        t = t.find('div', id='searchResult')
        t = t.find('div', class_='section-body')
        t = t.find('table')
        if t:
            r = t.tbody.find_all('td')
            result = dict(result, **{
                'name':r[1].text.replace('\r','').replace('\n','').replace(' ',''),
                'status':r[2].text.replace('\r','').replace('\n','').replace(' ',''),
                'url':r[3].a.get('href'),
                'log':r[4].a.get('href')
            })
            return result
        else:
            return False
    def print_log(self, msg, type='error'):
        """
            打印日志记录
            type, 日志类型
            msg, 日志内容
        """
        S = '%s | %s | %s' % (strftime('%Y-%m-%d %H:%M:%S', localtime(time())), type, msg)
        print(S)
    def get_keyword(self, content):
        """
            从文本中提取关键词
        """
        from jieba import analyse
        tag = analyse.extract_tags(content)

if __name__ == '__main__':
    start = int(sys.argv[1])
    code_start = int(sys.argv[2])
    s = barcode()
    # cookie = s.get_cookie_by_input(sys.argv[3])
    cookie = s.get_cookie_by_input(sys.argv[3])
    if cookie['result']:
        s.print_log(msg = 'cookie : %s' % s.header['Cookie'], type='log')
    else:
        s.print_log(msg='get_cookie failed', type='error')
        sys.exit()
    # 获得有效的factory， 从start 开始，每次取10个
    conn = MongoClient('localhost', 28010)
    conn = conn.get_database('web_db')
    conn = conn.get_collection('factory')
    # f = list(conn.find({'status':'有效', 'factory':{'$gte':start}, 'scan':False}, {'_id':0, 'factory':1}).sort('factory').limit(100))
    # if not f:
    #     print('no factory code')
    # flist = [i['factory'] for i in f]
    # 搜索厂商名称中含有'婴'的status有效 scan False的factory
    flist = [697010464, 697010598, 697011022, 697011101, 697011245, 697011385, 697011803, 697011827, 697012296, 697000977, 697001992, 697002589, 697003304, 697004637, 697004976, 697005238, 697005416, 697005532, 697006039, 697006115, 697006138, 697006343, 697006872, 697007105, 697007488, 697007501, 697007665, 697007750, 697007915, 697007917, 697007999, 697008161, 697008435, 697008595, 697008777, 697008911, 697009016, 697009323, 697009643, 697009792, 697009910, 697009949, 697013356, 697013362, 697013407, 697013524, 697013599, 697013878, 697013961, 697014013, 697014267, 697014397, 697014474, 697014589, 697014598, 697014957, 697016086, 697016282, 697016287, 697017155, 697017618, 697017893, 697017936, 697018000, 697018246, 697018287, 697018307, 697018368, 697018642, 697018651, 697018868, 697019504, 697020107, 697020172, 697020474, 697020508, 697020535, 697020971, 697021214, 697021253, 697021646, 697021648, 697021653, 697021664, 697021676, 697022502, 697022915, 697023034, 697023240, 697023246, 697023433, 697023469, 697023502, 697023524, 697023673, 697023925, 697024154, 697024199, 697024561, 697024784, 697024791, 697025179, 697025241,
697025603, 697025831, 697025936, 697026096, 697026397, 697026417, 697026955, 697027018, 697027027, 697027414, 697027825, 697027872, 697028267, 697028645, 697028662, 697028665, 697028810, 697029114, 697029184, 697029223, 697030100, 697030130, 697030289, 697030433, 697030868, 697030950, 697030958, 697031352, 697031353, 697031676, 697031986, 697032075, 697032121, 697032317, 697032819, 697033013, 697033124, 697033416, 697033444, 697033516, 697033621, 697033649, 697033658, 697033664, 697033978, 697034048, 697034408, 697034451, 697034943, 697035057, 697035177, 697035222, 697035560, 697035590, 697035670, 697035677, 697035818, 697035829, 697036669, 697036747, 697036777, 697036800, 697036836, 697037030, 697037092, 697037809, 697038023, 697038028, 697038253, 697038296, 697038882, 697038928, 697038959, 697039410, 697039666, 697040033, 697040151, 697040546, 697040965, 697040984, 697041055, 697041212, 697041493, 697041696, 697042130, 697042970, 697042974, 697043049, 697043149, 697043242, 697043495, 697043547, 697043622, 697043628, 697043836, 697044170, 697044227, 697044317, 697045073, 697045211, 697045238, 697045343, 697045405, 697045462, 697045664, 697046093, 697046128, 697046133, 697046142, 697046286, 697046402, 697046470, 697047481, 697047495, 697047720, 697047818, 697047819, 697047820, 697048236, 697048268, 697048522, 697048697, 697048854, 697048857, 697048905, 697048906,
697048923, 697049005, 697049233, 697049567, 697049587, 697049650, 697050286, 697050872, 697050924, 697051520, 697051603, 697051615, 697051617, 697051999, 697052114, 697052120, 697052489, 697052809, 697052933, 697053037, 697053507, 697053535, 697053739, 697053816, 697053940, 697054013, 697054240, 697054341, 697054483, 697054883, 697054889, 697054914, 697054936, 697055338, 697055367, 697055886, 697055912, 697055915, 697056220, 697056277, 697056313, 697056483, 697056567, 697056572, 697056998, 697057048, 697057110, 697057120, 697057609, 697057887, 697057905, 697058459, 697058641, 697058774, 697058903, 697059086, 697059246, 697059284, 697059457, 697060184, 697060582, 697060687, 697060825, 697061222, 697061230, 697061233, 697061237, 697061744, 697061789, 697061851, 697062048, 697062691, 697062781, 697063190, 697063284, 697063575, 697063769, 697063771, 697064041, 697064146, 697064747, 697064748, 697065151, 697065859, 697066213, 697066485, 697066645, 697066812, 697066914, 697066916, 697067240, 697067587, 697067747, 697067784, 697067789, 697068126, 697068249, 697068566, 697068606, 697068771, 697068815, 697069024, 697069033, 697069166, 697069875, 697069968, 697070170, 697070181, 697070731, 697070734, 697070776, 697070825, 697070928, 697071000, 697071140, 697071153, 697071198, 697071226, 697071314, 697071485, 697071507, 697071531, 697071708, 697072109, 697072602, 697072774,
697073096, 697073268, 697073351, 697073688, 697073845, 697073921, 697074406, 697074437, 697074472, 697074651, 697074694, 697074713, 697075135, 697075310, 697075502, 697075811, 697075900, 697075905, 697076115, 697076316, 697076340, 697076889, 697077016, 697077247, 697077338, 697077468, 697077791, 697077854, 697077991, 697078337, 697078480, 697078906, 697079475, 697079573, 697080084, 697080208, 697080267, 697080520, 697080897, 697081444, 697081519, 697081759, 697081933, 697082049, 697082185, 697082300, 697082573, 697082701, 697082745, 697083641, 697084193, 697084349, 697084368, 697084440, 697085000, 697085198, 697085330, 697085351, 697085404, 697086239, 697086432, 697086476, 697086500, 697086549, 697087497, 697087660, 697087896, 697087942, 697088022, 697088334, 697088510, 697088607, 697088682, 697088692, 697088832, 697088855, 697089128, 697089273, 697089325, 697089487, 697089542, 697089615, 697089680, 697089719, 697089797, 697089909, 697090074, 697090146, 697090411, 697090461, 697090602, 697091022, 697091030, 697091062, 697091619, 697091675, 697091680, 697091713, 697091777, 697091977, 697092648, 697093220, 697093366, 697093489, 697093546, 697093750, 697093896, 697093909, 697093923, 697093980, 697094009, 697094320, 697094330, 697094683, 697094774, 697094913, 697095111, 697095122, 697095125, 697095279, 697095322, 697095549, 697095670, 697096101, 697096323, 697096419,
697096474, 697096597, 697096716, 697096740, 697097178, 697097262, 697097849, 697097880, 697097885, 697098034, 697098245, 697098364, 697098801, 697099147, 697099285, 697099413, 697099792, 697099870, 697099927, 697100102, 697100263, 697100453, 697100575, 697100586, 697100895, 697101076, 697101785, 697101832, 697101842, 697102284, 697102364, 697102512, 697102591, 697102702, 697102832, 697102997, 697103017, 697103117, 697103535, 697103741, 697103849, 697103854, 697103885, 697104020, 697104321, 697104690, 697104698, 697104737, 697104951, 697105209, 697105250, 697105343, 697105466, 697105688, 697105715, 697105731, 697105750, 697106006, 697106483, 697106524, 697106743, 697107193, 697107200, 697107752, 697107937, 697108024, 697108289, 697108346, 697108665, 697108726, 697108838, 697109164, 697109487, 697109621, 697109632, 697109643, 697109694, 697109806, 697109984, 697110081, 697110426, 697110622, 697110792, 697110873, 697110996, 697111432, 697111587, 697111633, 697111730, 697112106, 697112209, 697112564, 697112619, 697112717, 697112795, 697112820, 697113195, 697113677, 697114082, 697114267, 697114498, 697114544, 697114778, 697114789, 697114982, 697115288, 697115387, 697115944, 697116043, 697116084, 697116161, 697116227, 697116258, 697116355, 697116432, 697116718, 697116925, 697117358, 697117521, 697117539, 697117998, 697118480, 697118549, 697118665, 697118736, 697119615,
697120043, 697120695, 697120840, 697120850, 697121129, 697121629, 697122052, 697122135, 697122230, 697122470, 697122501, 697123306, 697123310, 697123365, 697123381, 697123839, 697123875, 697124310, 697124611, 697124628, 697124681, 697125051, 697125167, 697125817, 697125834, 697125880, 697126278, 697126332, 697126478, 697126807, 697126973, 697127125, 697127174, 697127453, 697127522, 697127523, 697127529, 697127807, 697127916, 697128194, 697128195, 697128260, 697128363, 697128470, 697128736, 697128737, 697128834, 697128946, 697128975, 697128978, 697129201, 697129208, 697129257, 697129714, 697129737, 697131187, 697131431, 697131570, 697131736, 697131826, 697132301, 697132350, 697132351, 697132480, 697132691, 697132844, 697132876, 697133060, 697133164, 697134133, 697134333, 697134369, 697134501, 697134549, 697135239, 697135301, 697135369, 697136088, 697136482, 697136722, 697136754, 697136759, 697136885, 697137191, 697137370, 697137526, 697137577, 697137802, 697138181, 697138220, 697138326, 697138644, 697138967, 697139217, 697139337, 697139926, 697140130, 697140131, 697140426, 697140589, 697140712, 697140755, 697140893, 697142211, 697142601, 697142970, 697143291, 697143487, 697143525, 697143680, 697143698, 697143964, 697143965, 697144384, 697144515, 697144871, 697144908, 697145203, 697145222, 697145236, 697145243, 697145583, 697145695, 697145701, 697145914, 697145981,
697146002, 697146082, 697146229, 697146536, 697146537, 697146694, 697146698, 697146897, 697146934, 697147314, 697147572, 697148068, 697148392, 697148440, 697148636, 697148663, 697148799, 697148806, 697149266, 697149404, 697149447, 697149472, 697149632, 697149692, 697149730, 697149833, 697149862, 697149866, 697150131, 697150653, 697150800, 697150822, 697150899, 697150942, 697151012, 697151188, 697151429, 697151765, 697152406, 697152589, 697152773, 697153146, 697153175, 697153336, 697153424, 697153595, 697153633, 697153799, 697153898, 697154184, 697154424, 697154524, 697154814, 697154845, 697155323, 697155496, 697155695, 69500207, 69500428, 69500783, 69501392, 69501490, 69501661, 69501667, 69502290, 69502775, 69502833, 69504253, 69504309, 69505204, 69505313, 69505660, 69505666, 69506262, 69506841, 69507549, 69507852, 69509216, 69509240, 69509796, 69510545, 69510805, 69511163, 69511728, 69512722, 69512772, 69512858, 69513077, 69513610, 69514069, 69514205, 69514474, 69514757, 69515099, 69515718, 69517067, 69517116, 69517920, 69518154, 69518462, 69518579, 69518938, 69520409, 69521020, 69521242, 69521318, 69522168, 69523167, 69523419, 69524574, 69524621, 69525384, 69525430, 69525621, 69525865, 69527037, 69527503, 69527538, 69528089, 69528705, 69529038, 69530080, 69530200, 69531015, 69531245, 69531332, 69531438, 69532048, 69533258, 69533520, 69533585, 69533756, 69534199, 69534523, 69535029, 69535393, 69535745, 69536247, 69536588, 69537114, 69537616, 69538265, 69538331, 69538874, 69539145, 69539428, 69539886, 69539908, 69540123, 69541662, 69541965, 69542568, 69543267, 69544024, 69544866, 69545024, 69545194, 69545282, 69545533, 69545622, 69546258, 69547301, 69547567, 69547681, 69547684, 69547702, 69547977, 69548642, 69548996, 69549718, 69549724, 69549778, 69550044, 69551614, 69551825, 69552036, 69552113, 69552563, 69553454, 69553660, 69554336, 69554362, 69554882, 69555028, 69555350, 69555467, 69556038, 69556331, 69556802, 69556956, 69557028, 69557040, 69557708, 69558272, 69558303, 69558573, 69558723, 69558858, 69558896, 69559150, 69559194, 69559326, 69559724, 69559849, 69560490, 69560496, 69560800, 69561064, 69561138, 69561569, 69561846, 69562145, 69564355, 69564534, 69564893, 69565075, 69565454, 69565831, 69565934, 69566453, 69567028, 69567171, 69567321, 69567640, 69567810, 69567969, 69567986, 69568233, 69569045, 69569222, 69569274, 69569328, 69569728, 69569800, 69570007, 69571165, 69571427, 69571479, 69571950, 69572241, 69572738, 69573302, 69573839, 69574298, 69574876, 69575833, 69576101, 69576607, 69576669, 69577091, 69577573, 69577697, 69577792, 69577841, 69579177, 69579178, 69579436, 69579731, 69579881, 69580408, 69580667, 69582270, 69582650, 69582735, 69582839, 69582983, 69583193, 69583460, 69583515, 69583560, 69584276, 69584339, 69584380, 69584456, 69584800, 69584965, 69584969, 69584976, 69585130, 69585986, 69585999, 69586025, 69586836, 69586924, 69587937, 69588112, 69588646, 69589027, 69589125, 69589635, 69589649, 69589818, 69590121, 69590339, 69590464, 69590470, 69590604, 69590638, 69591148, 69591192, 69591831, 69593037, 69593211, 69593336, 69593662, 69593762, 69594008, 69594223, 69594238, 69594763, 69595023, 69596425, 69596894, 69597212, 69597384, 69597716, 69598386, 69598500, 69598873, 69599491, 6901066, 6901112, 6901458, 6902390, 6902469, 6904591, 6908588, 6913475, 6919530, 69200250, 69200277, 69200351, 69200706, 69200822, 69201062, 69201980, 69202073, 69202100, 69202482, 69203726, 69203753, 69204353, 69204846, 69204988, 69205016, 69205315, 69205536, 69206297,
69207557, 69208253, 69208314, 69208536, 69209633, 69209720, 69210082, 69211235, 69211286, 69211993, 69212427, 69212473, 69212486, 69212535, 69213102, 69213325, 69213887, 69213995, 69214329, 69214620, 69214753, 69214826, 69214835, 69215139, 69216376, 69216829, 69216962, 69217081, 69217381, 69217510, 69217955, 69218051, 69218114, 69218404, 69218808, 69219714, 69219820, 69220040, 69220082, 69220198, 69220530, 69220688, 69222683, 69223868, 69223924, 69225149, 69226588, 69227359, 69228103, 69228825, 69229025, 69229076, 69229152, 69229698, 69230074, 69230760, 69231496, 69232451, 69232984, 69233175, 69233519, 69233747, 69234508,
69235349, 69235628, 69235746, 69236008, 69236088, 69236166, 69236186, 69236263, 69236965, 69237189, 69237628, 69237701, 69237841, 69238096, 69238661, 69239303, 69239777, 69240700, 69241422, 69241525, 69243235, 69243677, 69244003, 69244164, 69244998, 69245150, 69246014, 69246021, 69246041, 69246282, 69246492, 69248714, 69249173, 69249514, 69249537, 69249648, 69250249, 69250284, 69250772, 69251255, 69251503, 69251547, 69254243, 69254308, 69254626, 69254753, 69255217, 69255852, 69255991, 69256094, 69256509, 69256663, 69256843, 69257764, 69257838, 69257933, 69258268, 69258638, 69258675, 69259571, 69260133, 69260910, 69261045,
69261281, 69261292, 69261559, 69261567, 69261708, 69261974, 69262196, 69263139, 69264394, 69264576, 69264607, 69265217, 69265995, 69266209, 69266349, 69266424, 69266666, 69267265, 69267324, 69267392, 69268227, 69268268, 69268713, 69268973, 69269107, 69269636, 69269778, 69270487, 69271180, 69272261, 69273792, 69274146, 69274352, 69275500, 69275956, 69276309, 69276615, 69276636, 69276693, 69276955, 69277187, 69277420, 69277634, 69277650, 69278259, 69278911, 69279134, 69279472, 69279784, 69279835, 69280425, 69281089, 69281735, 69281867, 69283325, 69283542, 69283664, 69283969, 69284371, 69284487, 69284705, 69284734, 69285301,
69285408, 69285689, 69285899, 69285946, 69285958, 69286373, 69286767, 69287344, 69287468, 69287522, 69288062, 69288104, 69288589, 69289080, 69289116, 69289534, 69289896, 69289954, 69301422, 69301423, 69301513, 69301975, 69302577, 69302797, 69303295, 69303382, 69303705, 69303761, 69303961, 69304687, 69304977, 69306938, 69307006, 69307530, 69307839, 69307843, 69307976, 69307980, 69307990, 69308367, 69308698, 69309323, 69309557, 69309715, 69309874, 69309899, 69310432, 69310509, 69310894, 69311447, 69311765, 69311837, 69311939, 69312021, 69312277, 69312330, 69312419, 69312606, 69312678, 69313126, 69313479, 69314485, 69314616,
69314943, 69315782, 69315891, 69315944, 69319039, 69319056, 69319649, 69319717, 69319746, 69319750, 69319979, 69320071, 69320334, 69320625, 69320706, 69321961, 69323040, 69323229, 69323272, 69323491, 69323922, 69325121, 69326047, 69326538, 69326574, 69327150, 69327395, 69327773, 69327821, 69328699, 69328870, 69329652, 69329825, 69330445, 69330628, 69330780, 69330943, 69331353, 69332041, 69333159, 69335224, 69335326, 69336320, 69336518, 69336880, 69337506, 69337804, 69338143, 69338331, 69338580, 69339310, 69339398, 69339596, 69340424, 69340851, 69341426, 69341504, 69341982, 69342272, 69342638, 69342875, 69343535, 69343589,
69344119, 69344684, 69345205, 69345228, 69345693, 69345714, 69345762, 69347903, 69348199, 69348499, 69348691, 69349312, 69349543, 69350896, 69351990, 69352425, 69352618, 69353196, 69353516, 69354069, 69354548, 69354721, 69355114, 69355833, 69356120, 69356458, 69357098, 69357526, 69358489, 69358723, 69358772, 69358839, 69359407, 69360971, 69361183, 69361288, 69361395, 69361526, 69362272, 69362702, 69363462, 69363515, 69363646, 69363717, 69363750, 69363753, 69363928, 69364266, 69364341, 69364534, 69364960, 69364978, 69365013, 69365330, 69367464, 69367512, 69367928, 69369575, 69369826, 69370348, 69371245, 69372669, 69373648,
69373750, 69373850, 69374343, 69374642, 69374824, 69374974, 69375548, 69375549, 69376161, 69376251, 69376680, 69377848, 69377861, 69378133, 69378739, 69379894, 69380331, 69381122, 69381235, 69383505, 69384387, 69384402, 69384646, 69385441, 69386022, 69386543, 69386793, 69387708, 69387893, 69388002, 69390625, 69390946, 69390965, 69391201, 69391505, 69392325, 69392456, 69393100, 69393708, 69394192, 69394553, 69394647, 69394898, 69395496, 69397165, 69397624, 69398080, 69399442, 69399858, 69399957, 69400615, 69400666, 69400910, 69401599, 69402248, 69402351, 69402430, 69402692, 69403097, 69405120, 69405512, 69405762, 69406579,
69406689, 69407796, 69407831, 69408142, 69409452, 69409462, 69409970, 69410064, 69410960, 69411832, 69411908, 69419432, 69419940, 69421280, 69423477, 69423762, 69425489, 69426022, 69432164, 69433331, 69436787, 69438781, 69439274, 69441984, 69442299, 69442938, 69444705, 69444712, 69445129, 69445800, 69446191, 69446473, 69446772, 69447987, 69448739, 69454205, 69454493, 69457682, 69458944, 69461682, 69465119, 69466380, 69466485, 69466924, 69467675, 69469969, 69470497, 69471294, 69471775, 69473999, 69474458, 69476432, 69477069, 69477208, 69477949, 69478037, 69478398, 69479136, 69479479, 69481748, 69483526, 69484800, 69485374,
69485906, 69486695, 69487864, 69487913, 69489390, 69489590, 69490137, 69490591, 69491509, 69492024, 69492870, 69494132, 69494189, 69494222, 69494423, 69496257, 69497648, 69497762, 69499135, 69499309, 697156063, 697156066, 697156329]
    for i in flist[flist.index(start):]:
        print("start scan code by factory : %d " % i)
        s.scan_code_by_factory(i, code_start)
        print("end scan code by factory : %d " % i)
        code_start = 0

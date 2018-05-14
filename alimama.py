#coding:utf-8

__author__ = 'liukoo'
import requests
from urllib.request import re
from hashlib import md5
from bs4 import BeautifulSoup as bs
from pandas import DataFrame as df
import random
user_agent = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
turl = "https://pub.alimama.com/common/code/getAuctionCode.json?auctionid=540073519626&adzoneid=130562660&siteid=36508049&scenes=1&t=1506759753037&_tb_token_=7860be36b8bb3&pvid=10_218.76.46.199_550_1506759736002"
theader = {
    "User-Agent": random.choice(user_agent),
}
res = requests.get(turl, headers = theader)
res = bs(res.content.decode())
lurl = res.iframe.attrs["src"]
res = requests.get(lurl)
ld = bs(res.content.decode("utf-8","ignore"))
inputdata = ld.body.div.div.div.find("form", id="J_Form")
inputdata = inputdata.find_all("input")
postdata = {}
for i in inputdata:
    try:
        name = i.attrs["name"]
    except:
        continue
    try:
        value = i.attrs["value"]
    except:
        value = ""
    postdata[name] = value


jsd = ld.find_all("script")[9]
p = re.compile("appkey : \"\S*\"")
postdata["appkey"] = p.findall(jsd.text)[0][10:-1]
p = re.compile("token : \"\S*\"")
postdata["token"] = p.findall(jsd.text)[0][9:-1]




loginurl = "https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http://login.taobao.com/member/taobaoke/login.htm?is_login=1&full_redirect=true&disableQuickLogin=true"

logindata = {
    "user":"ca17775879355@qq.com",
    "password":"Clove888",
    "TPL_username":	i%B4%B4%C6%BD%CC%A8%B4%B4%B0%AE%BF%C6%BC%BC
    "TPL_password":"",	
    "ncoSig":"",
    "ncoSessionid":"",
    "ncoToken":"f7066ba8d02c81fcb7f207d54e6edc7d35d45aa1",
    "slideCodeShow":"false",
    "useMobile":"false",
    "lang":"zh_CN",
    "loginsite":"0",
    "newlogin":"0",
    "TPL_redirect_url":"http://login.taobao.com/member/taobaoke/login.htm?is_login=1",
    "from":"alimama",
    "fc":"default",
    "style":"mini",
    "css_style":"",
    "keyLogin":"false",
    "qrLogin":"true",
    "newMini":"false",
    "newMini2":"true",
    "tid":"",
    "loginType":"3",
    "minititle":"",
    "minipara":"",
    "pstrong":"",
    "sign":"",
    "need_sign":"",
    "isIgnore":"",
    "full_redirect":"true",
    "sub_jump":"",
    "popid":"",
    "callback":"",
    "guf":"",
    "not_duplite_str":"",
    "need_user_id":"",
    "poy":"",
    "gvfdcname":"10",
    "gvfdcre":"",
    "from_encoding":"",
    "sub":"",
    "TPL_password_2":"18ec3b8894b3578c3b86d30ef75423378141d946603afce4aa083b2a74fc0239c63905d843da87ec59a879b56fcb163f529769335343271f22c1efc8c4a35f8e30382d7c82d847fdfc8e28fcb3e74fdc204680b64dbe785c3265c4663295f122eff4fdfd3a253a38dfdbf7ddf7776a34c439fd1783c745e471ab1ca3542aaba0",
    "loginASR":"1",
    "loginASRSuc":"1",
    "allp":"",
    "oslanguage":"zh-CN",
    "sr":"1536*864",
    "osVer":"",
    "naviVer":"firefox|56",
    "osACN":"Mozilla",
    "osAV":"5.0+(Windows)",
    "osPF":"Win32",
    "miserHardInfo":"",
    "appkey":"",
    "nickLoginLink":"",
    "mobileLoginLink":"https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http://login.taobao.com/member/taobaoke/login.htm?is_login=1&full_redirect=true&disableQuickLogin=true&useMobile=true",
    "showAssistantLink":"",
    "um_token":"HV01PAAZ0b85eb40da4c2ec759e80525002cd589",
    "ua":"099#KAFEr7EgEGFE6YTLEEEEE6twSXvqn6NcZXs5S6AqgswEZ6Y5YR+jG6GmZX+0LMATgsBEnIzwDywMNMUmDORqDIz1DRkHAKqTET4SluZdtpAiiiSPbbCmVbv0rokKQdkDYovK4GFEhiilsyaSUCP63xZCaKB8Cf8VAMvLAykTCo49E7EFD67EEKqTET4SluZdtp35iiSPbbCmVbv0rokKQdkDYovKJGFET6i5EE1iE7E063lP/3x+n4StRyRqNXyKZyvH+X3HPMJKCjdTEEi5DEEEIGFET/dEsyCs8TdTEEi5DEEErGFEhL7FusCi4llllav+/pwGRB8tY0s3YuaHLBvE6GFE19dIvRG4K3ldYwoTETEMTTWdj4yluJXKYPpEVyB66GFE19dE2saJAllQEYoTEEylEcZdt3xzE7Tx1F9VEHq6m/NrLLjoiDN7VmyO3LHq1ZWccMYtqMN05cHkukj2wNoZeZWcqNGRkmwvmrYAKNvk3QYvbHUSmStDbHwvB1A0DL8I6OT2cHXKyUQl+pSTE1LlluZdt3illllls43StE7illlO/3iS1Jnllurdt37In3llWFRStEL5OGFETYLlssnTtASTEELlluaLAzI70MoTEcL5qEEEaquYSpXfNV96Ly32rz7WbIDpPfOW8yXZ97ZAnRyic096Ly32rz7D6qd6rIXvSsGZ1GhVSROiFaoRLVvGrPq0vbtcUoiCNw8nw7hDZyn7bRMpcWywb64VbUO3YfcMzi7WadsAGuJxUKIulu2Ydoc2h536rtCtSAoW1UZZDsrmbyo6uuyiVe1ZbYDpbo3AGVU07duDZOyBPs5RuuyiVeEZPQbqrzxdCR2x3/lvUyncOa26+snidoc28o/udzxgai2/iYrGZ2ywbiUTaWyib0oCPIQpPPeAQReS+UCMts326Vs3ieJF/GFETJDovl49E7EFD67EEK5TEEilluCVz7FET6imEEEnE7EB6Exp/JAdll+ZKyR/YXcAUoDK8fZEWM4nE7EKlGgq/14zllG0IGFEHw7EsyCsvFStRB8fnM9SZyvHLyp64GFEhiilsyaSU8K63xZCaKB8Cf8VAMvLAykTCo8iE7E063lP/3xbM4StRyRqNXyKZyvH+X3HPMJKC0qTET4SluZdtpZqiiSPbbCmVbv0rokKQdkDYovKrGFEhL7FQsAby3lllZ48/RsgxfhHbMiIztcTa2hKJGFET6i5EEELE7E563lP/ptsiiSPX0nfgli0rok6bUSLE7E56EwP/ptZKBNKSMljvXNKaMJ6g6d="
}
theader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
}
tcookie = {
    "t":"0ea5f4649f5843e94fc7b17f5c947983",
    "cna":"4MFkEgtrfyoCAdpMLsehSCda",
    "isg":"AjQ0Y5Zu0Y9uDUVKrSS-ywrTBPFmpVmYMg6J-M6VwL9COdSD9h0oh-r7z0of",
    "account-path-guide-s1":"true",
    "126044062_yxjh-filter-1":"true",
    "cookie2":"1f10d188d7b57f03f3175bd4578dc6e3",
    "v":"0",
    "_tb_token_":"75817b34e8bbd",
    "alimamapwag":"TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NDsgcnY6NTYuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC81Ni4w",
    "cookie32":"46c704ea924f6776864a1ab0408c1367",
    "alimamapw":"WUZwBxQnDRx2D0QgcUMlcRUjCEZwBxQnDRx3CUQjcEMkdBUhBkZwcBQnejAFDAVWAwdRBQAABVQLAVIDCVoGDlJRV1dRA1ZWAQdXUQ",
    "cookie31":"MTI2MDQ0MDYyLGklRTUlODglOUIlRTUlQjklQjMlRTUlOEYlQjAlRTUlODglOUIlRTclODglQjElRTclQTclOTElRTYlOEElODAsY2ExNzc3NTg3OTM1NUBxcS5jb20sVEI",
    "login":"VT5L2FSpMGV7TQ=="
}

# 模拟登录，获得cookie
loginurl = "https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http://login.taobao.com/member/taobaoke/login.htm?is_login=1&full_redirect=true&disableQuickLogin=true"
logindata = {
    "TPL_username":"i%B4%B4%C6%BD%CC%A8%B4%B4%B0%AE%BF%C6%BC%BC",
    "TPL_password":"",
    "ncoSig":"",
    "ncoSessionid":"",
    "ncoToken":"406e13965b34656ea9f0192afff11ee284d6b38a",
    "slideCodeShow":"false",
    "useMobile":"false",
    "lang":"zh_CN",
    "loginsite":"0",
    "newlogin":"0",
    "TPL_redirect_url":"http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3D1",
    "from":"alimama",
    "fc":"default",
    "style":"mini",
    "css_style":"",
    "keyLogin":"false",
    "qrLogin":"true",
    "newMini":"false",
    "newMini2":"true",
    "tid":"",
    "loginType":"3",
    "minititle":"",
    "minipara":"",
    "pstrong":"",
    "sign":"",
    "need_sign":"",
    "isIgnore":"",
    "full_redirect":"true",
    "sub_jump":"",
    "popid":"",
    "callback":"",
    "guf":"",
    "not_duplite_str":"",
    "need_user_id":"",
    "poy":"",
    "gvfdcname":"10",
    "gvfdcre":"",
    "from_encoding":"",
    "sub":"",
    "TPL_password_2":"79ff2b63e1f92f0f941fd65b68704f238f575332d2ddc32e45873ed6e851ecf602a0b8c661f370605405dfb71b1d6db8fda7a7caf2eac33bd99056d589444de7c2e4983c4cd7f43017d57076412fe66b1e00d7ccf38f6171f8baefde140fef33fa95075519ac7be8af32f125d8dbe3d81b1f8a0f0569776f9fe0e966bfae6cc6",
    "loginASR":"1",
    "loginASRSuc":"1",
    "allp":"",
    "oslanguage":"zh-CN",
    "sr":"1536*864",
    "osVer":"",
    "naviVer":"firefox%7C56",
    "osACN":"Mozilla",
    "osAV":"5.0+%28Windows%29",
    "osPF":"Win64",
    "miserHardInfo":"",
    "appkey":"",
    "nickLoginLink":"",
    "mobileLoginLink":"https%3A%2F%2Flogin.taobao.com%2Fmember%2Flogin.jhtml%3Fstyle%3Dmini%26newMini2%3Dtrue%26from%3Dalimama%26redirectURL%3Dhttp%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3D1%26full_redirect%3Dtrue%26disableQuickLogin%3Dtrue%26useMobile%3Dtrue",
    "showAssistantLink":"",
    "ua":"099%23KAFE67EYEP5E6YTLEEEEE6twSXvqV6A3SXJ5C6NqDXBMNftHZcs5%2BfD1DuRMNMt3gs9FV6GBguh0A6digRyYSIzEYswYg0qTET4SluZdt6yniiSPbbCmVbv0rokKQdkDYovKIGFEHwilsyaUpFStRB8fnM9SZyvHLyp6JGFET6i5EEELE7E56EwP%2FcghiiSPX0nfgli0rok6bUSLE7E563lP%2F3Q6iiSPX0nfgli0rok6bUSLE7E56EwP%2F3FGiiSPX0nfgli0rok6bUS9E7EFD67EERbTETUSEwWd4Kwllld7BOCYd1DV%2FMhXaQ3bAMDVGwoTEToSE1cd8KLlw3D6%2F91OZQJKCf81azw3GwoTEEd5EHcdLQll1JUNb%2FeyWyhmE7EFlllbr7oTEEylEcZdt3xzE7TxTTxWEF2cqiToRKA3ccSQqCAnZDz%2FtiEsM8wokx%2FPcv64fmZo09ma3kj2iIDkWL7A6LhcLiL%2Bq1AnyNU0pu5sM8TCk7YCsn64fBxo8CrGkL6o32dTEEMIluutG9ofE7EIlllbQd9uMh2PE7EUlllP%2F3iSllllluVwt37FFlllWsaStEgtlllO%2F3iS16allug1t37IDIoTEcL5qEEEaquYSpXfNV96Ly32rz7WbIDpPfOW8yXZ97ZAnRyic096Ly32rz7D6qd6rIXvSsGZ1GhVSROiFaoRLVvGrPq0vbtcUoiCNw8nw7hDZyn7bRMpcWywb64VbUO3YfcMzi7WadsAGuJxUKIulu2Ydoc2h536rtCtSAoW1UZZDsrmbyo6uuyiVe1ZbYDpbo3AGVU07duDZOyBPs5RuuyiVeEZPQbqrzxdCR2x3%2FlvUyncOa26%2Bsnidoc28o%2Fudzxgai2%2FiYrGZ2ywbiUTaWyib0oCPIQpPPeAQReS%2BUCMts326Vs3ieJF%2FGFETJDovl49E7EFD67EEp5TEEi5D7EE6GFEwA7EBRADf9dIhxkCuz%2FzbioTEEd5E1%2BdYURl1KqNb%2FeyWyFnE7E3HEE8%2FIxFlGaEKyRW8u8AIGFET%2FllsyauT1qTEEylEcZdWJesE7Eqlld%2F%2FfRxllllyHrdrGFEhL7EKOCmN9lllnan%2FpwGRB8tY0s3YuaHLBvEJGFET6i5EE1iE7E063lP%2F3ikU5StRyRqNXyKZyvH%2BX3HPMJKCjdTEEi5DEEEJGFET6i5EE1sE7E26EEV%2FhmNllllNFhd%2FrHKSMkAgq%2BvSQJ6UM4%3D",
    "um_token":"HV01PAAZ0b871d89da4c2ec759e83fcb0033678a"
}

res = requests.get(loginurl)
res = bs(res.content)
res = res.body.div.div.div.find("form", id="J_Form")
t = res.find_all("input")
logindata = {}
for i in t:
    try:
        lname = i.attrs["name"]
    except KeyError as keye:
        continue
    try:
        lvalue = i.attrs["value"]
    except KeyError as keye:
        lvalue = ""
    logindata[lname] = lvalue
logindata = {}
logindata["TPL_username"] = "i创平台创爱科技".encode()
logindata["TPL_password"] = md5("Clove#!$159".encode()).hexdigest()
logindata = {}
logindata["TPL_username"] = "i创平台创爱科技"
logindata["TPL_password"] = "Clove#!$159"

res = requests.post(loginurl,data=logindata,headers=theader)

res2 = requests.get(turl, cookies=res.cookies, headers=theader)

res2 = requests.get(turl, cookies=tcookie, headers=theader)
print(res2.content.decode())
# cookies = {
#     "t":"d8058854161aaa72fd0b3cccf043dca6",
#     "cna":"4MFkEgtrfyoCAdpMLsehSCda",
#     "isg":"AuHh3C2iHFEn-bAl6EMHIvAk8a07JlTtTUEwV0O23ehHqgF8i95lUA_qeuXS",
#     "v":"0",
#     "cookie2":"17ac18b0e81d9fa89a2bc76af6cd65d9",
#     "_tb_token_":"ede9de3eeeba5",
#     "alimamapwag":"TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQ7IHJ2OjU2LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvNTYuMA==",
#     "cookie32":"46c704ea924f6776864a1ab0408c1367",
#     "alimamapw":"WkFzUR1yVkFxD0chdB13chUjC0FzUR1yVkFwCUcidR12dxUhBUFzJh1yIW0CDAZXBlkDBgAABlMIV1tWUgcBDlFQUgkDAFZWAgBUBw",
#     "cookie31":"MTI2MDQ0MDYyLGklRTUlODglOUIlRTUlQjklQjMlRTUlOEYlQjAlRTUlODglOUIlRTclODglQjElRTclQTclOTElRTYlOEElODAsY2ExNzc3NTg3OTM1NUBxcS5jb20sVEI=",
#     "login":"UIHiLt3xD8xYTw==",
# }
cookie_handle = cookiejar.CookieJar()
opener = request.build_opener(request.HTTPCookieProcessor(cookie_handle))
request.install_opener(opener)

class alimama:
    def __init__(self):
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'}
        #cookie 支持
        self.cookie_handle = cookiejar.CookieJar()
        self.opener = request.build_opener(request.HTTPCookieProcessor(self.cookie_handle))
        request.install_opener(self.opener)
    #登陆
    def login(self,username,passwd):
        login_data = {
            'logname':'ca17775879355@qq.com',
            'originalLogpasswd':'Clove888',
            'logpasswd':'',
            'proxy':'',
            'redirect':'',
            'style':''
        }
        login_data['logname'] =username
        login_data['originalLogpasswd'] =passwd
        login_data['logpasswd'] = md5(login_data['originalLogpasswd'].encode()).hexdigest()
        source = request.urlopen('http://www.alimama.com/member/minilogin.htm').read()
        token_list = re.findall(r"input name='_tb_token_' type='hidden' value='([a-zA-Z0-9]+)'", source.decode())
        login_data['_tb_token_'] = token_list[0] if token_list else ''
        loginurl = 'https://www.alimama.com/member/minilogin_act.htm'
        #拼接post数据
        login_data = urllib.parse.urlencode(login_data)
        self.header['Referer'] = 'http://www.alimama.com/member/minilogin.htm'
        try:
            req = request.Request(url=loginurl,data=login_data.encode(),headers=self.header)
            resp =request.urlopen(req)
            html = resp.read()
            if str(resp.url).find('success')!=-1:
                return True
        except Exception as e:
            print(e)
            return False
    #获取商品的推广链接
    def getUrl(self,url):
        try:
            item_id = re.search(r"id=(\d+)",url)
            item_id = item_id.group(1)
            html = request.urlopen('http://u.alimama.com/union/spread/common/allCode.htm?specialType=item&auction_id='+item_id).read()
            rule = re.compile(r"var clickUrl = \'([^\']+)")
            return rule.search(html).group(1)
        except Exception as e:
            print(e)
            return False

#example
ali = alimama()
if ali.login(loginname,loginpwd):
    url = ali.getUrl(turl)
    if url:
        print(url)
    else:
        print('获取推广链接失败')
else:
    print('登陆失败')
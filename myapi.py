from urllib import request
from urllib.parse import quote

def idcheck(idnum, name)
    """3023接口验证身份证与姓名是否一致，每次查询价格：一致0.2元，不一致0.2元，身份证号码错误0.0005元"""
idnum = '430221197901020012'
import re
pattern = re.compile('[A-WY-Za-wy-z]')
idnum = re.subn(pattern, '', idnum)[0]
if len(idnum) != 18:print('错误的身份证号码')

check_code = 10 if idnum[17]=='x' else int(idnum[17])

check_index = range(17)
w = []
for i in ind:
    w.append(2**(17-i) % 11)
check_weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2] # 各位数权重计算方法 .append(2**(17-i) % 11)
# 校验方法，(各位数*权重)求和 % 11
check_sum = 0
for i in check_index:
    check_sum = check_sum + int(idnum[i])*w[i])

check_sum = (check_sum + int(10)*1) if idnum[17] == 'x' else (check_sum + int(idnum[17]) * 1)

print('身份证号码有效') if check_sum == check_code else print('身份证号码无效')


    appkey = 'a88edb53f621b716691aa878d62d1994' # 3023接口密钥
    gurl = ('https://api.3023.com/idcard/authenticate'
            '?idcard=%s'
            '&name=%s'
            % (idnum, name))
    gurl = quote(gurl, safe='/:?&=')

    req = request.Request(gurl)
    req.add_header('key', 'a88edb53f621b716691aa878d62d1994')
    res = request.urlopen(req)
    content = res.read().decode()
    return content
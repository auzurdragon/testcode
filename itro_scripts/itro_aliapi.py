appinfo = {
    'appkey':'24598266',
    'apps'
}

url = 'http://pub.alimama.com/common/code/getAuctionCode.json?auctionid=540073519626&adzoneid=130562660&siteid=36508049&scenes=1&t=1506759753037&_tb_token_=7860be36b8bb3&pvid=10_218.76.46.199_550_1506759736002'

userinfo = {
    'TPL_username':'auzurdragon',
    'TPL_password':'s1i9n7d9y'  
}



cookies = {
    'ken_':'708ab38e1e881',
    '_umdata':'6AF5B463492A874D8618157602450F88AD53FD773ED6D53F3CC9C25E54D9F566CB0DC89BD38E1351CD43AD3E795C914C26824BC6112E8BF7D2BF10A2207C2E5F',
    'cna':'3uyaEnc1AykCAdpMLsfu2eR5',
    'cookie2':'1054521c789338c920526bef6d078259',
    'isg':'AuzsO2Fkmqy9AI6QCO3x-HvHvsneDZA8KtZJEEYt-Bc6UYxbbrVg3-JhAyOW',
    'rurl':'aHR0cDovL3B1Yi5hbGltYW1hLmNvbS9jb21tb24vY29kZS9nZXRBdWN0aW9uQ29kZS5qc29uP2F1Y3Rpb25pZD01NDAwNzM1MTk2MjYmYWR6b25laWQ9MTMwNTYyNjYwJnNpdGVpZD0zNjUwODA0OSZzY2VuZXM9MSZ0PTE1MDY3NTk3NTMwMzcmX3RiX3Rva2VuXz03ODYwYmUzNmI4YmIzJnB2aWQ9MTBfMjE4Ljc2LjQ2LjE5OV81NTBfMTUwNjc1OTczNjAwMg==',
    't':'b699e691f5ff81919e3c48f97969b662',
    'v':'0'
}

t=b699e691f5ff81919e3c48f97969b662;
cna=3uyaEnc1AykCAdpMLsfu2eR5;
isg=AoKCeRW6bElpS3CSAvuHmkEJ0Isk-4YegMiXksybrvWgHyKZtOPWfQhdvSCd;
v=0;
cookie2=1b1f3a089a0e29ee4f2062f5050aebde;
_tb_token_=eb38ee6fdbd71;
alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NDsgcnY6NTguMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC81OC4w;
cookie32=118948093111433d1e91b09682711bef;
alimamapw=BUceQkMBQVUCDg9sVAVWBQBSUwVUVQRSCgYGB1EGVwcBAlQCUwMCAwABVlY%3D;
cookie31=NjgwNjkxNzMsYXV6dXJkcmFnb24sYXV6dXJkcmFnb25AMTYzLmNvbSxUQg%3D%3D;
login=U%2BGCWk%2F75gdr5Q%3D%3D



client_id = '24598266'
response_type = 'code'
redirect_uri = 'https://pub.alimama.com/common/code/getAuctionCode.json?auctionid=540073519626&adzoneid=130562660&siteid=36508049&scenes=1&t=1506759753037&_tb_token_=7860be36b8bb3&pvid=10_218.76.46.199_550_1506759736002'
state = '1212'
view = 'web'


url = 'https://oauth.taobao.com/authorize?response_type=code&client_id=%s&redirect_uri=%s&state=1212&view=web' % (client_id, redirect_uri)

import requests




url = 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true'

header = {
    'Host':'login.taobao.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
}

tmp = requests.get(url, headers=header)
tmp = bs(tmp.content, 'lxml')
tmp = tmp.body.find('form', id='J_Form')

info = {
    'TPL_username':'',
    'TPL_password':'',
}
for item in tmp:
    if
    info[item['name']] = item.get('value')


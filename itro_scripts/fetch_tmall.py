# 抓取数据
# driver, 传入访问页面的驱动
# url, 页面URL，示例 https://s.taobao.com/search?q=%s&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&tab=mall&sort=sale-desc&bcoffset=0&s=%d' % ('纸尿裤',1)

from bs4 import BeautifulSoup as bs
from random import randint, choice
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests.utils import quote
header = [
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"},
    {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},
    {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'},
    {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {"User-Agent":'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'},
    {"User-Agent":'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'},
    {"User-Agent":'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)'},
    {"User-Agent":'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0'},
    {"User-Agent":'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'},
    {"User-Agent":'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201'},
    {"User-Agent":'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'},
]
pnum = 4000 # 预计抓取的商品总数
q = '纸尿裤'   # 检索关键字
result = []     # 保存结果

params = DesiredCapabilities.PHANTOMJS.copy()
params['phantomjs.page.settings.userAgent'] = (choice(header))
params['phantomjs.page.settings.loadImages'] = False
driver = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=params)
driver.implicitly_wait(10)
for i in range(1629,pnum,44):
    print(i)
    url = 'https://s.taobao.com/search?q=%s&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&tab=mall&sort=sale-desc&bcoffset=0&s=%d' % (q,i)
    url = quote(url, safe=':/?&.-_=')
    print(url)
    try:
        driver.get(url)
        sleep(5)
    except Exception as e:
        print(i, e)
        params['phantomjs.page.settings.userAgent'] = (choice(header))
        params['phantomjs.page.settings.loadImages'] = False
        driver = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=params)
        driver.implicitly_wait(10)
        print(i,'except')
        driver.get(url)
        sleep(5)
    finally:
        tmp = bs(driver.page_source, 'lxml')
        tmp = tmp.body.find_all('div', class_='J_MouserOnverReq')
        for item in tmp:
            item_info = {
                '图片链接':item.find('img').get('src'),   # 商品缩略图
                '商品价格':item.find('div', class_='price').strong.text,   # 商品价格
                '收货人数':item.find('div', class_='deal-cnt').text.split('人')[0],  # 收货人数
                '商品名称':item.find('div', class_='title').a.text.strip(),    # 商品标题
                '商品链接':item.find('div', class_='title').a.get('href'),  # 商品链接
                '店铺':item.find('div', class_='shop').a.text.strip(),      # 商店名称
                '所在地':item.find('div', class_='location').text,        # 所在地
            }
            # 修改数据类型
            item_info['商品价格'] = int(float(item_info['商品价格']) * 100)
            item_info['收货人数'] = int(i['收货人数'])
            # spec, 1天猫店, 0其它店
            item_info['shop'] = 1 if item_info['店铺'] == '天猫超市' else 0
            item_info['details'] = False  # 抓取商品详情的状态，False已抓取
            item_info['detail_char'] = ''   # 商品祥情字符串
            item_info['search_q'] = q
            item_info['product_id'] = re.search('id=\d*', item['商品链接']).group(0)[3:]
            result.append(item_info)
        print(i, len(result))

# 获得商品的规格信息，使用requests
# 使用result数据集，由上一步生成。
# 天猫超市和天猫国际官方直营店的详情数据不全，跳过
import requests, re
from bs4 import BeautifulSoup as bs
from random import randint, choice
from time import sleep
header = [
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"},
    {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},
    {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'},
    {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {"User-Agent":'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'},
    {"User-Agent":'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'},
    {"User-Agent":'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)'},
    {"User-Agent":'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0'},
    {"User-Agent":'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'},
    {"User-Agent":'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'},
    {"User-Agent":'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201'},
    {"User-Agent":'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'},
]

for item in result:
    print(result.index(item))
    if item['details'] or item['shop'] == 1:    # 天猫超市详情页无规格数据，跳过
        continue
    else:
        try:
            tmp = requests.get('http:%s' % item['商品链接'], headers=choice(header))
            tmp = bs(tmp.content, 'lxml')
            tmp = tmp.body.find('div', class_='attributes')
            tmp = tmp.find_all('li')
            tmp = [i.text.strip().replace('\xa0', '') for i in tmp]
            for i in tmp:
                j = re.split('[:：]', i)
                item[j[0]] = j[1]
                item['detail_char'] = '%s;%s;%s' % (item['detail_char'],j[0],j[1])
            item['shop'] = 2
            item['details'] = True
            print (item)
        except Exception as e:
            print(result.index(item), e)
        sleep(randint(0,2))

# 获得天猫超市商品的规格和片数
error = []
for i in result:
    if i['shop'] == 1:
        try:
            # 从商品名称中查找规格和尺寸信息
            # 反向查询[::-1]，避免名称前是英文名称的问题, 查找结果需要再次反转
            # 规格的字符 [smlxbSMLXNB]{1,3}
            # '\d{0,3}[*+]{0,1}[号码片 ]{0,2}\d{0,3}[smlxbSMLXNB]{1,3}'  ，可能的组合包括： L114, S84片*2包, NB40+2片, XL 38片
            tmp = re.search('\d{0,3}[*+]{0,1}[号码片 ]{0,2}\d{0,3}[SMLXNB]{1,3}',i['商品名称'][::-1][2:]).group().replace('片', '').replace('号', '').replace('码', '').replace(' ', '')[::-1]
            # 提取尺寸信息
            tmp_size = re.search('[a-zA-Z]{1,3}', tmp).group()
            tmp_num = re.search('\d{1,3}[*+]{0,1}\d{0,2}', tmp).group()
            if tmp.find('*') > 0:
                tmp_num = tmp_num.split('*')
                tmp_num = int(tmp_num[0]) * int(tmp_num[1])
            elif tmp.find('+') > 0:
                tmp_num = tmp_num.split('+')
                tmp_num = int(tmp_num[0]) + int(tmp_num[1])
            else:
                tmp_num = int(tmp_num)
            print(result.index(i), tmp_size, tmp_num, i['商品名称'])
            i['product_size'] = tmp_size
            i['product_num'] = tmp_num
        except Exception as e:
            error.append(result.index(i))
            print(e, tmp_num, result.index(i), i['商品名称'])
        finally:
            for i in error:
                print('error: %d, %s' % (i, result[i]['商品名称']))

# 获得其它商品的规格
error = []
for i in result:
    if i['shop'] != 1:
        namelist = set(['尿片规格型号', '尿片规格', '品牌', '具体规格', '产品名称']) & set(i.keys())
        namelist = list(namelist)
        namelist.sort(reverse=True)
        print(namelist)
        tmp = ';'.join([i[j] for j in namelist])
        tmp = '%s;%s' % (tmp, i['商品名称'][6:])
        try:
            tmpt = re.search('[SMLX]{1,3}|(NB)',tmp).group().replace('片', '').replace('号', '').replace('码', '').replace(' ', '')
            print('success: %d, %s, %s' % (result.index(i), tmpt, tmp))
            i['product_size'] = tmpt
        except Exception as e:
            print('failed: %d, %s, %s' % (result.index(i),tmp, i['商品名称']) )
            error.append(result.index(i))

for i in error:
    print('failed: %d, %s' % (i, result[i]))
    result[i]['product_size'] = input('请输入尺寸SMLXNB ： ')

# 修改规格数据
error =[]
errsize = ['SML', 'MLX', 'SNB', 'XXX', 'ML', 'LXL', 'SLN', 'SM']
for i in result:
    if i['product_size'] in errsize:
        tmp = ['尿片规格', '品牌', '具体规格', '产品名称']
        namelist = set(tmp) & set(i.keys())
        name1 = list(namelist)
        namelist = []
        for nl in tmp:
            if nl in name1:
                namelist.append(nl)
        tmp = ';'.join([i[j] for j in namelist])
        tmp = '%s;%s' % (tmp, i['商品名称'][6:])
        try:
            tmpt = re.search('[SMLX]{1,3}|(NB)',tmp).group().replace('片', '').replace('号', '').replace('码', '').replace(' ', '')
            i['product_size'] = tmpt.upper()
            print('success: %d, %s, %s' % (result.index(i), tmpt, tmp))
        except Exception as e:
            print(e)
            error.append(result.index(i))
            print('failed: %d, %s, %s' % (result.index(i), e, i))
            i['product_size'] = input().upper()

for i in result:
    if i['product_size'] == 'XXX':
        print(i)
        i['product_size'] = input().upper()


# 获得其它商品的包装片数 product_num
error = []
numset = set()
for i in result:
    if i['shop'] != 1:
        tmp = ['product_num', '包装数量(片)', '尿片规格型号', '尿片规格', '具体规格', '产品名称']
        namelist = set(tmp) & set(i.keys())
        name1 = list(namelist)
        namelist = []
        for nl in tmp:
            if nl in name1:
                namelist.append(nl)
        tmp = ';'.join([i[j] for j in namelist])
        tmp = '%s;%s' % (tmp, i['商品名称'][7:])
        p_num = ''
        try:
            p_num = re.search('\d{1,3}[号码片 ]{0,1}[*+]{0,1}[SMLX]{0,1}(夜用){0,1}\d{0,2}', tmp).group().replace('号', '').replace('码', '').replace('片', '').replace(' ', '').replace('夜用','').replace('S','').replace('L','')
            # print('success: %d, %s, %s' % (result.index(i), p_num, tmp))
            if p_num.find('*') > 0:
                p_numt = p_num.split('*')
                p_num = int(p_numt[0]) * int(p_numt[1])
            elif p_num.find('+') > 0:
                p_numt = p_num.split('+')
                p_num = int(p_numt[0]) + int(p_numt[1]) 
            else:
                p_num = int(p_num)
            i['product_num'] = p_num
        except Exception as e:
            print('failed: %d, %s, %s' % (result.index(i), p_num, i))
            error.append(result.index(i))
            i['product_num'] = int(input('请输入商品包装片数：'))

# 获得商品品牌数据
brandlist = []
for i in result:
    if '品牌' in i.keys():
        tmp = i['品牌'].replace('（母婴）','').split('/')
        tmp = tmp[1].upper() if len(tmp) > 1 else tmp[0].upper()    # 排除英文名称
        brandlist.append(tmp)

# brandlist = brandlist + ['爱的童话', '优步', '尤妮佳', 'SPIRITKIDS', '婴之良品','爱婴舒坦']
brandlist = list(set(brandlist))
brandlist = '|'.join(brandlist)
error = []
for i in result:
    tmp = i['品牌'].upper()+i['商品名称'].upper() if '品牌' in i.keys() else i['商品名称'].upper()
    try:
        tmp = re.search(brandlist, tmp).group()
        print('success: %d, %s, %s' % (result.index(i), tmp, i['商品名称']))
        i['product_brand'] = tmp
    except Exception as e:
        error.append(result.index(i))
        print('failed: %d, %s, %s, %s' % (result.index(i), tmp, i['商品名称'], i['商品链接']))
        i['product_brand'] = input('请输入品牌名称：')

# 计算每片单价
for i in result:
    i['product_unitprice'] = i['商品价格']/i['product_num']

# 补充产地数据
for i in result:
    i['product_location'] = i['产地'] if '产地' in i.keys() else '中国大陆'

# 修改数据类型
for i in result:
    i['收货人数'] = int(i['收货人数'])
    i['商品价格'] = int(float(i['商品价格'])*100)



# 恢复查询结果
import pickle
with open('tmp/tb_fetch.pkl', 'rb') as r:
    result = pickle.load(r)

# 转换数据框
import pandas as pd
names = ['product_id', '收货人数','商品价格', '商品名称', 'product_size', 'product_num', 'product_location', 'product_brand', 'product_unitprice']
        #   'location', 'spec', 
        #  '产品名称', '产地', '具体规格', '包装数量(片)', '品牌', '尿不湿品类', '尿片规格', '尿片规格型号', '系列', '适合体重',]
td = pd.DataFrame(result, columns=names)
td = td.rename(columns={
    'product_id':'p_id',
    '收货人数':'s_users', 
    '商品价格':'s_price', 
    '商品名称':'s_title',
    'product_size':'s_size',
    'product_num':'s_num',
    'product_location':'s_location',
    'product_brand':'s_brand',
    'product_unitprice':'s_unitprice'})
td = td.ix[:,['p_id','s_users','s_price','s_size','s_num','s_brand','s_unitprice']]

# 设置size,为定序数据
td['s_brand'] = td['s_brand'].astype('category')
td['p_size'] = td['s_size'].map(lambda x:['NB','S','M','L','XL','XXL','XXXL'].index(x))
td['p_size'] = td['p_size'].astype('category')
td['p_size'].cat.categories = (['NB','S','M','L','XL','XXL','XXXL'])

# 将p_users收货人数, p_num包装片数分组
td['p_users'] = td['s_users'].map(lambda x: x // 1000)
td['p_num'] = td['s_num'].map(lambda x: x // 10)


# 按尺寸和包装片数分组，绘制收货人数热力图
from matplotlib import pyplot as plt
import seaborn as sns

tdp = td.pivot_table(index='p_size', columns='p_num', values='s_users', aggfunc='sum')

fig= plt.figure(figsize=[12,6])
p = sns.heatmap(tdp, cmap='Blues', linewidths = 0.05)
p.title.set_text('尺寸-片数:收货人数合计热力图，样本数量：4003')
p.axes.set_xlabel('包装片数：按10片分组')
p.axes.set_ylabel('尺码')
p.axes.invert_yaxis()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.show(fig)


# 提取收货人数在1000以上的数据，绘图
tdp = td[td.s_users >= 1000].ix[:,['s_users','s_price','s_num','p_size','s_unitprice',]]
tdp = tdp.rename(columns={'s_users':'收货人数', 's_price':'价格', 's_num':'片数', 'p_size':'尺寸', 's_unitprice':'平均价格'})

fig = plt.figure(figsize=(9,9))
p = sns.PairGrid(data=tdp,hue='尺寸', size=3, vars=['收货人数','价格','片数','尺寸','平均价格'])
p.map_diag(plt.hist, rwidth=0.85)
p.map_upper(plt.scatter,s=2)
p.map_lower(plt.scatter, s=2)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.show(p)
plt.savefig('')


# 计算p_users收货人数的极值点
tmp = td.describe()
tmp = tmp['p_users'][6] + (tmp['p_users'][6] - tmp['p_users'][5])*1.5

# 选择p_users大于异常值的记录
tdp = td[td.p_users >= tmp].ix[:,['p_users', 'p_size', 'p_num', 'p_unitprice', 'p_price', 's_size']]

# 绘制配对图
p = sns.pairplot(data=td, 
                # hue='p_size', 
                # hue_order=td.s_size.cat.categories, 
                vars = ['p_users', 'p_size', 'p_num', 's_unitprice'], 
                kind='scatter', 
                diag_kind='boxplot',
                )

p = sns.pairplot(data=td, 
                # hue='Blues', 
                # hue_order=td.s_size.cat.categories, 
                vars = ['p_users', 'p_num', 'p_size', 's_unitprice'], 
                kind='scatter', 
                diag_kind='boxplot',
                )


# 绘制热力图
tdp = td.pivot_table(index='s_size', columns='p_num', values='p_users', aggfunc=np.sum)
# 保存CSV
with open('tmp/tb_fetch.csv', 'w') as w:
    td.to_csv(w)

# 保存查询结果
import pickle
with open('tmp/tb_fetch.pkl', 'wb') as w:
    pickle.dump(result, w)



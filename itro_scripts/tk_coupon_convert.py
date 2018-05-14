"""
手动配置优惠券链接二合一页面手动配置教程：
1、参数配置
通过在url中配置以下参数，得到一个优惠券+对应单品的页面。
activityId：券的标识，可从商家给到的优惠券url中获得；
itemId：商品的标识，可从商家处获得，也可从商品详情页的url中获得；
pid：推广渠道的标识，mm开头的三段式；
优惠券链接：http://shop.m.taobao.com/shop/coupon.htm?sellerId=800522100&activityId=e73a59933f72481cb2873ce427db3fa4
淘宝客链接：https://item.taobao.com/item.htm?id=535476074530&ali_trackid=2:mm_89785546_8246652_27920024:1476793835_3k2_1957083247&pvid=10_180.175.231.211_16330_1474465126259
替换结果：
http://uland.taobao.com/coupon/edetail?activityId=e73a59933f72481cb2873ce427db3fa4&pid=mm_89785546_8246652_27920024&itemId=535476074530&src= pgy_pgyqf &dx=1
dx：是否强制定向（选填），决定了商品的结算佣金；当输入dx=1时，按当前pid报名通过的定向计划佣金进行结算，如果没有定向计划按通用佣金结算；当未输入时，则首先在鹊桥里寻找该商品，如果存在则按鹊桥结算；如果不存在则寻找定向计划按定向计划的佣金结算，如果均不存在则按通用佣金结算；
2、商品id和优惠券id要输入正确，且必须对应同一个卖家，否则页面出不来；为了保证您的收益，将跳转到爱淘宝（用户在爱淘宝的成交会为您结算佣金）；
1143、优惠券必须能够用于单件单品上，即商品价格大于券的门槛，否则页面出不来；为了保证您的收益，将跳转到爱淘宝（用户在爱淘宝的成交会为您结算佣金）
4、当优惠券已发完时，消费者无法领券，但通过页面产生的购买依然会为您结算佣金；
"""
class coupon(object):
    """
        抓取淘鹊桥的优惠券
    """
    def __init__(self):
        pid = 'mm_68069173_42144173_248444921'
        pidt = 'mm_68069173_42144173_335908011'
        couponlink = 'https://uland.taobao.com/quan/detail?sellerId=2644898190&activityId=71b69c3c0377453098e2ae8faf29a5a8'
        queqiaolink = 'http://quan.meiquan8.com/index.php?mod=quan&act=index&iid=535058964256'
        activityid = '71b69c3c0377453098e2ae8faf29a5a8'
        itemid = '535058964256'
        link = 'http://uland.taobao.com/coupon/edetail?activityId=%s&pid=%s&itemId=%s&src=pgy_pgyqf&dx=1' % (activityid, pid, itemid)
        link = 'http://uland.taobao.com/coupon/edetail?activityId=%s&pid=%s&itemId=%s' % (activityid, pidt, itemid)
    def get_meiquan8(self, fromurl):
        """
            抓取淘鹊桥首页优惠券直播的优惠券，传入url，单页抓取。一页50个。6900137506243
        """
        import requests
        from bs4 import BeautifulSoup as bs
        import time
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
        # 优惠券直播
        tmp = requests.get(fromurl, headers=header, timeout=10)
        time.sleep(5)
        result = []
        tmp = bs(tmp.content, 'html5lib')
        tmp = tmp.body.find('div', class_='media-list')
        tmp = tmp.find_all('div', class_='media-list-item-top')
        for item in tmp:
            coupon = item.find('div', class_='v2-list-coupon-online').a.get('href')
            itemlink = item.find('div', class_='v2-list-btm-btn media-one-key-box').a.get('href')
            r = {
                'meiquanurl':item.find('div', class_='media-list-img-box').find('a', class_='media-list-goods-url').get('href'),
                'img':item.find('img', class_='lazy media-list-img common-xCtJ-count').get('data-original'),
                'title':item.find('div', class_='media-list-copy-writing').text.replace('\n', '').replace(' ',''),
                'coupon':coupon,
                'par':item.find('div', class_='v2-list-coupon-online').a.div.text.replace('\n', '').replace(' ',''),
                'price':item.find('div', class_='media-list-price').find('span', class_='media-list-price-num num-font').text.replace('\n', '').replace(' ',''),
                'commision':item.find('div', class_='media-list-price').find('div', class_='fr online').text.split()[0],
                'volume':item.find('div', class_='v2-list-icons-group').div.text.split('：')[1],
                'tag':[i.get('data-txt') for i in item.find('div', class_='v2-list-icons-group').find_all('span')],
                'itemlink':itemlink,
                'activityId':coupon[coupon.rfind('activityId=')+11:coupon.rfind('activityId=')+43] if coupon.rfind('activityId') > 0 else False,
                'itemid':itemlink[itemlink.rfind('id=')+3:],
            }
            result.append(r)
        return result

if __name__ == '__main__':
    import time
    result = []
    s = coupon()
    for page_no in range(100, 200):
        fromurl = 'http://quan.meiquan8.com/index.php?mod=index&type=all&cid=0&q=&commission=0&volume=0&price_start=0&price_end=0&sort=0&tmall=0&only=1&jr_update=0&jr_insert=0&from=0&table=goods&page=%d' % page_no
        while True:
            try:
                print(fromurl)
                result.extend(s.get_meiquan8(fromurl))
                break
            except Exception as e:
                print(e)
                time.sleep(20)
        time.sleep(5)


https://uland.taobao.com/coupon/edetail?e=TZxwuBR3Ti9D3FSiAPfS1GH2YkJV00u5RcbFYlghJ%2FLR1t2cMePXZmSlkL8%2BFO6J3ZdF3efaSglyWF3lujVbh8KUixUTTLeu7sRUcQe1PUddLMRHm4Jhh7MA9kLIn%2FM%2BmzSBSNjtLDgDF4IlGYL%2FgE0SZyu8unOR&af=1&pid=

https://uland.taobao.com/coupon/edetail?e=Nilc3JiO1%2FhD3FSiAPfS1GH2YkJV00u5RcbFYlghJ%2FLR1t2cMePXZmSlkL8%2BFO6J%2FPtCAXaCGCJlgC0K%2FW1jL8KUixUTTLeu7sRUcQe1PUddLMRHm4Jhh7MA9kLIn%2FM%2BKFqhjoFmq7GiowOwDtQ3T1lkTalpaJyM&af=1&pid=mm_68069173_42144173_335908011
https://uland.taobao.com/coupon/edetail?e=lBSnW3IFLmFD3FSiAPfS1GH2YkJV00u5RcbFYlghJ%2FLR1t2cMePXZmSlkL8%2BFO6J73nb2P6sa%2BwyQZusIDeLr8KUixUTTLeu7sRUcQe1PUddLMRHm4Jhh7MA9kLIn%2FM%2BKFqhjoFmq7GiowOwDtQ3T1lkTalpaJyM&af=1&pid=mm_68069173_42144173_248444921
https://uland.taobao.com/coupon/edetail?e=G7%2FBAhTPu%2BtD3FSiAPfS1GH2YkJV00u5RcbFYlghJ%2FLR1t2cMePXZmSlkL8%2BFO6J%2FPtCAXaCGCIsv87OBN6VV8KUixUTTLeu7sRUcQe1PUddLMRHm4Jhh7MA9kLIn%2FM%2BKFqhjoFmq7GiowOwDtQ3T1lkTalpaJyM&af=1&pid=mm_68069173_42144173_248444921
https://uland.taobao.com/coupon/edetail?e=Y%2BXdDSXW%2BIdD3FSiAPfS1GH2YkJV00u5RcbFYlghJ%2FLR1t2cMePXZmSlkL8%2BFO6JmEv94ne6mMr1Ylvf2zoUgsKUixUTTLeu7sRUcQe1PUddLMRHm4Jhh7MA9kLIn%2FM%2BpeBUFuuwLH8iQWYQbNyYz%2FEddtGrPfzxonv6QcvcARY%3D&af=1&pid=mm_68069173_42144173_335908011
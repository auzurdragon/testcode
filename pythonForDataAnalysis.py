# 0723：来自bit.ly的1.usa.gov数据，
path = 'http://bit.ly/ch02/usagov_bitly_data2012-03-16-1331923249.txt'

import pymongo
from urllib.parse import quote_plus

conn = pymongo.MongoClient(host='112.74.161.9', port=28010)
conn.BJDdb.authenticate('writeuser','51write')
db = conn.BJDdb
coll = db.BJD_User

rec = [i for i in coll.find(limit=100)] # 从数据库中取出100条用户记录

conn.close()

# 按nativename分组计数
t_nativename = [i['nativename'] for i in rec]
def get_counts(sequence):
    """基础计数方法"""
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

def get_counts(sequence):
    """使用defaultdict进行计数"""
    counts = defaultdict(int)  # 所有值初始化为0
    for x in sequence:
        counts[x] += 1
    return dict(counts)

def get_counts(sequence):
    """使用collections.Counter进行计数"""
    from collections import Counter
    t = Counter(sequence)
    print (dict(t))
    print (t.most_common(10))  # 打印top10
    return t
# 
"""
    《Python for Data Analysis》，作者：Wes McKinney
    数据源：http://www.grouplens.org/node , MovieLens用户提供的电影评分数据
"""

import pymongo
conn = pymongo.MongoClient(host='112.74.161.9', port=28010)
conn.mydata.authenticate('writeuser','51write')
try:
    db = conn.mydata
    coll = db.ml_ratings
except expression as identifier:
    print(identifier)

db = conn.BJDdb
coll = db.BJD_User
rec = [i for i in coll.find(limit=500, sort=[('_id', pymongo.DESCENDING),])] # 从数据库中取出最后的500条用户记录
conn.close()

def conn_alimongo(dbname='STUdb', collname='ml1m_users'):
    """连接MongoDB数据库"""
    import pymongo
    conn = pymongo.MongoClient(host='112.74.161.9', port=28010)
    db = conn.get_database(dbname)
    if db.authenticate('writeuser', '51write'):
        coll = db.get_collection(collname)
        return coll
    else:
        print ('db.authenticate() : false! ')

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

def get_counts(sequence,countfield):
    """使用pandas.DataFrame的数据框处理方法进行计数"""
    from pandas import DataFrame
    from matplotlib import pyplot as plt
    frame = DataFrame(sequence) # 将数据对象转换为DataFrame数据框
    t = frame[countfield].value_counts() # 使用value_counts()方法计数
    print(t[:10])   # 打印出TOP10
    t[:10].plot(kind='barh', rot=0) # 对TOP10生成绘图对象，横向条形图
    plt.show()   # 使用matplotlib绘图
    return t

def get_movielens(dpath, dname):
    """使用pandas.read_table()读取数据"""
    import pandas as pd
    t = pd.read_table(dpath, sep='::', header=None, names=dname)
    return t

def get_pivot(dataObj,valuesVar, indexVar, columnsVar, aggfunc):
    """
        使用pandas.pivot_table()对dataObj进行分类汇总
        valuesVar-需要汇总的变量,
        indexVar-行分类变量,
        columnsVar-列分类变量,
        aggfunc-汇总函数
        返回结果为pandas对象
    """
    import pandas
    t = dataObj.pivot_table(valuesVar, index=indexVar, columns=columnsVar, aggfunc=aggfunc)
    return t

# 将dataFrame转存入MongoDB
def to_mongodb(dataname, mongohost='localhost', mongoport=28010, dbname='mydata', collname)
    """
    """
    import pandas as pd
    from pymongo import MongoClient
    tmp = json.loads(ratings.T.to_json())
    insertlist = []
    for i in range(len(tmp)):
        insertlist.append(tmp.popitem()[1])
    
    conn = MongoClient(host=mongohost, port=mongoport)
    db = conn.get_database(dbname)
    coll = db.get_collection(collname)
    coll.insert_many(insertlist)

datapath = 'E:/MyDownload/ml-1m/users.dat'
datanames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = get_movielens(datapath, datanames)

datapath = 'E:/MyDownload/ml-1m/ratings.dat'
datanames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = get_movielens(datapath, datanames)
datapath = 'E:/MyDownload/ml-1m/movies.dat'
datanames = ['movie_id', 'title', 'genres']
movies = get_movielens(datapath, datanames)

to_mongodb(users,collname='ml_users')
to_mongodb(ratings,collname='ml_ratings')
to_mongodb(movies,collname='ml_movies')

# 使用pd.merge()合并数据框
sdata = pd.merge(pd.merge(ratings, users), movies)
# 建立数据透视表
mean_ratings = get_pivot(sdata, 'rating', 'title', 'gender', 'mean')


#coding:utf-8

# 读取数据集
import pandas as pd
# 读取用户数据，年龄和职业是编码格式，编码含义见readme
unames = ["user_id", "gender", "age", "occupation", "zip"]
users = pd.read_table("d:/mydb/testdb/MovieLens/ml-1m/users.dat", sep="::", header=None, names=unames)
rnames = ["user_id", "movie_id", "rating", "timestamp"]
ratings = pd.read_table("d:/mydb/testdb/MovieLens/ml-1m/ratings.dat", sep="::", header=None, names=rnames)
mnames = ["movie_id", "title", "genres"]
movies = pd.read_table("d:/mydb/testdb/MovieLens/ml-1m/movies.dat", sep="::", header=None, names=mnames)

import pickle
writer = open("pandas/users.dat", "wb")
pickle.dump(users, writer)
writer.close()
writer = open("pandas/ratings.dat", "wb")
pickle.dump(ratings, writer)
writer.close()
writer = open("pandas/movies.dat", "wb")
pickle.dump(movies, writer)
writer.close()

reader = open("pandas/users.dat", "rb")
users = pickle.load(reader)
reader.close()
reader = open("pandas/ratings.dat", "rb")
ratings = pickle.load(reader)
reader.close()
reader = open("pandas/movies.dat", "rb")
movies = pickle.load(reader)
reader.close()

# 合并数据集, merge(data1,data2), 自动按照列名的重叠情况判断合并键
data = pd.merge(pd.merge(ratings, users), movies)

# pivot_table(values=None, index=None,columns=None, aggfunc="mean"), 透视表
# 按性别计算每部电影的分, values-汇总的值，index-分组值， columns-分类值, aggfunc-汇总方法
mean_ratings = data.pivot_table(values="rating", index="title", columns="gender", aggfunc="mean")

# groupby(), 分组，size()，计数
ratings_by_title = data.groupby("title").size()

# 筛选评价数量大于250条的电影名称
active_titles = ratings_by_title.index[ratings_by_title >= 250]

# 排序出女性观众最喜欢的电影
top_female_ratings = mean_ratings.sort_values(by="F", ascending=False)

# 计算男女性平均评分的差异
mean_ratings["diff"] = mean_ratings["M"] - mean_ratings["F"]

# 计算出评分差异最大的电影，即求标准差.std()
ratings_std_by_title = data.groupby("title")["rating"].std()  # 求各电影的评价标准差
ratings_std_by_title = ratings_std_by_title.ix[active_titles]  # 筛选评价数量大于250条
ratings_std_by_title.sor_values(ascending=False)[:10]
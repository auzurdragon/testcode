# 利用Python进行数据分析
## 书籍信息
Wes McKinney, oreilly.com.cn, ISBN 978-7-111-43673-7
http://www.usa.gov/about/developer-resources/lusagov.shtml

## 保存示例数据
```Python
from pymongo import MongoClient
import pickle
client = MongoClient("localhost", 28010)
conn = client.mydata.ml_users
ml_users = conn.find({},{"_id":0, "user_id":1, "gender":1, "age":1, "occupation":1, "zip":1})
ml_users = list(ml_users)
opener = open("PythonForDataAnalysis/ml_users.pkl", "wb")
pickle.dump(ml_users, opener)
opener.close()
```

## 示例
```Python
def get_data(self):
"""还原示例数据"""
import pickle
数据格式示例
ml_users = [{
    # "user_id":"",   # userid
    # "gender":"F",   # 性别
    # "age":int(35),   # 年龄
    # "occupation":int(20),   # 职业
    # "zip":"60440",  # 邮编
}]
opener = open("PythonForDataAnalysis/ml_users.pkl", "rb")
ml_users = pickle.load(opener)
opener.close()
return self.ml_users

# 对zip邮编排序，求数量最多的10个zip
ml_users = get_data()
def top_zip(self):
    zip = [i["zip"] for i in ml_users]
    
# 
```

## 对zip邮编排序，求数量最多的10个zip
```Python
ml_users = get_data()
```

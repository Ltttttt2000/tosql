import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 假设您的数据库连接字符串如下
import urllib.parse  # 用于URL编码

# 定义连接参数
username = "root"
password = "ltAb123456@"  # 密码中包含特殊字符
host = "localhost"
port = 3306
database = "august"

# 对密码进行URL编码
password_encoded = urllib.parse.quote_plus(password)

# 构建连接字符串
db_connection_str = f"mysql+mysqlconnector://{username}:{password_encoded}@{host}:{port}/{database}"

print(db_connection_str)
engine = create_engine(db_connection_str)

# 执行SQL查询
query = """
SELECT electrodeID, COUNT(sessionID) AS sessionCount
FROM session
GROUP BY electrodeID;
"""
df = pd.read_sql_query(query.strip(), engine)

print(df)
# 使用Matplotlib绘制图表
plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题
# 绘制柱状图
plt.figure(figsize=(10, 6))
bar_list = plt.bar(df['electrodeID'], df['sessionCount'])

# 在每个柱子上添加数值
for bar in bar_list:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval, 1), va='bottom') # va: vertical alignment



plt.xlabel('电极名称')
plt.ylabel('Session数量')
plt.title('不同电极session数量')
plt.xticks(ticks=range(len(df)), labels=df['electrodeID'], rotation=90)
plt.tight_layout()
plt.show()

# query2 = """
# select type, COUNT(sessionID) AS sessionCOUNT
# FROM session, electrode
# where session.electrodeID=electrode.name
# group by type;
# """
#
# print(query2)
# df2 = pd.read_sql_query(query2.strip(), engine)
#
# print(df2)
# # 使用Matplotlib绘制图表
# plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
# plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题
# # 绘制柱状图
# plt.figure(figsize=(10, 6))
# bar_list = plt.bar(df2['type'], df2['sessionCOUNT'])
#
# # 在每个柱子上添加数值
# for bar in bar_list:
#     yval = bar.get_height()
#     plt.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval, 1), va='bottom') # va: vertical alignment
#
#
#
# plt.xlabel('电极名称')
# plt.ylabel('Session数量')
# plt.title('不同电极的session数量')
# plt.xticks(ticks=range(len(df2)), labels=df2['type'], rotation=90)
# plt.tight_layout()
# plt.show()
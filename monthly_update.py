

import pymysql.cursors
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='ltAb123456@',
    database='august',
)

cursor = conn.cursor()
cursor.execute('use august;')

print('开始查询......')

# 不同实验类型及其对应的Session数量
experiment_types = ['临床项目', '临床实验个数', '临床实验session个数', '动物实验项目', '动物实验个数', '动物实验session个数',
                    '电生理数据个数', '小鼠实验', '大鼠实验', '猴子实验', 'Spike数据', 'ECoG数据']
counts = []

data_type = ['动物ECoG', '动物Spike', '临床ECoG']
data_type_counts = []



cursor.execute("select count(distinct project_number)  AS '临床项目' from clinic;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(clinicID) AS '临床实验个数' from clinic;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(sessionID) AS '临床实验session个数' from session where clinicID is not null;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(distinct project_number)  AS '动物实验项目' from experiment;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(experimentID) AS '动物实验个数' from experiment;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(sessionID) AS '动物实验session个数' from session where experimentID is not null;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)


cursor.execute("select count(sessionID) AS '电生理数据个数' from session where left(file_type,1) =1;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(sessionID) AS '小鼠实验session个数' from session s, animal a where s.animalID=a.animalID and a.species='小鼠';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(sessionID) AS '大鼠实验session个数' from session s, animal a where s.animalID=a.animalID and a.species='大鼠';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(sessionID) AS '猴子实验session个数' from session s, animal a where s.animalID=a.animalID and a.species='猕猴';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(sessionID) AS 'spike数据session个数' from session where signal_type='Spike';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)

cursor.execute("select count(sessionID) AS 'ECoG数据session个数' from session where signal_type='ECoG';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
counts.append(result)


cursor.execute("select count(sessionID) AS '动物ECoG数据' from session where signal_type='ECoG' and experimentID IS NOT NULL;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
data_type_counts.append(result)

cursor.execute("select count(sessionID) AS '动物Spike数据' from session where signal_type='Spike' and experimentID IS NOT NULL;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
data_type_counts.append(result)

cursor.execute("select count(sessionID) AS '临床ECoG数据' from session where signal_type='ECoG' and experimentID IS NULL;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)
data_type_counts.append(result)

conn.commit()
conn.close()

print("Finished.... Check the database :)")




import pandas as pd
import matplotlib.pyplot as plt

# 绘制柱状图
plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题

# 绘制饼图
labels = ['小鼠实验', '大鼠实验', '猴子实验']
sizes = [counts[7], counts[8], counts[9]]
plt.figure()
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('不同动物种类实验Session个数比例')
plt.show()



# 创建柱状图

# plt.bar(data_type, data_type_counts)
fig, ax = plt.subplots()   # figsize=(10, 6)
bar_container = ax.bar(data_type, data_type_counts)

# 在柱状图上添加数值
for bar in bar_container:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 5, round(yval, 1), ha='center', va='bottom')
# 添加标题和标签
plt.title('不同实验类型的Session数量')
plt.xlabel('实验类型')
plt.ylabel('Session数量')



# 显示图表
plt.show()
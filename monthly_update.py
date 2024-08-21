

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


cursor.execute("select count(distinct project_number)  AS '临床项目' from clinic;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(clinicID) AS '临床实验个数' from clinic;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(sessionID) AS '临床实验session个数' from session where clinicID is not null;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(distinct project_number)  AS '动物实验项目' from experiment;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(experimentID) AS '动物实验个数' from experiment;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(sessionID) AS '动物实验session个数' from session where experimentID is not null;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)


cursor.execute("select count(sessionID) AS '电生理数据个数' from session where left(file_type,1) =1;")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(sessionID) AS '小鼠实验session个数' from session s, animal a where s.animalID=a.animalID and a.species='小鼠';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(sessionID) AS '大鼠实验session个数' from session s, animal a where s.animalID=a.animalID and a.species='大鼠';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(sessionID) AS '猴子实验session个数' from session s, animal a where s.animalID=a.animalID and a.species='猕猴';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(sessionID) AS 'spike数据session个数' from session where signal_type='Spike';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

cursor.execute("select count(sessionID) AS 'ECoG数据session个数' from session where signal_type='ECoG';")
result = cursor.fetchall()[0][0]
name = cursor.description[0][0]
print(name + ": ", result)

conn.commit()
conn.close()

print("Finished.... Check the database :)")
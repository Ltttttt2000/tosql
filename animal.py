import json
from datetime import datetime

import pandas as pd
from pymysql import NULL

path = 'D:/DATA/HE05/HE05.xlsx'


print("Start reading the data survey form ... ")
df = pd.read_excel(path) # skiprows=2，不需要跳过任何行，第一行就是表头
to_sql = []
IDs = []
for index, row in df.iterrows():
    if row['动物ID'] not in IDs:
        animal_name = row['动物ID']
        species = row['动物种类']
        strains = row[('动物品系')]


        age = None
        if pd.isna(row['动物周龄']) is False:
            age = row[('动物周龄')]


        gender = None
        if pd.isna(row['动物性别']) is False:
            gender = row['动物性别']

        weight = None
        if pd.isna(row['动物体重']) is False:
            weight = row['动物体重']


        values = (animal_name, species, strains, age, gender, weight)
        IDs.append(animal_name)

        if values not in to_sql:
            to_sql.append(values)

print(to_sql)
'''存入数据库'''
import pymysql.cursors
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='ltAb123456@',
    database='june',
)

cursor = conn.cursor()
cursor.execute('use june;')

sql = 'INSERT INTO animal (name, species, strains, age, weight, gender) VALUES (%s, %s, %s, %s, %s, %s)'
for values in to_sql:
    print(values)
    ''' remove comments while enter database '''
    cursor.execute(sql, values)

conn.commit()
conn.close()

print("Finished.... Check the database :)")
import json
from datetime import datetime

import pandas as pd
from pymysql import NULL

path = r'D:\DATA\NC_2023_A_02.xlsx'
dtype = {
    '动物出生日期': str,
    '动物体重': float
}

print("Start reading the data survey form ... ")
df = pd.read_excel(path, dtype=dtype) # skiprows=2，不需要跳过任何行，第一行就是表头
to_sql = []
IDs = []
for index, row in df.iterrows():
    if row['动物ID'] not in IDs:
        animal_name = row['动物ID']
        species = row['动物种类'] if pd.isna(row['动物种类']) is False else None
        strains = row[('动物品系')] if pd.isna(row['动物品系']) is False else None


        dob = None
        if pd.isna(row['动物出生日期']) is False:
            tmp = row['动物出生日期']
            year = tmp[0:4]
            month = tmp[4:6]
            day = tmp[6:8]

            dob = str(year) + '-' + str(month) + '-' + str(day)


        gender = None
        if pd.isna(row['动物性别']) is False:
            gender = row['动物性别']

        weight = None
        if pd.isna(row['动物体重']) is False:
            weight = row['动物体重']


        values = (animal_name, species, strains, dob, gender, weight)

        if values not in to_sql:
            to_sql.append(values)

print(to_sql)
# '''存入数据库'''
import pymysql.cursors
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='ltAb123456@',
    database='august',
)

cursor = conn.cursor()

sql = 'INSERT INTO animal (name, species, strains, DOB, gender, weight) VALUES (%s, %s, %s, %s, %s, %s)'
for values in to_sql:
    print(values)
    ''' remove comments while enter database '''
    cursor.execute(sql, values)

conn.commit()
conn.close()

print("Finished.... Check the database :)")
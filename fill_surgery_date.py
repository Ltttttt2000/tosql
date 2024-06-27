'''
对应上小鼠的植入日期，植入脑区和植入深度 到invasive_json
三个字段全存成字符串

深度是mm

'''



import json
from datetime import datetime

import pandas as pd
from pymysql import NULL

path = 'C:/Users/Lenovo/Downloads/animal.xlsx'


print("Start reading the data survey form ... ")
df = pd.read_excel(path) # skiprows=2，不需要跳过任何行，第一行就是表头

to_sql = []
for index, row in df.iterrows():




    if pd.isna(row['植入日期']) is False:
        surgety_date = row['植入日期']
    else:
        surgety_date = None

    if pd.isna(row['植入脑区']) is False:
        naoqu = row['植入脑区']
    else:
        naoqu = None

    if pd.isna(row['植入深度']) is False:
        depth = row['植入深度']
    else:
        depth = None

    invasive_dic = {
        "date": surgety_date,
        "region": naoqu,
        "depth": depth
    }
    # 1. json.dumps(字典)：将字典转为JSON字符串，indent为多行缩进空格数，
    # sort_keys为是否按键排序,ensure_ascii=False为不确保ascii，及不将中文等特殊字符转为\uXXX等
    invasive_json = json.dumps(invasive_dic, ensure_ascii=False)


    animal_name = row['动物ID']

    value = (invasive_json, animal_name)
    to_sql.append(value)

import pymysql.cursors
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='ltAb123456@',
    database='june',
)

cursor = conn.cursor()
cursor.execute('use june;')

sql = 'UPDATE animal SET invasive_json = %s WHERE name = %s'
for values in to_sql:
    print(values)
    ''' remove comments while enter database '''
    cursor.execute(sql, values)

conn.commit()
conn.close()

print("Finished.... Check the database :)")


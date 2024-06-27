"""
把session对应上所有的文件夹
以HE04为例子

"""
import json
from datetime import datetime

import pandas as pd
from pymysql import NULL

path = 'C:/Users/Lenovo/Downloads/HE04.xlsx'


print("Start reading the data survey form ... ")
df = pd.read_excel(path) # skiprows=2，不需要跳过任何行，第一行就是表头
to_sql = []
for index, row in df.iterrows():
    filename = row['文件名']
    animal_name = row['动物编号']
    project_number = row[('项目编号')]
    experiment_name = row['实验名称']
    # print(row['开始日期'])
    '''对时间的一些处理'''



    if str(row['开始日期']) != 'nan':

        year = str(int(row['开始日期']))[0:4]
        month = str(int(row['开始日期']))[4:6]
        day = str(int(row['开始日期']))[6:8]
        # print(year, month, day)

        t = str(row['开始时间'])
        # print(t)''
        if t != 'nan':
            start_time = str(year)+'-'+str(month)+'-'+str(day)+' '+t
        else:
            start_time = str(year)+'-'+str(month)+'-'+str(day)+' '+ '00:00:00'
        # print(start_time)

        if str(row['duration']) != 'nan':
            duration = row['duration']
        else:
            duration = None
        electrodeID = row['使用电极']

        '''整理JSON字段'''


        signal_type = row['信号类型']
        system = row['采集系统']
        sample_rate = row['sample_rate']
        if pd.isna(row['channel_count']) is False:
            channel_count = int(row['channel_count'])
        else:
            channel_count = None
        paradigm = str(row['范式'])
        electrophysiology_dic = {
            "signal_type": signal_type,
            "system": system,
            "sample_rate": sample_rate,
            "channel_count": channel_count,
            "paradigm": paradigm
        }
        # 1. json.dumps(字典)：将字典转为JSON字符串，indent为多行缩进空格数，
        # sort_keys为是否按键排序,ensure_ascii=False为不确保ascii，及不将中文等特殊字符转为\uXXX等
        electrophysiology_json = json.dumps(electrophysiology_dic, ensure_ascii=False)


        if str(row['行为学软件']) != 'nan':
            software = row['行为学软件']
            behavior_dic = {
                'software': software
            }
            behavior_json = json.dumps(behavior_dic, ensure_ascii=False)
        else:
            behavior_json = json.dumps('')


        file_type = row['file_type']


        path =  project_number + '/' + experiment_name + '/' + filename
        values = (electrodeID, start_time, duration, electrophysiology_json, behavior_json, file_type, path, animal_name, project_number, experiment_name)
        to_sql.append(values)



import pymysql.cursors
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='ltAb123456@',
    database='june',
)

cursor = conn.cursor()
cursor.execute('use june;')

sql = 'INSERT INTO session (electrodeID, start_time, duration, electrophysiology_json, behavior_json, file_type, path,animal_name, project_number, experiment_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
for values in to_sql:
    print(values)
    ''' remove comments while enter database '''
    cursor.execute(sql, values)

conn.commit()
conn.close()

print("Finished.... Check the database :)")
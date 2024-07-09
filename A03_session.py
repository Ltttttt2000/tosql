"""
把session对应上所有的文件夹
以HE04为例子

"""
import json
from datetime import datetime

import pandas as pd
from pymysql import NULL

path = 'D:/DATA/A03/A03.xlsx'


print("Start reading the data survey form ... ")
df = pd.read_excel(path) # skiprows=2，不需要跳过任何行，第一行就是表头
to_sql = []
for index, row in df.iterrows():
    file = str(row['文件夹名'])[0:4] + '_' + str(row['文件夹名'])[4:6] + '_' + str(row['文件夹名'])[6:9]
    filename = 'CIBR' + row['动物ID'].split('-')[1] + '_' + file
    print(filename)

    animal_name = row['动物ID']
    project_number = row[('项目编号')]
    experiment_name = row['实验名称']
    # print(row['开始日期'])
    '''对时间的一些处理'''

    start_time = row['开始时间']
    electrodeID = row['电极名称']

    '''整理JSON字段'''
    signal_type = row['信号类型']
    system = row['采集系统']
    sample_rate = row['采样率']
    if pd.isna(row['通道量']) is False:
        channel_count = int(row['通道量'])
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

    electrophysiology_json = json.dumps(electrophysiology_dic, ensure_ascii=False)
    '''忘了补充'''
    record_way = row['急性/慢性']

    if pd.isna(row['电极植入日期']) is False:
        surgety_date = row['电极植入日期']
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

    path = project_number + '/' + experiment_name + '/' + filename
    experimentID = 3
    values = (experimentID, electrodeID, start_time, electrophysiology_json, invasive_json, '10001001', path, animal_name, project_number, experiment_name)
    print(values)
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

sql = 'INSERT INTO session (experimentID, electrodeID, start_time, electrophysiology_json, invasive_json, file_type, path, animal_name, project_number, experiment_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
for values in to_sql:
    print(values)
    ''' remove comments while enter database '''
    cursor.execute(sql, values)

conn.commit()
conn.close()

print("Finished.... Check the database :)")
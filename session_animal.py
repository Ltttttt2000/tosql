"""
把session对应上所有的文件夹
以HE04为例子

表头 项目编号	实验名称	动物ID	文件夹名	电极名称	动物种类	动物品系	动物周龄	动物性别	动物体重	记录状态	电极植入日期	植入脑区	植入深度	开始时间	持续时间	采样率	通道量	采集系统	范式	信号类型

"""
import json
from datetime import datetime

import pandas as pd
from pymysql import NULL


print('请输入该实验所涉及的JSON类型（共5个）：电生理信号采集、行为学、侵入式、刺激、麻醉，若含有该类型为1，不含有为0，例如：10110')
type = input()
print(type[0])
path = 'D:\\DATA\\C02\\C02.xlsx'


print("Start reading the data survey form ... ")
df = pd.read_excel(path) # skiprows=2，不需要跳过任何行，第一行就是表头
to_sql = []

for index, row in df.iterrows():
    project_number = str(row[('项目编号')])
    experiment_name = str(row['实验名称'])

    animal_name = row['动物ID']

    filename = str(row['文件夹名'])
    electrodeID = row['电极名称']

    if pd.isna(row['记录状态']) is False:
        record_way = row['记录状态']
    else: record_way = None

    if pd.isna(row['开始时间']) is False:
        start_time = row['开始时间']
    else: start_time = None

    if pd.isna(row['持续时间']) is False:
        duration = row['持续时间']
    else: duration = None



    electrodeID = row['电极名称']



    # '''对时间的一些处理'''
    # if str(row['开始日期']) != 'nan':
    #
    #     year = str(int(row['开始日期']))[0:4]
    #     month = str(int(row['开始日期']))[4:6]
    #     day = str(int(row['开始日期']))[6:8]
    #     # print(year, month, day)
    #
    #     t = str(row['开始时间'])
    #     # print(t)''
    #     if t != 'nan':
    #         start_time = str(year)+'-'+str(month)+'-'+str(day)+' '+t
    #     else:
    #         start_time = str(year)+'-'+str(month)+'-'+str(day)+' '+ '00:00:00'
    #     # print(start_time)
    #
    #     if str(row['duration']) != 'nan':
    #         duration = row['duration']
    #     else:
    #         duration = None

    '''电生理信号采集实验'''
    if type[0] == '1':
        signal_type = row['信号类型']
        system = row['采集系统']
        sample_rate = row['采样率']
        if pd.isna(row['通道量']) is False:
            channel_count = int(row['通道量'])
        else:
            channel_count = None

        if pd.isna(row['范式']) is False:
            paradigm = str(row['范式'])
        else: paradigm = None

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
    else: electrophysiology_json = None



    '''整理JSON字段：以下是根据'''
    '''侵入式的'''
    if type[2] == '1':
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
    else: invasive_json = None





    '''行为学记录'''
    if type[1] == '1':
        software = row['行为学软件']
        behavior_dic = {
            'software': software
        }
        behavior_json = json.dumps(behavior_dic, ensure_ascii=False)
    else: behavior_json = None


    if type[2] == '1':
        stimus_dic = {
            # 'stimus_type': row['刺激类型']
        }
        stimus_json = json.dumps(stimus_dic, ensure_ascii=False)
    else: stimus_json = None


    if type[3] == '1':
        others_dic = {
            # 'anaesthesia_type': row['麻醉类型']
        }
        others_json = json.dumps(others_dic, ensure_ascii=False)
    else: others_json = None


    path = project_number + '/' + experiment_name + '/' + filename
    # print(project_number, experiment_name, electrodeID, start_time, duration, record_way, electrophysiology_json, behavior_json, stimus_json, invasive_json, others_json, path, animal_name)



    values = (project_number, experiment_name, electrodeID, start_time, duration, record_way, electrophysiology_json, behavior_json, stimus_json, invasive_json, others_json, path, animal_name)

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

sql = 'INSERT INTO session (project_number, experiment_name, electrodeID, start_time, duration, record_way, electrophysiology_json, behavior_json, stimus_json, invasive_json, others_json, path, animal_name)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
for values in to_sql:
    print(values)
    ''' remove comments while enter database '''
    cursor.execute(sql, values)

conn.commit()
conn.close()

print("Finished.... Check the database :)")
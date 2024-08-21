"""
把session对应上所有的文件夹
以HE04为例子

表头 项目编号	实验名称	患者ID	文件夹名	电极名称	姓名	性别	出生年份	病症	 记录状态 电极植入日期	植入脑区	植入深度	开始时间	持续时间	采样率	通道量	采集系统	范式	信号类型

"""
import json
from datetime import datetime

import pandas as pd
from pymysql import NULL
import re


path = r'D:\DATA\NC_2023_C_02.xlsx'
project_number = 'NC_2023_C_02'

dtype = {
    'filetype': str,
    '开始时间': str
}
print("Start reading the data survey form ... ")
df = pd.read_excel(path, dtype=dtype) # skiprows=2，不需要跳过任何行，第一行就是表头
to_sql = []

for index, row in df.iterrows():
    experiment_name = str(row['实验名称'])
    filename = str(row['文件夹名'])


    experimenter = str(row['患者ID'])
    electrodeID = row['电极名称']


    if pd.isna(row['记录状态']) is False:
        record_way = row['记录状态']
    else: record_way = None

    if pd.isna(row['开始时间']) is False:
        tmp = row['开始时间']
        year = tmp[6:10]
        month = tmp[3:5]
        day = tmp[0:2]

        t = tmp[11:]
        start_time = str(year)+'-'+str(month)+'-'+str(day)+' '+ t
        # print(start_time)
    else: start_time = None



    if pd.isna(row['持续时间']) is False:
        duration = row['持续时间']
    else: duration = None



    file_type = None
    if pd.isna(row['filetype']) is False:
        file_type = row['filetype']

    signal_type = row['信号类型']
    record_system = row['采集系统']
    sample_rate = row['采样率']
    if pd.isna(row['通道量']) is False:
        channel_count = int(row['通道量'])
    else:
        channel_count = None

    if pd.isna(row['范式']) is False:
        paradigm = str(row['范式'])
    else:
        paradigm = None

    if pd.isna(row['电极植入日期']) is False:
        invasive_date = row['电极植入日期']
    else:
        invasive_date = None

    if pd.isna(row['植入脑区']) is False:
        region = row['植入脑区']
    else:
        region = None

    if pd.isna(row['植入深度']) is False:
        depth = row['植入深度']
    else:
        depth = None

    location = row['实验地点'] if not pd.isna(row['实验地点']) else None
    sterilization = row['消毒方式'] if not pd.isna(row['消毒方式']) else None
    path = project_number + '/' + experiment_name + '/' + filename


    values = (project_number, experiment_name, electrodeID, start_time, duration, record_way, file_type, path, experimenter,
              sample_rate, record_system, paradigm, signal_type, channel_count, invasive_date, region, depth, location, sterilization)

    print(values)
    to_sql.append(values)

print(len(to_sql))

# import pymysql.cursors
# conn = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='ltAb123456@',
#     database='august',
# )
#
# cursor = conn.cursor()
#
#
# sql = ('INSERT INTO session (project_number, experiment_name, electrodeID, start_time, duration, record_way, file_type, path, experimenter,'
#        'sample_rate, record_system, paradigm, signal_type, channel_count, invasive_date, region, depth, location, sterilization)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
# for values in to_sql:
#     print(values)
#     ''' remove comments while enter database '''
#     cursor.execute(sql, values)
#
# conn.commit()
# conn.close()
#
# print("Finished.... Check the database :)")
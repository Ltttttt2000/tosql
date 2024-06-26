"""
把session对应上所有的

"""
from datetime import datetime

import pandas as pd
path = 'C:/Users/Lenovo/Downloads/HE04.xlsx'


print("Start reading the data survey form ... ")
df = pd.read_excel(path) # skiprows=2，不需要跳过任何行，第一行就是表头

values = []
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
        # print(t)'
        start_time = str(year)+'-'+str(month)+'-'+str(day)+' '+t
        # print(start_time)


        duration = row['duration']

        '''整理JSON字段'''


        signal_type = row['信号类型']
        system = row['采集系统']
        sample_rate = row['sample_rate']
        channel_count = row['channel_count']
        paradigm = row['范式']
        electrophysiology_json = {
            "signal_type": signal_type,
            "system": system,
            "sample_rate": sample_rate,
            "channel_count": channel_count,
            "paradigm": paradigm
        }

        if str(row['行为学软件']) != 'nan':
            software = row['行为学记录软件']
            behavior_json = {
                'software': software
            }
        else:
            behavior_json = ''


        path = '/zhangshuai/Rnd_data/' + project_number + '/' + experiment_name + '/' + filename
        sql = 'INSERT INTO session (start_time, duration, electrophysiology_json, behavior_json) VALUES (%s, %s, %s, %s)'
        values = (start_time, duration, electrophysiology_json, behavior_json)


"""
从飞书导出动物实验《项目数据调研表》后读取并存入MySQL数据库的过程
为了方便查询和存储，将中文的信息以英文字母的形式存储（详见mapping）

workflow:
1. 从飞书导出每个项目的数据调研表excel文件
2. Change path to where the Excel exists
3. Change skiprows代表从第几行读取（表头）
4. Open database in cmd: mysql -u root -p
5. Change connection settings (username, password, port)
6. Run experiment.py
7. Check the database
"""


import pandas as pd


path = r'C:\Users\Lenovo\Downloads\NC_2023_HE_04_数据调研表.xlsx'
print("Start reading the data survey form ... ")
dtype = {
    '实验目的': str
}

df = pd.read_excel(path, skiprows=0, dtype=dtype) # 从第三行读取，第三行是表头


''' mapping '''
data_type_mapping = {
    '电生理信号数据': 'E',
    '刺激模式数据': 'S',
    '行为学数据': 'B',
    '其他': 'O',
}

record_status_mapping = {
    '麻醉态': 'A',
    '清醒-任务态': 'T',
    '清醒-静息态': 'R'
}


contrast_type_mapping = {
    '无对照': 'N',
    '同期对照': 'C',
    '历史对照': 'H',
    '自身前后对照': 'S'
}


experiment_sql = []    # 存储sql语句values

# 一行一行的处理excel文件，全都是选择，不考虑为空的情况
for index, row in df.iterrows():
    # print(pd.isna(row['研究类型'])) # 判断是否为nan，在pandas里nan是float类型
    project_number = row['项目编号'].strip()
    experiment_name = row['实验名称'].strip()

    # 多选：实验数据类型
    value = row['实验数据类型'].split(',')
    aim = row['实验目的'] if not pd.isna(row['实验目的']) else None
    data_type = ''
    for i in range(len(value)):
        extend = data_type_mapping.get(value[i])
        data_type = data_type + extend

    # 清醒态还是麻醉态
    value2 = row['记录状态'].split(',')
    record_status = ''
    for j in range(len(value2)):
        record_status += record_status_mapping.get(value2[j])

    record_way = row['记录方式']
    contrast_type = contrast_type_mapping.get(row['对照类型（如有）'])

    notes = None  # 空值
    if pd.isna(row['备注']) is False:
        notes = row['备注']
    has_code = row['是否涉及数据处理']

    values = (project_number, experiment_name, aim, data_type, record_status, record_way, contrast_type, notes, has_code)
    experiment_sql.append(values)



# check the sql before import to database
print(experiment_sql)

''' 
two ways to import to sql
1. store every sql to an array, execute(sql)
2. store values into an array, use execute(sql, values)
 '''

import pymysql.cursors
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='ltAb123456@',
    database='august',
)

cursor = conn.cursor()

''' remove comments while enter database '''
# for sql in experiment_sql:
#     cursor.execute(sql)

sql = 'INSERT INTO experiment(project_number, experiment_name, aim, data_type, record_status, record_way, contrast_type, notes, has_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'


for values in experiment_sql:
    print(values)
    ''' remove comments while enter database '''
    cursor.execute(sql, values)

conn.commit()
conn.close()

print("Finished.... Check the database :)")
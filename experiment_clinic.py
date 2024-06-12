'''
从飞书导出数据调研表后读取并存入MySQL数据库的过程
为了方便查询和存储，将中文的信息以英文字母的形式存储（详见mapping）
'''
import pandas as pd
path = 'C:/Users/Lenovo/Downloads/data.xlsx'
df = pd.read_excel(path, skiprows=2) # 从第三行读取，第三行是表头


''' map '''
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

observational_mapping = {
    '前瞻性队列研究': 'prospective',
    '回顾性队列研究': 'retrospective',
    '双向队列': 'bidirectional',
    '病例对照研究': 'case-control',
    'case-only': 'case-only'
}
interventional_mapping = {
    '单臂实验': 'signle-arm',
    '平行组': 'parallel',
    '交叉设计': 'cross-over',
    '序贯设计': 'sequential',
    '析因设计': 'factorial',
}

record_way_mapping = {
    'N/A': 'N',
    '急性': 'A',
    '慢性': 'C'
}

contrast_type_mapping = {
    '无对照': 'N',
    '同期对照': 'C',
    '历史对照': 'H',
    '自身前后对照': 'S'
}


experiment_sql = []
clinic_sql = []
# 一行一行的处理excel文件
for index, row in df.iterrows():
    # print(pd.isna(row['研究类型'])) # 判断是否为nan，在pandas里nan是float类型
    if row['项目编号'] != 'nan':
        project_name = row['项目编号'].strip()
        experiment_name = row['实验名称'].strip()

        values = row['实验数据类型'].split(',')
        # print(values)
        data_type = ''
        for i in range(len(values)):
            extend = data_type_mapping.get(values[i])
            data_type = data_type + extend

        # print(data_type)

        record_status = record_status_mapping.get(row['记录状态'])

        # 临床实验
        study_type = row['研究类型']
        study_model = ''
        if row['Study Type'] == 'Observational' and row['Study Type'] != 'nan':
            study_model = 'O-' + observational_mapping.get(row['观察性研究模型'])
        elif row['Study Type'] == 'Interventional' and row['Study Type'] != 'nan':
            study_model = 'I-' + interventional_mapping.get(row['干预性研究模型'])

        record_time = row['记录时段']
        indications = row['适应病症']

        # 动物实验
        record_way = record_way_mapping.get(row['记录方式'])
        contrast_type = contrast_type_mapping.get(row['对照类型（如有）'])

    # clinic和experiment录入数据库

    if pd.isna(row['研究类型']) is True:
        print(index, project_name, experiment_name, data_type, record_status, record_way, contrast_type)
        sql = 'INSERT INTO experiment(project_number, experiment_name, data_type, record_status, record_way, contrast_type) VALUES ("'\
        + project_name + '", "' + experiment_name + '", "' + data_type + '", "' + record_status + '", "' + record_way + '", "' + contrast_type + '");'
        # print(sql)
        experiment_sql.append(sql)
    else:
        print(index, project_name, experiment_name, data_type, record_status, study_type, study_model, record_time, indications)

        sql = 'INSERT INTO clinic (project_number, experiment_name, data_type, record_status, study_type, study_model, record_time, indications) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        values = (project_name, experiment_name, data_type, record_status, study_type, study_model, record_time, indications)

        clinic_sql.append(values)

# 录入
# import mysql.connector
#
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password='ltAb123456@',
#     database="june"
# )
#
# # 创建一个游标对象来执行SQL语句
# cursor = conn.cursor()
# sql = ''
# cursor.execute(sql)
#
# result = cursor.fetchall()
# print(result)
# conn.close()


import pymysql.cursors
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='ltAb123456@',
    database='june',
)
cursor = conn.cursor()
# for sql in experiment_sql:
#     cursor.execute(sql)

sql = 'INSERT INTO clinic (project_number, experiment_name, data_type, record_status, study_type, study_model, record_time, indications) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

for values in clinic_sql:
    print(values)
    # cursor.execute(sql, values)

conn.commit()
conn.close()

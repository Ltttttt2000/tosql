import pandas as pd



path = r'D:\DATA\NC_2023_C_02.xlsx'
projectID = 'NC_2023_C_02'

print("Start reading the data survey form ... ")

# 读取时指定每列的数据类型
dtype = {
    'filetype(human)': str
}
df = pd.read_excel(path, dtype=dtype) # skiprows=2，不需要跳过任何行，第一行就是表头
to_sql = []



for index, row in df.iterrows():
    name = str(row['患者ID'])
    year_of_birth = None

    '''对出生年份进行时间漂移法，统一+5'''
    if pd.isna(row['出生年份']) is False:
        year_of_birth = int(row['出生年份']) + 5
    gender = None
    if pd.isna(row['性别']) is False:
        gender = row['性别']

    indication = None
    if pd.isna(row['病症']) is False:
        indication = row['病症']

    file_type = row['filetype(human)']

    path = projectID + '/' + name

    values = (name, year_of_birth, gender,indication, file_type, path)

    if values not in to_sql:
        to_sql.append(values)


print(to_sql)
print(len(to_sql))
for human in to_sql:
    print(human)

import pymysql.cursors
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='ltAb123456@',
    database='august',
)

cursor = conn.cursor()
# cursor.execute('use august;')

sql = 'INSERT INTO human (name, year_of_birth, gender, indication, file_type, path) VALUES (%s, %s, %s, %s, %s, %s)'
for values in to_sql:
    print(values)
    ''' remove comments while enter database '''
    cursor.execute(sql, values)

conn.commit()
conn.close()

print("Finished.... Check the database :)")
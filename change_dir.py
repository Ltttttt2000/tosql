import os

path = 'D:\\NC-2023-HE-04\\柔性电极动物实验数据\\NC-2023-HE-04\\大鼠的神经信号采集'
dir =  'D:\\NC-2023-HE-04\\柔性电极动物实验数据\\NC-2023-HE-04\\'
files = os.listdir(path)


'''Step 1: 批量新建文件夹， 新建完成后注释掉'''
# for file in files:
#     file_path = os.path.join(path, file)
#
#     if os.path.isfile(file_path):
#         print(file)
#         print(dir + file.split('.')[0])
#         os.mkdir(dir + file.split('.')[0])

''' Step 2: 批量移动文件到文件夹下，其他步骤注释掉'''
import shutil



for file in files:
    file_path = os.path.join(path, file)
    dir_path = dir + file.split('.')[0]

    print(file_path, dir_path)
    shutil.move(file_path, dir_path)

    # if os.path.isfile(file_path):
    #
    #     print(file)
    #     print()
    #     # os.mkdir(dir + file.split('.')[0])
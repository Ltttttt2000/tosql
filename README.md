
## MySQL元数据入库Workflow

飞书导出数据调研表为Excel



主要录入三个表：experiment, animal, session

Step 1: 录入experiment

运行Python文件experiment_clinic.py录入experiment和clinic两个表

Step 2: 录入animal

直接csv导入animal的相关信息，需要修改字段mapping，运行fill_surgery_date填写植入的相关信息

Step 3： 录入session

运行session录入相关字段，运行fill_session.sql进行相关字段的填充（实验信息收集表Excel，根据项目编号和实验名称对应到相关的experimentID和clinicID）

## MySQL元数据入库Workflow

飞书导出数据调研表为Excel

主要录入三个表：experiment/clinic, animal/human, session

## Step 1: 录入实验表

若为临床实验数据运行clinic.py录入clinic表

若为动物实验数据运行experiment.py录入experiment表

若该项目动物实验数据和临床实验数据都涉及，运行experiment_clinic.py录入experiment和clinic两个表


## Step 2: 录入实验个体信息

若为动物实验运行animal.py录入animal表

若为临床实验运行human.py录入human表

## Step 3： 录入session信息

运行session.py录入session

## Step 4: 补充relation

运行fill_session.sql


## Notes

若自增字段不连续，需要对数据库进行设置

```sql
SET @i=0;
UPDATE `tablename` SET `id`=(@i:=@i+1);
ALTER TABLE `tablename` AUTO_INCREMENT=0;
ALTER TABLE your_table AUTO_INCREMENT = 1;

```

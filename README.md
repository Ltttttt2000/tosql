
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

根据该实验所涉及的数据填写：'请输入该实验所涉及的JSON类型（共5个）：电生理信号采集、行为学、侵入式、刺激、麻醉，若含有该类型为1，不含有为0，例如：10110'

## Step 4: 补充relation

运行fill_session.sql

```sql
use june;

-- 通过项目编号和实验名称对应上 --
UPDATE session s, experiment e
SET s.experimentID = e.experimentID
WHERE s.project_number = e.project_number AND s.experiment_name = e.experiment_name;

-- 通过动物名字对应
UPDATE session s, animal a
SET s.animalID = a.animalID
WHERE s.animal_name = a.name;

-- 把动物的植入信息存到session
UPDATE session s, animal a
SET s.invasive_json = a.invasive_json
WHERE s.animalID = a.animalID;
```

## Notes

若自增字段不连续，需要对数据库进行设置

```sql
SET @i=0;
UPDATE `tablename` SET `id`=(@i:=@i+1);
ALTER TABLE `tablename` AUTO_INCREMENT=0;
ALTER TABLE your_table AUTO_INCREMENT = 1;

```

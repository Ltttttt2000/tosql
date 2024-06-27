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
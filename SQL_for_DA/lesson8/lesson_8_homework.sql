--task1  (lesson8)
-- oracle: https://leetcode.com/problems/department-top-three-salaries/
select 
    department
    , employee
    , salary
from
    (
        select 
            e.name as employee
            , d.name as department
            , e.salary
            , departmentid
            , dense_rank() over(partition by departmentid order by salary desc)  as num_row
        from 
            employee e
            join department d on e.departmentid = d.id
    )
where 
    num_row <= 3
order by 
    departmentid
    , num_row;


--task2  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/17
SELECT 
    fm.member_name
    , status
    , sum(unit_price*amount) as costs
from 
    FamilyMembers fm
    join Payments p on p.family_member = fm.member_id 
        and date_format(p.date, '%Y') = '2005'
group by 
    fm.member_name
    , status
;
   
   
--task3  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/13
select distinct p1.name From Passenger p1 join Passenger p2 on p2.name = p1.name and p1.id != p2.id

--task4  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/38
select count(*) as count from Student where first_name = 'Anna'

--task5  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/35
SELECT 
    count(distinct classroom) as count 
FROM 
    Schedule
WHERE 
    date_format(date, '%d.%m.%Y') = '02.09.2019'
;

--task6  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/38
--см. task4 (lesson8)

--task7  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/32
select floor(avg(floor(datediff(sysdate(),birthday)/365))) as age from FamilyMembers;

--task8  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/27
select
     good_type_name
    , sum(amount*unit_price) as costs
from 
    Payments p
    join Goods g on g.good_id = p.good
    join GoodTypes gt on gt.good_type_id = g.type
WHERE 
    date_format(date, '%Y') =  '2005' 
group by
    gt.good_type_name
;

--task9  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/37
select 
    floor(datediff(sysdate(), birthday)/365) as year 
from 
    Student
where 
    birthday = (select max(birthday) from Student)
;

--task10  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/44
select 
    max(floor(datediff(sysdate(),s.birthday)/365)) as max_year
from 
    class c
    join Student_in_class sc on sc.class = c.id and c.name like '10%'
    join Student s on s.id = sc.student
;

--task11 (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/20
select 
    fm.status
    , fm.member_name
    , sum(amount*unit_price) as costs
FROM 
    GoodTypes gd
    join Goods g on g.type = gd.good_type_id and gd.good_type_name = 'entertainment'
    join Payments p on p.good = g.good_id
    join FamilyMembers fm on fm.member_id = p.family_member
group BY 
    fm.status
    , fm.member_name
;

--task12  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/55
DELETE FROM company WHERE id IN (SELECT DISTINCT t.company FROM Trip t GROUP BY t.company HAVING COUNT(*) = (SELECT COUNT(*) FROM trip GROUP BY Company ORDER BY count(*) LIMIT 1))
;


-- универсальный запрос, так как легко вытащить любой тип ID, если бы был
-- реализованы связки через PersonalKey и ForeignKey
delete from Company where id in 
	(
		select 
			id 
		from 
			(
				select 
					distinct c.id       --удаление компаний
				FROM 
					Company c
					join trip t on t.company = c.id
					join Pass_in_trip pit on pit.trip = t.id
					join Passenger p on p.id = pit.passenger 
				where 
					c.id in (
								select 
									distinct c.id
								FROM 
									Trip t 
									join Company c on c.id = t.company 
								group by 
									c.id
								HAVING count(*) = (select count(*) 
													from trip 
													group by Company 
													order by count(*) limit 1))
			) as slаа
	);

--task13  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/45
select 
	classroom 
from 
	Schedule
GROUP BY 
	classroom
HAVING 
	count(classroom) = 
		(
			select 
				count(classroom)
			From 
				Schedule 
			group by 
				classroom 
			order by 
				count(classroom) desc
			limit 1
		)
;

--task14  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/43
select 
    distinct last_name 
from 
    Teacher t 
    join Schedule s on s.teacher = t.id 
    join Subject su on su.id = s.subject and su.name = 'Physical Culture'
order by 
    last_name
;


--task15  (lesson8)
-- https://sql-academy.org/ru/trainer/tasks/63
select 
    concat(last_name, '.', substring(first_name,1,1), '.', substring(middle_name,1,1), '.') as name
from 
    Student
order by 
    1
;
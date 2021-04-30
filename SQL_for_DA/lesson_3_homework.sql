--схема БД: https://docs.google.com/document/d/1NVORWgdwlKepKq_b8SPRaSpraltxoMg2SIusTEN6mEQ/edit?usp=sharing

--task1
--Корабли: Для каждого класса определите число кораблей этого класса, потопленных в сражениях. Вывести: класс и число потопленных кораблей.

select c."class", count(o."result") from classes c join ships s on s."class" = c."class" left join outcomes o on o.ship = s."name" and o."result" = 'sunk'
group by c."class"


--task2
--Корабли: Для каждого класса определите год, когда был спущен на воду первый корабль этого класса. Если год спуска на воду головного корабля неизвестен, определите минимальный год спуска на воду кораблей этого класса. Вывести: класс, год.

select 
	c."class"
	, min(launched) as launched_year 
from 
	classes c 
	join ships s on s."class" = c."class" 
group by c."class" 
order by min(launched)

--task3
--Корабли: Для классов, имеющих потери в виде потопленных кораблей и не менее 3 кораблей в базе данных, вывести имя класса и число потопленных кораблей.

select c."class", count(o."result") 
from 
	classes c 
	join ships s on s."class" = c."class" 
	left join outcomes o on o.ship = s."name" and o."result" = 'sunk'
group by c."class"
having count(o."result") > 3


--task4
--Корабли: Найдите названия кораблей, имеющих наибольшее число орудий среди всех кораблей такого же водоизмещения (учесть корабли из таблицы Outcomes).
with ship_name as (select coalesce(s."name", o.ship) as ship, coalesce (s."class", o.ship) as "class" from outcomes o full join ships s on s."name" = o.ship) 
select sn.ship, sn."class", c.numguns, c.displacement from classes c right join ship_name sn on sn."class" = c."class" 
where 
	(c.numguns, c.displacement) in (select max(numguns) as numguns, c.displacement from classes c group by displacement )
order by c.displacement desc, c.numguns 

--task5
--Компьютерная фирма: Найдите производителей принтеров, которые производят ПК с наименьшим объемом RAM и с самым быстрым процессором среди всех ПК, имеющих наименьший объем RAM. Вывести: Maker

select maker from 
	product p 
	join pc on pc.model = p.model and (pc.ram, pc.speed) = (select min(ram), max(speed) from pc group by ram order by min(ram) limit 1)
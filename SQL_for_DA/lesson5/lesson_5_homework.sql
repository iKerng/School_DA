--схема БД: https://docs.google.com/document/d/1NVORWgdwlKepKq_b8SPRaSpraltxoMg2SIusTEN6mEQ/edit?usp=sharing
--colab/jupyter: https://colab.research.google.com/drive/1j4XdGIU__NYPVpv74vQa9HUOAkxsgUez?usp=sharing

--task1 (lesson5)
-- Компьютерная фирма: Сделать view (pages_all_products), в которой будет постраничная разбивка всех продуктов (не более двух продуктов на одной странице). 
-- Вывод: все данные из laptop, номер страницы, список всех страниц

SELECT 
	p.maker
	, l.*
	, round((ROW_NUMBER() over() + 1)/2) AS page 
	, count(*) OVER()/2 pages
FROM 
	product p 
	JOIN laptop l ON l.model = p.model

--task1 (lesson5) с уточнением
	
SELECT 
	app.maker
	, model 
	, REPLACE('list'||to_char(round((ROW_NUMBER() over(ORDER BY maker) + 1)/2), '999'),' ', '') AS page 
	, count(*) OVER()/2 AS count_pages
FROM 
	all_products_price app 

	
--task2 (lesson5)
-- Компьютерная фирма: Сделать view (distribution_by_type), в рамках которого будет процентное соотношение всех товаров по типу устройства. Вывод: производитель,
CREATE OR REPLACE VIEW distribution_by_type AS 
(SELECT * FROM (SELECT "type", (count(*) OVER(PARTITION BY "type")*100/count(*) over()) AS percent_all FROM all_products_price app ORDER BY maker) a 
GROUP BY 1,2)
	
--task3 (lesson5)
-- Компьютерная фирма: Сделать на базе предыдущенр view график - круговую диаграмму

SELECT * from distribution_by_type

--task4 (lesson5)
-- Корабли: Сделать копию таблицы ships (ships_two_words), но у название корабля должно состоять из двух слов
CREATE TABLE ships_two_words AS 
(
	SELECT * FROM ships s WHERE "name" LIKE '% %' 
);


--task5 (lesson5)
-- Корабли: Вывести список кораблей, у которых class отсутствует (IS NULL) и название начинается с буквы "S"
CREATE OR REPLACE VIEW all_ships AS 
select 
	COALESCE (o."ship", s."name") AS ship_name
	, s."class"
from 
	outcomes o  
	left join ships s on s."name" = o.ship;  

SELECT * FROM all_ships als 
WHERE 
	als."class" IS NULL AND als.ship_name LIKE 'S%' 

--task6 (lesson5)
-- Компьютерная фирма: Вывести все принтеры производителя = 'A' со стоимостью выше средней по принтерам производителя = 'C' 
--и три самых дорогих (через оконные функции). Вывести model

SELECT * FROM 	
	(
		SELECT 
			*
			, row_number() OVER(ORDER BY price) AS rn
		FROM 
			all_products_price app 
		WHERE 
			maker = 'A' 
			AND "type" = 'Printer' 
			AND price > (SELECT COALESCE (avg(price), 0) FROM all_products_price app2 WHERE maker = 'С' AND app2."type" = 'Printer')
	) a
WHERE 
	rn < 4;

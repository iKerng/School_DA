--схема БД: https://docs.google.com/document/d/1NVORWgdwlKepKq_b8SPRaSpraltxoMg2SIusTEN6mEQ/edit?usp=sharing
--colab/jupyter: https://colab.research.google.com/drive/1j4XdGIU__NYPVpv74vQa9HUOAkxsgUez?usp=sharing

create or replace view all_products_price as 
	(
		select pro.maker, pro."type", mo.*from 
			product pro
			join 
			(
				SELECT model, price FROM pc
				union all
				SELECT model, price FROM printer p 
				union all
				SELECT model, price FROM laptop
			) mo on mo.model = pro.model
	)

--task13 (lesson3)
--Компьютерная фирма: Вывести список всех продуктов и производителя с указанием типа продукта (pc, printer, laptop). Вывести: model, maker, type
with query_models as 
	(
		SELECT model, 'PC' as "type" FROM pc
		union
		SELECT model, 'Printer' FROM printer p 
		union
		SELECT model, 'Laptop' FROM laptop
	)
select pro.maker, qm.* from product pro join query_models qm on qm.model = pro.model

--task14 (lesson3)
--Компьютерная фирма: При выводе всех значений из таблицы printer дополнительно вывести для тех, у кого цена вышей средней PC - "1", у остальных - "0"

SELECT pr.*, case when pr.price > (select avg(price) from printer) then 1 else 0 end as more_avg FROM printer pr

--task15 (lesson3)
--Корабли: Вывести список кораблей, у которых class отсутствует (IS NULL)

select * from ships s where s."class" is null

--task16 (lesson3)
--Корабли: Укажите сражения, которые произошли в годы, не совпадающие ни с одним из годов спуска кораблей на воду.

select "name" from battles b where to_number(to_char(b."date", 'YYYY'), '9999') <> any (select launched from ships s)

--task17 (lesson3)
--Корабли: Найдите сражения, в которых участвовали корабли класса Kongo из таблицы Ships.

select b."name" from outcomes o join battles b on b."name"  = o.battle join ships s on s."name" = o.ship and s."class" = 'Kongo'

--task1  (lesson4)
-- Компьютерная фирма: Сделать view (название all_products_flag_300) для всех товаров (pc, printer, laptop) с флагом, если стоимость больше > 300. Во view три колонки: model, price, flag

create view all_products_flag_300 as 
	(
		select
			model
			, price
			, case when price > 300 then 1 else 0 end as flag
		from 
			(
				SELECT model, price FROM pc
				union
				SELECT model, price FROM printer p 
				union
				SELECT model, price FROM laptop
			)
	)

--task2  (lesson4)
-- Компьютерная фирма: Сделать view (название all_products_flag_avg_price) для всех товаров (pc, printer, laptop) с флагом, если стоимость больше cредней . Во view три колонки: model, price, flag

create view all_products_flag_avg_price as 
	(
		with models_price as 
			(
				SELECT model, price FROM pc
				union
				SELECT model, price FROM printer p 
				union
				SELECT model, price FROM laptop
			)
		select
			model
			, price
			, case when price > (select avg(price) from models_price) then 1 else 0 end as flag
		from 
			models_price
	)
	
		
--task3  (lesson4)
-- Компьютерная фирма: Вывести все принтеры производителя = 'A' со стоимостью выше средней по принтерам производителя = 'D' и 'C'. Вывести model

select ap.model from all_products_price ap 
where 
	ap.maker = 'A'
	and ap."type" = 'Printer'
	and ap.price > (select avg(price) from all_products_price app where app.maker in ('D', 'C') and app."type" = 'Printer')
	
--	
--task4 (lesson4)
-- Компьютерная фирма: Вывести все товары производителя = 'A' со стоимостью выше средней по принтерам производителя = 'D' и 'C'. Вывести model

select * from all_products_price app
where 
	app.maker = 'A'
	and app.price > (select avg(price) from all_products_price app1 where app1.maker in ('D', 'C') and app1."type" = 'Printer')

	
	
--task5 (lesson4)
-- Компьютерная фирма: Какая средняя цена среди уникальных продуктов производителя = 'A' (printer & laptop & pc)

select avg(price) from (select distinct model, price from all_products_price app where maker = 'A')	b
;
--task6 (lesson4)
-- Компьютерная фирма: Сделать view с количеством товаров (название count_products_by_makers) по каждому производителю. Во view: maker, count
create view count_products_by_makers as 
	(select maker, count(*) as count from all_products_price app group by maker)
;
--task7 (lesson4)
-- По предыдущему view (count_products_by_makers) сделать график в colab (X: maker, y: count)

/*
 * see at lesson_4_homework.py
 * */

--task8 (lesson4)
-- Компьютерная фирма: Сделать копию таблицы printer (название printer_updated) и удалить из нее все принтеры производителя 'D'

-- 1 variant
create table printer_updated as 
	(select * from printer where model not in (select model from all_products_price where "type" = 'Printer' and maker = 'D'));
-- 2 variant
drop table printer_updated;
create table printer_updated as (select * from printer);
delete from printer_update where model in (select model from all_products_price where "type" = 'Printer' and maker = 'D'));
	
--task9 (lesson4)
-- Компьютерная фирма: Сделать на базе таблицы (printer_updated) view с дополнительной колонкой производителя (название printer_updated_with_makers)

create or replace view printer_updated_with_makers as 
	(select distinct pu.*, pro.maker from printer_updated pu join product pro on pro.model = pu.model )

--task10 (lesson4)
-- Корабли: Сделать view c количеством потопленных кораблей и классом корабля (название sunk_ships_by_classes). Во view: count, class (если значения класса нет/IS NULL, то заменить на 0)

create or replace view sunk_ships_by_classes as 
	(		
		select 
			coalesce (s."class", '0') as "ship_class",
			count(*) as quantity
		from 
			outcomes o  
			left join ships s on s."name" = o.ship  
		where o."result" = 'sunk' 
		group by s."class"
	);
	
--task11 (lesson4)
-- Корабли: По предыдущему view (sunk_ships_by_classes) сделать график в colab (X: class, Y: count)

/*
 * see at lesson_4_homework.py
 * */


--task12 (lesson4)
-- Корабли: Сделать копию таблицы classes (название classes_with_flag) и добавить в нее flag: если количество орудий больше или равно 9 - то 1, иначе 0

create table classes_with_flag as 
	(select c.*, case when numguns >= 9 then 1 else 0 end as flag from classes c)

--task13 (lesson4)
-- Корабли: Сделать график в colab по таблице classes с количеством классов по странам (X: country, Y: count)

/*
 * see at lesson_4_homework.py
 * */

--task14 (lesson4)
-- Корабли: Вернуть количество кораблей, у которых название начинается с буквы "O" или "M".

	select count(regexp_match(s."name", '^(O|M)')) from ships s
		
--task15 (lesson4)
-- Корабли: Вернуть количество кораблей, у которых название состоит из двух слов.
	
	select count(*) from ships s where s."name" like '% %'
	
--task16 (lesson4)
-- Корабли: Построить график с количеством запущенных на воду кораблей и годом запуска (X: year, Y: count)

/*
 * see at lesson_4_homework.py
 * */
	
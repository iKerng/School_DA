--схема БД: https://docs.google.com/document/d/1NVORWgdwlKepKq_b8SPRaSpraltxoMg2SIusTEN6mEQ/edit?usp=sharing
--colab/jupyter: https://colab.research.google.com/drive/1j4XdGIU__NYPVpv74vQa9HUOAkxsgUez?usp=sharing

--task1  (lesson6, дополнительно)
-- SQL: Создайте таблицу с синтетическими данными (10000 строк, 3 колонки, все типы int) и заполните ее случайными данными от 0 до 1 000 000. 
--Проведите EXPLAIN операции и сравните базовые операции.
CREATE TABLE sintetic_table AS 
	(
		SELECT 
			round((random()*1000000)) AS column_a
			, round((random()*1000000)) AS column_b
			,  round((random()*1000000)) AS column_c 
		FROM 
			generate_series(1, 1000, 1) a
	)

CREATE INDEX IDX_SINTETIC_TABLE_COLUMN_A ON sintetic_table(column_a);
EXPLAIN ANALYZE 
--	SELECT 
--		a.*
--		, row_NUMERIC(10)() OVER(ORDER BY COLUMN_B) 
--	FROM 
--		sintetic_table a
--	WHERE 
--		COLUMN_A BETWEEN 400000 AND 600000;
	SELECT DISTINCT column_a FROM sintetic_table;



HashAggregate  (cost=19.50..29.50 rows=1000 width=8) (actual time=0.289..0.400 rows=1000 loops=1)
  Group Key: column_a
  ->  Seq Scan on sintetic_table  (cost=0.00..17.00 rows=1000 width=8) (actual time=0.009..0.083 rows=1000 loops=1)
Planning time: 0.168 ms
Execution time: 0.467 ms	
	



DROP INDEX IDX_SINTETIC_TABLE_COLUMN_A;
EXPLAIN ANALYZE 
--	SELECT 
--		a.*
--		, row_NUMERIC(10)() OVER(ORDER BY COLUMN_B) 
--	FROM 
--		sintetic_table a
--	WHERE 
--		COLUMN_A BETWEEN 400000 AND 600000;
	SELECT DISTINCT column_a FROM sintetic_table;


HashAggregate  (cost=19.50..29.50 rows=1000 width=8) (actual time=0.372..0.485 rows=1000 loops=1)
  Group Key: column_a
  ->  Seq Scan on sintetic_table  (cost=0.00..17.00 rows=1000 width=8) (actual time=0.019..0.114 rows=1000 loops=1)
Planning time: 0.070 ms
Execution time: 0.566 ms
	
	


--task2 (lesson6, дополнительно)
-- GCP (Google Cloud Platform): Через GCP загрузите данные csv в базу PSQL по личным реквизитам (используя только bash и интерфейс bash) 

psql -h 52.157.159.24 -U student10 -d sql_ex_for_student10

psql -h 52.157.159.24 -U student10 -d sql_ex_for_student10 -c 'create table avocado(id NUMERIC(10), "Date" varchar, AveragePrice NUMERIC(10), Total_Volume NUMERIC(10), "4046" NUMERIC(10), "4225" NUMERIC(10), "4770" NUMERIC(10), Total_Bags NUMERIC(10), Small_Bags NUMERIC(10), Large_Bags NUMERIC(10), XLarge_Bags NUMERIC(10), "type" varchar, "year" NUMERIC(10), "region" varchar);'

psql -h 52.157.159.24 -U student10 -d sql_ex_for_student10 -c "\copy avocado from 'avocado.csv' delimiter ',' header csv"

SELECT * FROM avocado
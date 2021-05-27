--task1  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/the-report/problem
SELECT * FROM 
    (
        SELECT
            S.NAME
            , G.GRADE
            , S.MARKS AS MARK
        FROM 
            STUDENTS S
            JOIN GRADES G ON G.GRADE = (TRUNC(CASE WHEN MARKS = 100 THEN 99 ELSE MARKS END, -1)/10 +1)
                AND G.GRADE >= 8
        ORDER BY 
            G.GRADE DESC, 
            S.NAME ASC
    ) A
UNION ALL
SELECT * FROM 
    (
        SELECT
            NULL
            , G.GRADE
            , S.MARKS
        FROM 
            STUDENTS S
            JOIN GRADES G ON G.GRADE = (TRUNC(CASE WHEN MARKS = 100 THEN 99 ELSE MARKS END, -1)/10 +1)
                AND G.GRADE < 8
        ORDER BY 
            G.GRADE DESC, S.MARKS ASC
    ) B
;


--task2  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/occupations/problem
SELECT 
    A.NAME
    , B.NAME
    , C.NAME
    , D.NAME
FROM 
	(SELECT NAME, OCCUPATION, ROW_NUMBER() OVER(ORDER BY NAME) NUM FROM OCCUPATIONS WHERE OCCUPATION = 'Doctor') A
	FULL JOIN (SELECT NAME, OCCUPATION, ROW_NUMBER() OVER(ORDER BY NAME) NUM FROM OCCUPATIONS WHERE OCCUPATION = 'Professor') B ON A.NUM = B.NUM
	FULL JOIN (SELECT NAME, OCCUPATION, ROW_NUMBER() OVER(ORDER BY NAME) NUM FROM OCCUPATIONS WHERE OCCUPATION = 'Singer') C ON C.NUM = B.NUM
	FULL JOIN (SELECT NAME, OCCUPATION, ROW_NUMBER() OVER(ORDER BY NAME) NUM FROM OCCUPATIONS WHERE OCCUPATION = 'Actor') D ON D.NUM = C.NUM
;

--или так:

SELECT 
    DOC
    , PROF
    , SING
    , ACT 
FROM 
    (
        SELECT 
            O.*
        , ROW_NUMBER() OVER(PARTITION BY OCCUPATION ORDER BY NAME) AS RN 
        FROM OCCUPATIONS O
    )
PIVOT
    (
        MAX(NAME)
        FOR OCCUPATION IN 
            (
                'Doctor' AS DOC
                , 'Professor' AS PROF
                , 'Singer' AS SING
                , 'Actor' AS ACT
            )
    )
ORDER BY 
    RN
;

--task3  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/weather-observation-station-9/problem
SELECT 
    DISTINCT CITY 
FROM 
    STATION 
WHERE 
    REGEXP_LIKE (LOWER(CITY), '^[^aeiou]')
-- исключил y, так как по их мнению это гласная
;

--task4  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/weather-observation-station-10/problem
SELECT 
    DISTINCT CITY 
FROM 
    STATION 
WHERE 
    REGEXP_LIKE (LOWER(CITY), '[^aeiou]\Z')
;

--task5  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/weather-observation-station-11/problem
SELECT 
    DISTINCT CITY 
FROM 
    STATION 
WHERE 
    REGEXP_LIKE (LOWER(CITY), '^[^aeiou]|[^aeiou]\Z')
;


--task6  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/weather-observation-station-12/problem
SELECT 
    DISTINCT CITY 
FROM 
    STATION 
WHERE 
    REGEXP_LIKE (LOWER(CITY), '(^[^aeiou]).*([^aeiou]\Z)')
;

--task7  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/salary-of-employees/problem
select name from Employee 
where salary > 2000 and months < 10
;

--task8  (lesson9)
-- oracle: https://www.hackerrank.com/challenges/the-report/problem
--задача повторяется, см. task1 (lesson9) 

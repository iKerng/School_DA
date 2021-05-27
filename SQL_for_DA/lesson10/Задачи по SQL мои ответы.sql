1)
select 
	al.bank
	, al."date"
	, al.gender
	, al.age_group
	, avg(al.salary) as avg_salary
	, count(*) as quantity_clients
from
	(
		select 
			ca.client_id
			, ca.bank
			, ca.salary
			, ca."date"
			, case when cd.age <= 18 then 1
				when cd.age <= 35 then 2
				when cd.age <= 60 then 3
				else 4 end as age_group
			, cd.gender
		from
			clnt_aggr ca
			join (select * from clnt_data where actual_to_date = to_date('2099-12-31', 'YYYY-MM-DD')) cd on cd.client_id = ca.client_id
		where
			ca."date" between to_date('2018-01-01', 'YYYY-MM-DD') and to_date('2018-12-31', 'YYYY-MM-DD')
	) al
group by 
	al.bank
	, al."date"
	, al.age_group
	, al.gender
;
2)
select 
	ca.bank
	, ca.client_id
	, ca.salary
from 
	clnt_aggr ca
where
	(ca.bank, ca.salary) in 
		(
			select 
				ca.bank
				, max(salary) as max_salary
			from
				clnt_aggr ca
			where
				ca.date = (select max("date") from clnt_aggr)
			group by 
				ca.bank
		)
;
3)
select 
	ca.client_id
from
	clnt_Aggr ca
where
	ca."date" = (select max("date") from clnt_Aggr)
	and client_id in 
		(
			select 
				client_id
			from 
				clnt_Aggr
			group by 
				client_id
			having 
				sum(pos_amt) > (select avg(pos_amt) from clnt_Aggr)
		)
;
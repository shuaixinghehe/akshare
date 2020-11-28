sql = """
select
    T3.ts_code,
    T3.name,
	(cast(T3.{} as decimal(5,2))- cast(T4.{} as decimal(5,2)))/ cast(T4.{} as decimal(5,2)) rate,
	pe,total_share,float_share,free_share,total_mv,circ_mv
from
(
    select
	    T1.ts_code,
	    T1.{},
	    T2.name,
	    T5.pe,total_share,float_share,free_share,total_mv,circ_mv
	from
	(
	        select *
	        from stock_daily
	        where trade_date='{}'

	)T1
	join
	(
	        select *
	        from stock_basic
	        where dt='{}' and market  not in ('科创板')

	)T2 on (T1.ts_code=T2.ts_code)
	join
	(
	        select ts_code,pe,total_share,float_share,free_share,total_mv,circ_mv
	        from stock_daily_basic
	        where trade_date='{}' 
	)T5 on (T1.ts_code=T5.ts_code)
)T3
join
(
    select *
	from stock_daily
	where trade_date='{}'

)T4 on (T3.ts_code=T4.ts_code)
order by rate desc
limit 100;
"""
type = "high"
start_date = "20201102"
end_date = "20201127"
print(sql.format(type, type, type, type, end_date, end_date,end_date, start_date))

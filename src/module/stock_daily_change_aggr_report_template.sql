-- 最近5个工作日涨跌幅限制
select 
	T3.ts_code,T3.name,T3.high,T3.close,T4.high,T4.close,
	
	(cast(T3.high as DECIMAL(5,2))- cast(T4.high as DECIMAL(5,2)))/ cast(T4.high as DECIMAL(5,2)) 5_daily_rate,
	(cast(T3.high as DECIMAL(5,2))- cast(T5.high as DECIMAL(5,2)))/ cast(T5.high as DECIMAL(5,2)) 10_daily_rate
from
(
	select
	    T1.ts_code,
	    T1.high,
	    T1.close,
	    T2.name
	from
	(
	        select *
	        from stock_daily
	        where trade_date='20200730'
	
	)T1
	join
	(
	        select *
	        from stock_basic
	        where dt='20200730' and market  not in ('科创板')
	        and list_date<='20200601'

	)T2 on (T1.ts_code=T2.ts_code)
)T3
join
(
	select *
	from stock_daily
	where trade_date='20200723'  
)T4 on (T3.ts_code=T4.ts_code)
join
(
	select *
	from stock_daily
	where trade_date='20200716'  
)T5 on (T3.ts_code=T5.ts_code)
join
(
	select *
	from stock_daily
	where trade_date='20200702'  
)T5 on (T3.ts_code=T5.ts_code)

order by 10_daily_rate desc 
limit 100;


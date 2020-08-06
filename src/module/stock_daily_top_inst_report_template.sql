	select
	    T1.pct_chg,
	    T2.name,
	    T3.*
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
	join
	(
	        select *
	        from top_inst
	        where trade_date='20200730'
	)T3 on (T1.ts_code=T3.ts_code);

	select
	    T2.name,
	    max(pct_chg),
	    sum(cast(net_buy as decimal )) total_net_buy
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
	join
	(
	        select *
	        from top_inst
	        where trade_date='20200730'
	)T3 on (T1.ts_code=T3.ts_code)
	group by name;



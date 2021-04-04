select
	T1.*,
	T2.*
from
(
	select ts_code,close ,trade_date
	from stock_daily
	where trade_date>='20200301' and trade_date<='20200401'
			and open!=close
)T1
join
(
	select ts_code,close ,trade_date
	from stock_daily
	where trade_date>='20200401' and trade_date<='20200501'
		and open!=close
)T2 on (T1.ts_code=T2.ts_code)
where T2.close/T1.close>=1.5 and timestampdiff(day,T1.trade_date,T2.trade_date)=30;



















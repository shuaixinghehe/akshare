use tushare;

select 
	ts_code,
	average_value,
	((max_open-average_value) * (max_open-average_value) +
	(max_high-average_value) * (max_high-average_value) +
	(max_low-average_value) * (max_low-average_value) +
	(max_close-average_value) * (max_close-average_value)) / 4.0 
from 
(
	select 
		ts_code,
		sum(open+high+low+close)/4.0 as average_value,
		max(open) max_open,
		max(high) max_high,
		max(low) max_low,
		max(close) max_close
	from tushare.stock_daily
	where trade_date='20200116'
	group by ts_code
)T1

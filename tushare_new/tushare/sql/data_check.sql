select *
from
(
select *
from stock_daily_basic
where trade_date='20201216'
) T2
left join
(
 select trade_date,ts_code
 from realtime_action_detail_basic
 where trade_date='20201216'
 )T1 on (T2.ts_code=T1.ts_code)
 where T1.ts_code is null
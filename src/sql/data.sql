select
    T1.ts_code,T1.f,T2.name
from
(
    select
        ts_code,cast(circ_mv as DECIMAL(20,2) )/10000  f
    from stock_daily_basic
    where trade_date='20201016'
)T1
join
(
    select *
    from stock_basic
    where dt='20201016'
)T2 on (T1.ts_code=T2.ts_code)
order by f desc
limit 1000;


select
    T1.ts_code,T1.f,T2.name
from
(
    select
        ts_code,cast(circ_mv as DECIMAL(20,2) )/10000  f
    from stock_daily_basic
    where trade_date='20201016'
)T1
join
(
    select *
    from stock_basic
    where dt='20201016'
        and market in ('主板','中小板','创业板')
)T2 on (T1.ts_code=T2.ts_code)
where T1.f >=100.0;








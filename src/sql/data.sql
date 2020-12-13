select
    T1.ts_code,T1.f,T2.name
from
(
    select
        ts_code,cast(circ_mv as decimal(20,2) )/10000  f
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
        ts_code,cast(circ_mv as decimal(20,2) )/10000  f
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


-- 各个板块的情况
select
    T1.industry,
    sum(T2.total_mv) sum_total_mv,
    sum(T2.circ_mv) sum_circ_mv
from
(
    select ts_code,industry
    from stock_basic
    where dt='{}'
    group by ts_code,industry
)T1
join
(
    select ts_code,total_mv,circ_mv
    from stock_daily_basic
    where trade_date='{}'
    group by ts_code,total_mv,circ_mv
)T2 on (T1.ts_code=T2.ts_code)
group by     T1.industry







select 
    T1.ts_code,
    T2.name,
    count(1) cnt,
    group_concat(trade_date) trade_date_list
from
(
        select *
        from stock_daily
        where trade_date>='20200720' and low!=high
        and pct_chg>=9.90
)T1
join
(
        select *
        from stock_basic
        where dt='20200729' and market  not in ('科创板')
)T2 on (T1.ts_code=T2.ts_code)
group by T1.ts_code,T2.name
order by cnt desc ;


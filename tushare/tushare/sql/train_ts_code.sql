use tushare;
select ts_code,count(1) cnt,group_concat(trade_date) from stock_daily  group by ts_code order by cnt desc ;

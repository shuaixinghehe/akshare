select trade_date,count(1) cnt from stock_realtime_action_002400SZ group by trade_date;




select trade_date, sum(volumn)
from stock_realtime_action_002400SZ
where trade_date>='20200701'
group by trade_date;


select
   trade_date, avg(price) avg_price, sum(price*volumn)/sum(volumn) avg_trade_price,
   std(price) std_price,
   sum(if(kind='买盘',volumn,0)) buy_kind_volumn,
   sum(if(kind='卖盘',volumn,0)) sell_kind_v,
   sum(if(kind='中性盘',volumn,0)) neutral_kind_v,
   sum(volumn)
from akshare.stock_realtime_action_002400SZ
where trade_date>='20200705'
group by trade_date;

select
   trade_date, avg(price) avg_price, sum(price*volumn)/sum(volumn) avg_trade_price,
   std(price) std_price,
   sum(if(kind='买盘',volumn,0)) buy_kind_volumn,
   sum(if(kind='卖盘',volumn,0)) sell_kind_v,
   sum(if(kind='中性盘',volumn,0)) neutral_kind_v,
   sum(volumn),
   sum(if(price>close,volumn,0))  profit_volumn
from
(
    select T1.*,T2.open,T2.high,T2.close
    from
    (
        select *
        from akshare.stock_realtime_action_002400SZ
        where trade_date>='20200710'
    )T1
    join
    (
        select *
        from tushare.stock_daily
        where trade_date>='20200710' and ts_code='002400.SZ'
    )T2 on (T1.trade_date=T2.trade_date)
)T3
group by trade_date;



select trade_date,kind,sum(volumn)
from stock_realtime_action_002400SZ
where trade_date>='20200705'
group by trade_date,kind


select trade_date, sum(value)/sum(volumn)
from
(
	select T1.trade_date,  (price-avg_true_price)*(price-avg_true_price) value,volumn
	from 
	(
		select trade_date, sum(price*volumn)/sum(volumn) avg_true_price
		from stock_realtime_action_002400SZ
		where trade_date>='20200705'
		group by trade_date
	)T1
	join
	(
		select trade_date, price,volumn
		from stock_realtime_action_002400SZ
		where trade_date>='20200705'
	)T2 on (T1.trade_date=T2.trade_date)
)T3
group by trade_date;










select
	trade_date,
	avg_price,
	avg_trade_price,
	std_price,
	buy_kind_volumn/sum_volumn buy_kind_volumn_rate,
	sell_kind_volumn/sum_volumn sell_kind_volumn_rate,
	neutral_kind_volumn/sum_volumn neutral_kind_volumn_rate,
	profit_volumn/sum_volumn profit_volumn_rate,
	lose_volumn/sum_volumn lose_volumn_rate,
	equal_volumn/sum_volumn equal_volumn_rate

from
(
	select
	   trade_date, avg(price) avg_price, sum(price*volumn)/sum(volumn) avg_trade_price,
	   std(price) std_price,
	   sum(if(kind='买盘',volumn,0)) buy_kind_volumn,
	   sum(if(kind='卖盘',volumn,0)) sell_kind_volumn,
	   sum(if(kind='中性盘',volumn,0)) neutral_kind_volumn,
	   sum(volumn) sum_volumn,
	   sum(if(price>close,volumn,0))  profit_volumn,
	   sum(if(price<close,volumn,0))  lose_volumn,
	   sum(if(price=close,volumn,0))  equal_volumn
	from
	(
	    select T1.*,T2.open,T2.high,T2.close
	    from
	    (
	        select *
	        from akshare.stock_realtime_action_002400SZ
	        where trade_date>='20200705'
	    )T1
	    join
	    (
	        select *
	        from tushare.stock_daily
	        where trade_date>='20200705' and ts_code='002400.SZ'
	    )T2 on (T1.trade_date=T2.trade_date)
	)T3
	group by trade_date
)T4;

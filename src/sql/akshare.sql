-----------
----------
---天级别的数据
----
create TABLE `akshare_daily` (
  `ts_code` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `trade_date` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `open` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `high` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `low` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `close` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `adjust` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `volume` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `outstanding_share` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `turnover` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

ALTER  TABLE  `akshare_daily`  ADD  PRIMARY  KEY (  `ts_code`,`trade_date`  ) ;
--- 实时数据
create TABLE `stock_realtime_action` (
  `ts_code` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `trade_date` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `trade_time` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `price` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `price_change` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `volumn` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `value` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `kind` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


--- 实时数据
create TABLE `check_stock_realtime_action` (
  `ts_code` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `trade_date` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `is_download` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
   PRIMARY KEY (`ts_code`,`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


--- 检查数据表
create TABLE if not exists `check_data_report` (
  `table_name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `detail` LONGTEXT COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin




insert into check_data_report (table_name,detail) values (
    "stock_basic",
    "select trade_date,count(1) cnt from tushare.stock_daily where trade_date>='{}' group by trade_date;"
);

insert into check_data_report (table_name,detail) values (
    "index_daily",
    "select trade_date,count(1) cnt from tushare.index_daily where trade_date>='{}' group by trade_date;"
);


insert into check_data_report (table_name,detail) values (
    "money_flow",
    "select trade_date,count(1) cnt from tushare.money_flow where trade_date>='{}' group by trade_date;"
);

insert into check_data_report (table_name,detail) values (
    "realtime_action_detail_basic",
    "select trade_date,count(1) cnt from tushare.realtime_action_detail_basic where trade_date>='{}' group by trade_date;"
);

insert into check_data_report (table_name,detail) values (
    "stock_daily",
    "select trade_date,count(1) cnt from tushare.stock_daily where trade_date>='{}' group by trade_date;"
);

insert into check_data_report (table_name,detail) values (
    "stock_daily_basic",
    "select trade_date,count(1) cnt from tushare.stock_daily_basic where trade_date>='{}' group by trade_date;"
);


insert into check_data_report (table_name,detail) values (
    "stock_daily_report_basic",
    "select trade_date,count(1) cnt from tushare.stock_daily_report_basic where trade_date>='{}' group by trade_date;"
);

insert into check_data_report (table_name,detail) values (
    "top_inst",
    "select trade_date,count(1) cnt from tushare.top_inst where trade_date>='{}' group by trade_date;"
);










    -- 最近5个工作日涨跌幅限制
select
	T3.ts_code,T3.name,T3.high,T3.close,T4.high,T4.close,

	(cast(T3.high as decimal(5,2))- cast(T4.high as decimal(5,2)))/ cast(T4.high as decimal(5,2)) 5_daily_rate,
	(cast(T3.high as DECIMAL(5,2))- cast(T5.high as DECIMAL(5,2)))/ cast(T5.high as DECIMAL(5,2)) 10_daily_rate,
	(cast(T3.high as DECIMAL(5,2))- cast(T6.high as DECIMAL(5,2)))/ cast(T6.high as DECIMAL(5,2)) 20_daily_rate
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
	        where trade_date='{}'

	)T1
	join
	(
	        select *
	        from stock_basic
	        where dt='{}' and market  not in ('科创板')
	        and list_date<='{}'

	)T2 on (T1.ts_code=T2.ts_code)
)T3
join
(
	select *
	from stock_daily
	where trade_date='{}'
)T4 on (T3.ts_code=T4.ts_code)
join
(
	select *
	from stock_daily
	where trade_date='{}'
)T5 on (T3.ts_code=T5.ts_code)
join
(
	select ts_code,high,close
	from stock_daily
	where trade_date='{}'
	group by ts_code,high,close
)T6 on (T3.ts_code=T6.ts_code)

order by 10_daily_rate desc




---
----
---
select
    T3.ts_code,
    T3.name,
	(cast(T3.'{}' as decimal(5,2))- cast(T4.'{}' as decimal(5,2)))/ cast(T4.'{}' as decimal(5,2)) rate
from
(
    select
	    T1.ts_code,
	    T1.'{}',
	    T2.name
	from
	(
	        select *
	        from stock_daily
	        where trade_date='{}'

	)T1
	join
	(
	        select *
	        from stock_basic
	        where dt='{}' and market  not in ('科创板')
	        and list_date<='{}'

	)T2 on (T1.ts_code=T2.ts_code)
)T3
join
(
    select *
	from stock_daily
	where trade_date='{}'

)T4 on (T3.ts_code=T4.ts_code)

























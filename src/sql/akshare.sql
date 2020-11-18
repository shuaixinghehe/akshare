-----------
----------
---天级别的数据
----
CREATE TABLE `akshare_daily` (
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


--- 实时数据
CREATE TABLE `stock_realtime_action` (
  `ts_code` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `trade_date` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `trade_time` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `price` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `price_change` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `volumn` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `value` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `kind` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin


--- 实时数据
CREATE TABLE `check_stock_realtime_action` (
  `ts_code` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `trade_date` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `is_download` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin


--- 检查数据表
CREATE TABLE if not exists `check_data_report` (
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








































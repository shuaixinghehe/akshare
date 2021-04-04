--ts_code	str	TS代码
--symbol	str	股票代码
--name	str	股票名称
--area	str	所在地域
--industry	str	所属行业
--fullname	str	股票全称
--enname	str	英文全称
--market	str	市场类型 （主板/中小板/创业板/科创板）
--exchange	str	交易所代码
--curr_type	str	交易货币
--list_status	str	上市状态： L上市 D退市 P暂停上市
--list_date	str	上市日期
--delist_date	str	退市日期
--is_hs	str	是否沪深港通标的，N否 H沪股通 S深股通

create database if not exists tushare;

use tushare;

create table if not exists stock_basic (
    dt varchar(100) ,
    ts_code varchar(100) ,
    symbol varchar(100) ,
    name varchar(100) ,
    area varchar(100) ,
    industry varchar(100) ,
    fullname varchar(100) ,
    enname varchar(100) ,
    market varchar(100) ,
    exchange varchar(100) ,
    curr_type varchar(100) ,
    list_status varchar(100) ,
    list_date varchar(100) ,
    delist_date varchar(100) ,
    is_hs varchar(100)
);
ALTER  TABLE  `stock_basic`  ADD  PRIMARY  KEY (  `dt`,`ts_code`  ) ;

insert into stock_basic (
dt,ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs
)
values
('20200511','600614.SH','600614','*ST鹏起','吉林','综合类','鹏起科技发展股份有限公司','Pengqi Technology Development Co., Ltd','主板','SSE','CNY','L','19920828','None','N')


--ts_code	str	股票代码
--trade_date	str	交易日期
--open	float	开盘价
--high	float	最高价
--low	float	最低价
--close	float	收盘价
--pre_close	float	昨收价
--change	float	涨跌额
--pct_chg	float	涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
--vol	float	成交量 （手）
--amount	float	成交额 （千元）
create table if not exists stock_daily (
    `ts_code` varchar(100) ,
    `trade_date` varchar(100) ,
    `open` varchar(100) ,
    `high` varchar(100) ,
    `low` varchar(100) ,
    `close` varchar(100) ,
    `pre_close` varchar(100) ,
    `change` varchar(100) ,
    `pct_chg` varchar(100),
    `vol` varchar(100),
    `amount` varchar(100),
      PRIMARY KEY (`trade_date`,`ts_code`)
);
    insert into stock_daily (
        `ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`
    )
    values

   ('test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test' );


--  ts_code	str	TS股票代码
--trade_date	str	交易日期
--close	float	当日收盘价
--turnover_rate	float	换手率（%）
--turnover_rate_f	float	换手率（自由流通股）
--volume_ratio	float	量比
--pe	float	市盈率（总市值/净利润）
--pe_ttm	float	市盈率（TTM）
--pb	float	市净率（总市值/净资产）
--ps	float	市销率
--ps_ttm	float	市销率（TTM）
--total_share	float	总股本 （万股）
--float_share	float	流通股本 （万股）
--free_share	float	自由流通股本 （万）
--total_mv	float	总市值 （万元）
--circ_mv	float	流通市值（万元）

create table if not exists stock_daily_basic (
    `ts_code` varchar(100) ,
    `trade_date` varchar(100) ,
    `close` varchar(100) ,
    `turnover_rate` varchar(100) ,
    `turnover_rate_f` varchar(100) ,
    `volume_ratio` varchar(100) ,
    `pe` varchar(100) ,
    `pe_ttm` varchar(100) ,
    `pb` varchar(100) ,
    `ps` varchar(100) ,
    `ps_ttm` varchar(100) ,
    `total_share` varchar(100) ,
    `float_share` varchar(100) ,
    `free_share` varchar(100) ,
    `total_mv` varchar(100) ,
    `circ_mv` varchar(100),
     PRIMARY KEY (`trade_date`,`ts_code`)
);


insert into stock_daily_basic (
             `ts_code`, `trade_date`, `close`, `turnover_rate`,
             `turnover_rate_f`, `volume_ratio`, `pe`, `pe_ttm`, `pb`,
              `ps`, `ps_ttm`,`total_share`,`float_share`,`free_share`,`total_mv`,
              `circ_mv`
        )
        values
        ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16" );



create table if not exists top_inst (
    `trade_date` varchar(100) ,
    `ts_code` varchar(100) ,
    `exalter` varchar(10000) ,
    `buy` varchar(100),
    `buy_rate` varchar(100),
    `sell` varchar(100),
    `sell_rate` varchar(100),
    `net_buy` varchar(100)
);


create table if not exists money_flow (
    `ts_code` varchar(100) ,
    `trade_date` varchar(100) ,
    `buy_sm_vol` varchar(10000) ,
    `buy_sm_amount` varchar(100),
    `sell_sm_vol` varchar(100),
    `sell_sm_amount` varchar(100),
    `buy_md_vol` varchar(100),
    `buy_md_amount` varchar(100),
    `sell_md_vol` varchar(100),
    `sell_md_amount` varchar(100),
    `buy_lg_vol` varchar(100),
    `buy_lg_amount` varchar(100),
    `sell_lg_vol` varchar(100),
    `sell_lg_amount` varchar(100),
    `buy_elg_vol` varchar(100),
    `buy_elg_amount` varchar(100),
    `sell_elg_vol` varchar(100),
    `sell_elg_amount` varchar(100),
    `net_mf_vol` varchar(100),
    `net_mf_amount` varchar(100)
);


create table if not exists realtime_action_detail_basic (
    `ts_code` varchar(100) ,
    `trade_date` varchar(100) ,
    `avg_price` varchar(10000) ,
    `avg_trade_price` varchar(100),
    `std_price` varchar(100),
    `buy_kind_volumn_rate` varchar(100),
    `sell_kind_volumn_rate` varchar(100),
    `neutral_kind_volumn_rate` varchar(100),
    `profit_volumn_rate` varchar(100),
    `lose_volumn_rate` varchar(100),
    `equal_volumn_rate` varchar(100)
);

create table if not exists index_daily (
    `ts_code` varchar(100) ,
    `trade_date` varchar(100) ,
    `close` varchar(100) ,
    `open` varchar(100) ,
    `high` varchar(100) ,
    `low` varchar(100) ,
    `pre_close` varchar(100) ,
    `change` varchar(100) ,
    `pct_chg` varchar(100) ,
    `vol` varchar(100) ,
    `amount` varchar(100)
);

CREATE TABLE `realtime_action_detail_basic_5day` (
  `ts_code` varchar(100) DEFAULT NULL,
  `trade_date` varchar(100) DEFAULT NULL,
  `avg_price` varchar(10000) DEFAULT NULL,
  `avg_trade_price` varchar(100) DEFAULT NULL,
  `std_price` varchar(100) DEFAULT NULL,
  `buy_kind_volumn_rate` varchar(100) DEFAULT NULL,
  `sell_kind_volumn_rate` varchar(100) DEFAULT NULL,
  `neutral_kind_volumn_rate` varchar(100) DEFAULT NULL,
  `profit_volumn_rate` varchar(100) DEFAULT NULL,
  `lose_volumn_rate` varchar(100) DEFAULT NULL,
  `equal_volumn_rate` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1

CREATE TABLE `realtime_action_detail_basic_10day` (
  `ts_code` varchar(100) DEFAULT NULL,
  `trade_date` varchar(100) DEFAULT NULL,
  `avg_price` varchar(10000) DEFAULT NULL,
  `avg_trade_price` varchar(100) DEFAULT NULL,
  `std_price` varchar(100) DEFAULT NULL,
  `buy_kind_volumn_rate` varchar(100) DEFAULT NULL,
  `sell_kind_volumn_rate` varchar(100) DEFAULT NULL,
  `neutral_kind_volumn_rate` varchar(100) DEFAULT NULL,
  `profit_volumn_rate` varchar(100) DEFAULT NULL,
  `lose_volumn_rate` varchar(100) DEFAULT NULL,
  `equal_volumn_rate` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1
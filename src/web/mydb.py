#! /usr/bin/env python
# *-* coding:utf-8 *-*
import web

db_akshare = web.database(dbn='mysql', db='akshare', user='tushare', pw='&QwX0^4#Sm^&t%V6wBnZC%78')
db_tushare = web.database(dbn='mysql', db='tushare', user='tushare', pw='&QwX0^4#Sm^&t%V6wBnZC%78')
t = db_akshare.transaction()


def get_model_reco_stock_detail(model_name):
    data = db_akshare.select('model_reco_stock_detail', where='model_name=$model_name', vars=locals())
    return data

def insert_admin_skill_answer_log(user_id,ts_code,start_trade_date,end_trade_date,predict_trade_date,fact,user_answer,result,detail):
    data = db_tushare.insert('submit_admin_skill_answer_log',
                            user_id=user_id,ts_code=ts_code,start_trade_date=start_trade_date, 
                            end_trade_date=end_trade_date, predict_trade_date=predict_trade_date,
                            fact=fact,user_answer=user_answer,result=result,detail=detail,vars=locals())


def get_admin_skill_user_id(user_id):
    data = db_tushare.query('select count(1) as cnt from submit_admin_skill_answer_log where user_id={}'.format(user_id))
    return data

def get_admin_skill_user_rank():
    data = db_tushare.query('select user_id,sum(result) as score from submit_admin_skill_answer_log group by user_id order by score desc ')
    return data


def get_stock_detail(ts_code, trade_date):
    return db_tushare.select('stock_daily', where='ts_code=$ts_code and trade_date=$trade_date', vars=locals())


def get_tushare_query(sql=""):
    return db_tushare.query(sql)


def get_stock_daily(trade_date):
    return db_tushare.select('stock_daily', where='trade_date=$trade_date', vars=locals())


def get_stock_daily_history(trade_date, ts_code):
    return db_tushare.select('stock_daily', where='trade_date>=$trade_date and ts_code=$ts_code', order="trade_date",
                             vars=locals())


def get_stock_list(trade_date):
    return db_tushare.select('stock_daily', where='trade_date=$trade_date', vars=locals())


def get_check_data_report():
    return db_tushare.select('check_data_report', vars=locals())


def get_industry_report(trade_date, industry):
    return db_tushare.query("""
        select 
    T1.ts_code,T1.name,T2.*,T3.pct_chg
from 
(
    select ts_code,name
    from stock_basic
    where dt='{}' and industry='{}'
    group by ts_code,name
)T1
join
(
    select *
    from stock_daily_basic
    where trade_date='{}' 
)T2 on (T1.ts_code=T2.ts_code)
join
(
    select ts_code,pct_chg
    from stock_daily
    where trade_date='{}'
    group by ts_code,pct_chg 
)T3 on (T1.ts_code=T3.ts_code)
order by cast(total_mv as SIGNED)  desc 
limit 10000;
    """.format(trade_date, industry, trade_date, trade_date))


def get_stock_name(trade_date):
    return db_tushare.select('stock_basic', where='dt=$trade_date', vars=locals())


def get_stock_code(trade_date):
    return db_tushare.query(""" 
    select distinct ts_code from stock_daily where trade_date>={}
    """.format(trade_date))


def get_stock_daily_basic(trade_date):
    return db_tushare.select('stock_daily_basic', where='trade_date=$trade_date', vars=locals())


def get_stock_daily_report_detail(trade_date):
    return db_tushare.select('stock_daily_report_basic', where='trade_date=$trade_date', vars=locals())


def get_stock_continue_high(start_date, trade_date):
    pass
    return db_tushare.query("""
        select 
    T1.ts_code,
    T2.name,
    count(1) cnt,
    group_concat(trade_date) trade_date_list
from
(
        select *
        from stock_daily
        where trade_date>={} and low!=high
        and pct_chg>=9.90
)T1
join
(
        select *
        from stock_basic
        where dt={} and market  not in ('科创板')
)T2 on (T1.ts_code=T2.ts_code)
group by T1.ts_code,T2.name
order by cnt desc ;
    """.format(start_date, trade_date))


def get_stock_change_aggr(today_trade_date, list_trade_date, day_5_before_trade_date, day_10_before_trade_date,
                          day_20_before_trade_date):
    return db_tushare.query("""
    -- 最近5个工作日涨跌幅限制
select 
	T3.ts_code,T3.name,T3.high,T3.close,T4.high,T4.close,
	
	(cast(T3.high as DECIMAL(5,2))- cast(T4.high as DECIMAL(5,2)))/ cast(T4.high as DECIMAL(5,2)) 5_daily_rate,
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
""".format(today_trade_date, today_trade_date, list_trade_date, day_5_before_trade_date, day_10_before_trade_date,
           day_20_before_trade_date))


def get_stock_daily_top_inst(trade_date, list_date):
    return db_tushare.query("""
    	select
	    T1.pct_chg,
	    T2.name,
	    T3.*
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
	join
	(
	        select *
	        from top_inst
	        where trade_date='{}'
	)T3 on (T1.ts_code=T3.ts_code)

    """.format(trade_date, trade_date, list_date, trade_date))

#! /usr/bin/env python
# *-* coding:utf-8 *-*

# 提前准备特征
import sys
import time
import datetime

from tushare_global_config import conn, cur, \
    get_valid_stock, is_valid_trade_date, LOG, LOG_INFO, perf, get_stock_daily_ts_code_list

STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY = {}


def check_all_download(trade_date, valid_stock_list):
    select_sql = """
                select distinct ts_code
                from tushare.realtime_action_detail_basic
                where trade_date=%s 
            """
    cur.execute(select_sql, (trade_date))
    select_result = cur.fetchall()
    download_code_list = []
    for item in select_result:
        download_code_list.append(item[0])

    new_ts_code_list = []
    for valid_stock in valid_stock_list:
        if valid_stock not in download_code_list:
            new_ts_code_list.append(valid_stock)
    LOG_INFO("check_all_download ", trade_date, str(valid_stock_list))
    LOG_INFO("check_all_download new_ts_code_list ", str(new_ts_code_list))

    if len(new_ts_code_list) > 0:
        LOG_INFO("need cal stock size ", str(len(new_ts_code_list)))
        return False, new_ts_code_list

    return True, []


BACK_TRACE_TRADE_DATE_NUM = 60  # 查询多长时间数据


def is_download_stock_realtime_action(ts_code, trade_date):
    pass
    start_time = time.time()
    select_sql = """
                select *
                from tushare.realtime_action_detail_basic
                where ts_code=%s and trade_date=%s 
            """
    cur.execute(select_sql, (ts_code, trade_date))
    select_result = cur.fetchall()
    LOG_INFO("check download cost time", time.time() - start_time)
    if len(select_result) > 0:
        LOG_INFO("is_download_stock_realtime_action ", ts_code, trade_date)
        return True
    return False


# 检查是否全部下载完，返回结果和需要下载new code list


# 插入实时交易一天计算后的特征
def insert_stock_realtime_action_detail_basic(ts_code='', start_trade_date=''):
    pass
    ts_code_simple = str(ts_code).replace('.', '')
    sql = """ 
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
    	            select 
                             T1.*,T2.open,T2.high,T2.close
    	            from
    	            (
    	                select 
                                ts_code,trade_date,trade_time,price,price_change,volumn,value,kind
    	                from akshare.stock_realtime_action_""" + ts_code_simple + """
    	                where trade_date=%s
    	                group by ts_code,trade_date,trade_time,price,price_change,volumn,value,kind
    	    	    )T1
    	            join
    	            (
    	                select *
    	                from tushare.stock_daily
    	                where trade_date=%s and ts_code=%s
    	            )T2 on (T1.trade_date=T2.trade_date)
    	        )T3
    	        group by trade_date
              )T4
            """
    cur.execute(sql, (start_trade_date, start_trade_date, ts_code))
    result = cur.fetchall()
    LOG_INFO("execute sql ", start_trade_date, ts_code, 'result', len(result))
    for row in result:
        insert_sql = """
                    insert into tushare.realtime_action_detail_basic 
                    (`ts_code`,`trade_date`,`avg_price`,`avg_trade_price`,`std_price`,
                    `buy_kind_volumn_rate`,`sell_kind_volumn_rate`,`neutral_kind_volumn_rate`,
                    `profit_volumn_rate`,`lose_volumn_rate`,`equal_volumn_rate`)

                    values
                    (   %s,%s,%s,%s,%s,
                        %s,%s,%s,
                        %s,%s,%s
                    )
                """
        cur.execute(insert_sql, (
            str(ts_code),
            str(row[0]),
            str(row[1]),
            str(row[2]),
            str(row[3]),
            str(row[4]),
            str(row[5]),
            str(row[6]),
            str(row[7]),
            str(row[8]),
            str(row[9])
        ))
        conn.commit()
        perf(namespace='realtime_action_detail_basic', subtag='insert', extra=ts_code)


def download_stock_realtime_action_detail_basic_in_memory(start_trade_date='', end_trade_date='', ts_code_list=[],
                                                          hashmod=0, value=0):
    # 获取股票实时交易行为的汇总基础信息
    # trade_date,平均每秒钟价格，平均成交价格，每秒钟价格方差，买盘数量，买盘数量，截止收盘，当天赚钱交易量占当天比例，当天赔钱交易量占当天比例
    LOG.info('select_stock_realtime_action_detail_basic_in_mysql' + ' hashmod' + hashmod + 'value' + value)
    start_time = time.time()
    global STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY
    download_ts_code_num = 0
    for ts_code in ts_code_list:
        if int(hash(ts_code)) % int(hashmod) != int(value):
            continue
        if is_download_stock_realtime_action(ts_code=ts_code, trade_date=start_trade_date):
            continue
        download_ts_code_num += 1
        insert_stock_realtime_action_detail_basic(ts_code=ts_code, start_trade_date=start_trade_date)

        LOG_INFO(start_trade_date, " select_stock_realtime_action_daily_basic fetch time"
                 , str(time.time() - start_time), str(download_ts_code_num),
                 ' hashmod', str(hashmod), 'value', str(value))
    LOG_INFO("select_stock_realtime_action_daily_basic total fetch time", str(time.time() - start_time),
             ' hashmod', str(hashmod), ' value', str(value))


if __name__ == '__main__':
    start_time = time.time()
    LOG.info("股市有风险，入市需谨慎")
    LOG.info("目标翻一倍")
    LOG.info('参数个数为:' + str(len(sys.argv)) + '个参数')
    hashmod = sys.argv[1]
    value = sys.argv[2]
    start_date = sys.argv[3]
    if not is_valid_trade_date(start_date):
        LOG.info(" not valid trade date finish " + start_date)
        sys.exit(0)
    # 计算当天实时交易的特征
    valid_stock_list = get_stock_daily_ts_code_list(trade_date=start_date)
    is_all_calculate, new_stock_list = check_all_download(trade_date=start_date, valid_stock_list=valid_stock_list)
    download_cnt = 1
    LOG_INFO("need calc", new_stock_list)
    while not is_all_calculate:
        download_cnt += 1
        if download_cnt > 100:
            break
        LOG.info(valid_stock_list)
        today = datetime.datetime.now()

        download_stock_realtime_action_detail_basic_in_memory(start_trade_date=start_date,
                                                              ts_code_list=new_stock_list,
                                                              hashmod=hashmod, value=value)
        LOG.info("Total cost:" + str(time.time() - start_time))
        is_all_calculate, new_stock_list = check_all_download(start_date=start_date, valid_stock_list=valid_stock_list)
    LOG.info("finish create feature pre")
    sys.exit(0)

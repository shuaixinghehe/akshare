#! /usr/bin/env python
# *-* coding:utf-8 *-*
import time

from tushare_global_config import LOG_INFO, stock_basic_fileds, cur, stock_basic_fileds_list, LOG_ERROR, LOG, \
    get_stock_daily_trade_date, get_valid_stock

STOCK_DAILY_BASIC_MEMORY = {}


def download_stock_daily_basic_in_memory(start_trade_date='', end_trade_date='', ts_code_list=[]):
    LOG_INFO("获取股票基本信息,换手率，成交量信息")
    global STOCK_DAILY_BASIC_MEMORY
    LOG_INFO("download_stock_daily_basic_in_memory," + start_trade_date)
    start_time = time.time()
    sql = "select " + stock_basic_fileds + " from stock_daily_basic where trade_date>=%s and ts_code in ("
    for ts_code in ts_code_list:
        sql += "'" + ts_code + "',"
    sql = sql[:-1]
    sql += ") order by ts_code,trade_date desc"
    stock_daily_basic_memory = {}
    cur.execute(sql, (start_trade_date))
    result = cur.fetchall()
    run_num = 0
    for row in result:
        STOCK_DAILY_BASIC_MEMORY[str(row[0]) + "_" + row[1]] = {}
        feature_map = {}
        run_num += 1
        if run_num % 10000 == 0:
            LOG_INFO("download_stock_daily_basic_in_memory", round(run_num * 1.0 / len(result), 4))
        for index in range(0, len(stock_basic_fileds_list)):
            if index >= 0 and index <= 1:
                feature_map[stock_basic_fileds_list[index]] = row[index]
            elif index > 1:
                try:
                    if row[index] is None or row[index] == "None":
                        # LOG_INFO("stock basic is None", "index", index, row)
                        feature_map[stock_basic_fileds_list[index]] = 0.0
                    else:
                        feature_map[stock_basic_fileds_list[index]] = float(row[index])
                except Exception as  e:
                    LOG_ERROR(row, e, str(e))
            else:
                LOG_ERROR("不会运行，如果运行的话，就出错了")
                feature_map[stock_basic_fileds_list[index]] = 0.0
        STOCK_DAILY_BASIC_MEMORY[str(row[0]) + "_" + str(row[1])] = feature_map
    LOG_INFO("download_stock_daily_basic_in_memory fetch time", str(time.time() - start_time), str(
        len(stock_daily_basic_memory)))
    LOG_INFO("stock_daily_basic_memory len ", len(stock_daily_basic_memory))
    for key in stock_daily_basic_memory.keys():
        LOG_INFO("download stock_daily_basic_memory key:", key)
    return STOCK_DAILY_BASIC_MEMORY


if __name__ == '__main__':
    pass
    # download_stock_realtime_action_detail_basic_in_memory()
    # 获取需要计算的日期,回溯多长时间
    LOG_INFO("开始计算训练数据")
    back_trace_trade_date_list = get_stock_daily_trade_date()
    # 根据交易日list，获取最近BACK_TRACE_TRADE_DATE_NUM 的日期
    # back_trace_start_trade_date = back_trace_trade_date_list[BACK_TRACE_TRADE_DATE_NUM]
    # 获取需要计算的股票，
    # 条件最近每天都可以交
    valid_stock_list = get_valid_stock(back_trace_trade_date_list[60], today_date=back_trace_trade_date_list[0])
    LOG_INFO("可以回溯的交易日:", len(back_trace_trade_date_list))
    LOG_INFO("开始交易日", back_trace_trade_date_list[0], '结束交易日', back_trace_trade_date_list[60])
    LOG_INFO("可以回溯的股票:", len(valid_stock_list))
    download_stock_daily_basic_in_memory(start_trade_date=back_trace_trade_date_list[60],
                                         ts_code_list=valid_stock_list)
    LOG_INFO("STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY", len(STOCK_DAILY_BASIC_MEMORY.keys()))

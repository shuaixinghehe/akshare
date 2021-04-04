#! /usr/bin/env python
# *-* coding:utf-8 *-*
import time

from tushare_global_config import LOG_INFO, ak_share_realtime_action_fileds, cur, ak_share_realtime_action_fileds_list, \
    LOG_ERROR, get_stock_daily_trade_date, get_valid_stock

STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY = {}


def download_stock_realtime_action_detail_basic_in_memory(start_trade_date='', end_trade_date='', ts_code_list=[]):
    pass
    # 获取股票实时交易行为的汇总基础信息
    # trade_date,平均每秒钟价格，平均成交价格，每秒钟价格方差，买盘数量，买盘数量，截止收盘，当天赚钱交易量占当天比例，当天赔钱交易量占当天比例
    LOG_INFO("获取股票实时交易行为的汇总基础信息")
    LOG_INFO("trade_date,平均每秒钟价格，平均成交价格，每秒钟价格方差，买盘数量，买盘数量，截止收盘，当天赚钱交易量占当天比例，当天赔钱交易量占当天比例")
    LOG_INFO('download_stock_realtime_action_detail_basic_in_memory')
    start_time = time.time()
    global STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY
    sql = "select  " + ak_share_realtime_action_fileds + \
          " from tushare.realtime_action_detail_basic where trade_date>=%s and ts_code in ("
    for ts_code in ts_code_list:
        sql += "'" + ts_code + "',"
    sql = sql[:-1]
    sql += ") order by ts_code,trade_date desc"

    cur.execute(sql, (start_trade_date))
    result = cur.fetchall()
    num = 0
    for row in result:
        STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY[str(row[0]) + "_" + str(row[1])] = {}
        feature_map = {}
        num += 1
        if num % 10000 == 0:
            LOG_INFO("download_stock_realtime_action_detail_basic_in_memory process", num,
                     round(num * 1.0 / len(result), 2))
        for index in range(0, len(ak_share_realtime_action_fileds_list)):
            if index >= 0 and index <= 1:
                feature_map[ak_share_realtime_action_fileds_list[index]] = row[index]
            elif index > 1:
                try:
                    feature_map[ak_share_realtime_action_fileds_list[index]] = float(row[index])
                except Exception as e:
                    LOG_ERROR(row, e, str(e))
            else:
                feature_map[ak_share_realtime_action_fileds_list[index]] = 0.0
        STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY[str(row[0]) + "_" + str(row[1])] = feature_map
    LOG_INFO("download_stock_realtime_action_daily_basic fetch time", time.time() - start_time, len(
        STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY))

    LOG_INFO("【下载完成】股票实时交易行为的汇总基础信息", len(STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY.keys()))
    return STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY


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
    download_stock_realtime_action_detail_basic_in_memory(start_trade_date=back_trace_trade_date_list[60],
                                                          ts_code_list=valid_stock_list)
    LOG_INFO("STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY", len(STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY.keys()))

#! /usr/bin/env python
# *-* coding:utf-8 *-*
import time

from tushare_global_config import LOG_INFO, stock_basic_fileds, cur, stock_basic_fileds_list, LOG_ERROR, LOG, \
    stock_daily_fileds, stock_daily_fileds_list

STOCK_DAILY_MEMORY = {}


# 获取最高 最低 开盘 收盘 价格
def download_stock_daily_in_memory(start_trade_date='', end_trade_date='', ts_code_list=[]):
    LOG_INFO("股票基本信息，开盘价格 收盘价格 成交量")
    LOG.info("download_stock_daily_in_memory " + start_trade_date)
    start_time = time.time()
    global STOCK_DAILY_MEMORY
    sql = "select " + stock_daily_fileds + " from stock_daily where trade_date>=%s and ts_code in ("
    for ts_code in ts_code_list:
        sql += "'" + ts_code + "',"
    sql = sql[:-1]
    sql += ") group by " + stock_daily_fileds + " order by ts_code,trade_date desc"
    cur.execute(sql, (start_trade_date))
    result = cur.fetchall()
    run_num = 0
    for row in result:
        STOCK_DAILY_MEMORY[str(row[0]) + "_" + row[1]] = {}
        feature_map = {}
        run_num += 1
        for index in range(0, len(stock_daily_fileds_list)):
            if index >= 0 and index <= 1:
                feature_map[stock_daily_fileds_list[index]] = row[index]
            elif index > 1:
                feature_map[stock_daily_fileds_list[index]] = float(row[index])
            else:
                feature_map[stock_daily_fileds_list[index]] = 0.0
        STOCK_DAILY_MEMORY[str(row[0]) + "_" + row[1]] = feature_map
    LOG.info("download_stock_daily_in_memory fetch time ", str(time.time() - start_time), str(
        len(STOCK_DAILY_MEMORY)), str(len(STOCK_DAILY_MEMORY)))
    for key in STOCK_DAILY_MEMORY.keys():
        LOG_INFO('download_stock_daily_in_memory key:', key)
    return STOCK_DAILY_MEMORY


if __name__ == '__main__':
    pass

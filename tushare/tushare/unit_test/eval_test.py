#! /usr/bin/env python
# *-* coding:utf-8 *-*
import datetime

from module.create_feature import BACK_TRACE_TRADE_DATE_NUM
from module.tushare_global_config import get_valid_stock


def test():
    today = datetime.datetime.now()
    start_trade_date = (today + datetime.timedelta(-1 * BACK_TRACE_TRADE_DATE_NUM * 2)).strftime("%Y%m%d")
    valid_stock_list = get_valid_stock(start_trade_date)

    # print "today", today, 'start_date', start_trade_date
    # stock_daily_basic_memory = download_stock_daily_basic_in_memory(start_trade_date=start_trade_date,
    #                                                                 ts_code_list=valid_stock_list)
    # valid_trade_date_list, start_feature_trade_date, end_feature_trade_date = get_stock_daily_trade_date(
    #     start_trade_date=start_trade_date,
    #     limit=BACK_TRACE_TRADE_DATE_NUM)
    # print 'valid_trade_date_list', valid_trade_date_list
    # print 'start_feature_trade_date', start_feature_trade_date
    # print 'end_feature_trade_date', end_feature_trade_date



if __name__ == '__main__':
    test()

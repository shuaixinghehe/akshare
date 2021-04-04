#! /usr/bin/env python
# *-* coding:utf-8 *-*
import os, sys

LOCAL_SYS_PATH = ['/Users/beacherlu/Workspace/akshare/tushare/tushare/module',
                  '/Users/beacherlu/Workspace/akshare',
                  '/Users/beacherlu/Workspace/akshare/tushare/tushare/module',
                  '/Users/beacherlu/Workspace/akshare/tushare/tushare', ]
for p in LOCAL_SYS_PATH:
    sys.path.append(p)
print("sys.path", sys.path)

from index_daily import download_index_daily

from tushare_utils import LOG, perf
import tushare_check_data_utils
from stock_basic import download_stock_basic
from stock_daily import download_stock_daily
from stock_daily_basic import download_stock_daily_basic
from top_inst import download_top_inst
from feature_create_stock_money_flow import download_stock_money_flow

# sys.setdefaultencoding('utf8')

# 下载数据，判断逻辑
if __name__ == '__main__':
    # 返回应该下载的表数据
    perf(namespace="a_download_tushare_data", subtag='start')
    need_download_map = tushare_check_data_utils.get_need_downloaded()
    for trade_date in sorted(need_download_map.keys()):
        print(trade_date, need_download_map[trade_date])
        for info_type in need_download_map[trade_date]:
            if info_type == "stock_basic":
                perf(namespace="a_download_tushare_data", subtag='stock_basic', extra=trade_date)
                download_stock_basic(trade_date)
            elif info_type == "stock_daily":
                perf(namespace="a_download_tushare_data", subtag='stock_daily', extra=trade_date)
                download_stock_daily(trade_date)
            elif info_type == "stock_daily_basic":
                perf(namespace="a_download_tushare_data", subtag='stock_daily_basic', extra=trade_date)
                download_stock_daily_basic(trade_date)
            elif info_type == 'top_inst':
                perf(namespace="a_download_tushare_data", subtag='top_inst', extra=trade_date)
                download_top_inst(trade_date)
            elif info_type == 'money_flow':
                perf(namespace="a_download_tushare_data", subtag='money_flow', extra=trade_date)
                download_stock_money_flow(trade_date)
            # elif info_type == 'index_daily':
            #     perf(namespace="a_download_tushare_data", subtag='index_daily', extra=trade_date)
            #     download_index_daily(trade_date)
            else:
                perf(namespace="a_download_tushare_data", subtag='unkown_type', extra=trade_date)
                print("error info Type")
    LOG.info("finish")

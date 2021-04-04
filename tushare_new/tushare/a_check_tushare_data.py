#! /usr/bin/env python
# *-* coding:utf-8 *-*
import sys

import module.tushare_check_data_utils
from module.stock_basic import download_stock_basic
from module.stock_daily import download_stock_daily
from module.stock_daily_basic import download_stock_daily_basic
from module.stock_money_flow import download_stock_money_flow
from module.top_inst import download_top_inst

reload(sys)
sys.setdefaultencoding('utf8')

# 下载数据，判断逻辑
# 检查下载的数据
if __name__ == '__main__':
    #
    need_download_map = module.tushare_check_data_utils.get_need_downloaded()
    for trade_date in sorted(need_download_map.keys()):
        print (trade_date, need_download_map[trade_date])
        for info_type in need_download_map[trade_date]:
            if info_type == "stock_basic":
                download_stock_basic(trade_date)
            elif info_type == "stock_daily":
                download_stock_daily(trade_date)
            elif info_type == "stock_daily_basic":
                download_stock_daily_basic(trade_date)
            elif info_type == 'top_inst':
                download_top_inst(trade_date)
            elif info_type == 'money_flow':
                download_stock_money_flow(trade_date)
            else:
                print ("error info Type")

#! /usr/bin/env python
# *-* coding:utf-8 *-*
import sys
import time

import pymysql.cursors
import tushare as ts

from tushare_global_config import stock_money_flow_fileds, stock_money_flow_fileds_list, VALID_TRADE_DATE_LIST
from tushare_utils import LOG_INFO, perf

# reload(sys)
# sys.setdefaultencoding('utf8')

ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="tushare", \
                       charset='utf8')
cur = conn.cursor()


if __name__ == '__main__':
    pass
    today_date = time.strftime("%Y%m%d", time.localtime())
    print(today_date)
    # download_stock_money_flow('20200612')

# coding:utf8
import datetime
import sys
import time

import akshare as ak
import pymysql.cursors
from download_stock_daily_data_once import history_stock_daily


def offline_stock_daily():
    pass
    ofile = open('./download_fuquan.txt')
    for line in ofile:
        line = line.strip()
        print(line.strip())
        adjust = line.split(' ')[0]
        ts_code = line.split(' ')[1]
        trade_date = line.split(' ')[2]
        history_stock_daily(ts_code=ts_code, trade_date=trade_date, adjust=adjust)


def offline_realtime_action():
    pass
    ofile = open('./offline_action_day.txt')
    for line in ofile:
        line = line.strip()
        print(line)


if __name__ == '__main__':
    pass
    # offline_stock_daily()
    offline_realtime_action()

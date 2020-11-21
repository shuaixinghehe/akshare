# coding:utf8
import datetime
import sys
import time

import akshare as ak
import pymysql.cursors
from download_stock_daily_data_once import history_stock_daily
from download_realtime_action_data_once import check_realtime_action_data
from download_realtime_action_data_once import is_download_realtime_stock_action
from download_realtime_action_data_once import realtime_stock_detail


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
    # table_name_download_map = check_realtime_action_data()
    table_name_download_map = {}
    ofile = open('./download_realtime_action.txt')
    for line in ofile:
        line = line.strip()
        table_name_download_map[line.split(" ")[0]] = line.split(" ")[1]
    for key in table_name_download_map.keys():
        print(key, table_name_download_map[key])
    download_trade_date_list = []
    ofile = open('./offline_action_day.txt')
    for line in ofile:
        line = line.strip()
        print(line)
        download_trade_date_list.append(line)

    for key in table_name_download_map.keys():
        ts_code = key.split('_')[3][0:6] + "." + key.split('_')[3][6:]
        if int(table_name_download_map[key]) == 0 or int(table_name_download_map[key]) == 40:
            continue
        for trade_date in download_trade_date_list:
            if not is_download_realtime_stock_action(trade_date=trade_date, ts_code=ts_code):
                realtime_stock_detail(ts_code=ts_code, trade_date=trade_date)


if __name__ == '__main__':
    pass
    # offline_stock_daily()
    offline_realtime_action()
    print("stock_realtime_action_000009SZ".split("_")[3][0:6] + ".")
    print("stock_realtime_action_000009SZ".split("_")[3][6:] + "")

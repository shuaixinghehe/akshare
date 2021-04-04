#! /usr/bin/env python
# *-* coding:utf-8 *-*
import sys
import time

import pymysql.cursors
import tushare as ts
import os, sys

LOCAL_SYS_PATH = ['/Users/beacherlu/Workspace/akshare/tushare/tushare/module',
                  '/Users/beacherlu/Workspace/akshare',
                  '/Users/beacherlu/Workspace/akshare/tushare/tushare/module',
                  '/Users/beacherlu/Workspace/akshare/tushare/tushare', ]
for p in LOCAL_SYS_PATH:
    sys.path.append(p)
print("sys.path", sys.path)

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

conn_tencent = pymysql.connect(host="49.235.90.127", user="tushare", \
                               password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                               db="tushare", \
                               charset='utf8')
cur_tencent = conn.cursor()


# 回溯日线行情
def download_stock_daily(trade_date=''):
    sql = """
    insert into stock_daily (
         `ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`
    )
    values
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );
    """
    if len(trade_date) == 0:
        return
    is_need_downloaded = True
    while is_need_downloaded:
        try:
            df = pro.daily(trade_date=trade_date)
            time.sleep(1)
            is_need_downloaded = False
        except Exception as e:
            print("retry daily", repr(e))  # 回溯历史情况

    for index, row in df.iterrows():
        result = cur.execute(sql, (
            str(row['ts_code']).encode('utf-8'),
            str(row['trade_date']).encode('utf-8'),
            str(row['open']).encode('utf-8'),
            str(row['high']).encode('utf-8'),
            str(row['low']).encode('utf-8'),
            str(row['close']).encode('utf-8'),
            str(row['pre_close']).encode('utf-8'),
            str(row['change']).encode('utf-8'),
            str(row['pct_chg']).encode('utf-8'),
            str(row['vol']).encode('utf-8'),
            str(row['amount']).encode('utf-8')
        ))
        conn.commit()
        LOG_INFO("download_stock_daily", row['ts_code'], row['trade_date'], result)
        perf(namespace='stock_daily', subtag=row['ts_code'])


if __name__ == '__main__':
    pass
    print('参数个数为:', len(sys.argv), '个参数。')
    print('参数列表:', str(sys.argv))
    today_date = sys.argv[1]
    # today_date = time.strftime("%Y%m%d", time.localtime())
    print(today_date)
    download_stock_daily(today_date)

#! /usr/bin/env python
# *-* coding:utf-8 *-*
import sys
import time

import pymysql.cursors
import tushare as ts
import sys
LOCAL_SYS_PATH = ['/Users/beacherlu/Workspace/akshare/tushare/tushare/module',
                  '/Users/beacherlu/Workspace/akshare',
                  '/Users/beacherlu/Workspace/akshare/tushare/tushare/module',
                  '/Users/beacherlu/Workspace/akshare/tushare/tushare', ]
for p in LOCAL_SYS_PATH:
    sys.path.append(p)
print("sys.path", sys.path)

# reload(sys)
# sys.setdefaultencoding('utf8')

ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="tushare", \
                       charset='utf8')
# CREATE USER 'tushare'@'127.0.0.1' IDENTIFIED BY '&QwX0^4#Sm^&t%V6wBnZC%78';
# GRANT all privileges ON tushare.* TO 'tushare'@'127.0.0.1';
cur = conn.cursor()

conn_tencent = pymysql.connect(host="49.235.90.127", user="tushare", \
                               password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                               db="tushare", \
                               charset='utf8')
cur_tencent = conn.cursor()

need_download_index_code = [
    '399001.SZ',  # 深证成指
    '000001.SH',  # 上证指数
    '000016.SH',  # 上证50
]
from tushare_utils import LOG_INFO, perf


def download_index_daily(stock_date=''):
    df = pro.index_basic(market='SZSE')
    for index, row in df.iterrows():
        download_index_daily_detail(start_trade_date=stock_date, end_trade_date=stock_date,
                                    index_ts_code=row['ts_code'])

    df = pro.index_basic(market='SSE')
    for index, row in df.iterrows():
        download_index_daily_detail(start_trade_date=stock_date, end_trade_date=stock_date,
                                    index_ts_code=row['ts_code'])


# 回溯日线行情
def download_index_daily_detail(start_trade_date='', end_trade_date='', index_ts_code=''):
    sql = """
    insert into index_daily (
         `ts_code`, `trade_date`, `close`, `open`, `high`, `low`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`
    )
    values
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );
    """
    if len(start_trade_date) == 0:
        return
    is_need_downloaded = True
    while is_need_downloaded:
        try:
            df = pro.index_daily(ts_code=index_ts_code, start_date=start_trade_date, end_date=end_trade_date)
            time.sleep(1)
            is_need_downloaded = False
        except Exception as e:
            print("retry daily", repr(e))  # 回溯历史情况

    for index, row in df.iterrows():
        result = cur.execute(sql, (
            str(row['ts_code']).encode('utf-8'),
            str(row['trade_date']).encode('utf-8'),
            str(row['close']).encode('utf-8'),
            str(row['open']).encode('utf-8'),
            str(row['high']).encode('utf-8'),
            str(row['low']).encode('utf-8'),
            str(row['pre_close']).encode('utf-8'),
            str(row['change']).encode('utf-8'),
            str(row['pct_chg']).encode('utf-8'),
            str(row['vol']).encode('utf-8'),
            str(row['amount']).encode('utf-8')
        ))
        conn.commit()
        perf(namespace='download_index_daily_detail', subtag=row['ts_code'])
        LOG_INFO("download_index_daily_detail", row['ts_code'], row['trade_date'], result)


if __name__ == '__main__':
    pass
    today_date = time.strftime("%Y%m%d", time.localtime())
    print
    today_date
    download_index_daily(stock_date='20200825')
    download_index_daily(stock_date='20200826')
    download_index_daily(stock_date='20200827')
    download_index_daily(stock_date='20200828')
    download_index_daily(stock_date='20200831')
    download_index_daily(stock_date='20200901')
    download_index_daily(stock_date='20200902')
    # download_index_daily(start_trade_date='20200101', end_trade_date='20200807', index_ts_code='399001.SZ')
    # df = pro.index_basic(market='SZSE')
    # for index, row in df.iterrows():
    #     download_index_daily_detail(start_trade_date='20200101', end_trade_date='20200820',
    #                                 index_ts_code=row['ts_code'])
    #
    # df = pro.index_basic(market='SSE')
    # for index, row in df.iterrows():
    #     download_index_daily_detail(start_trade_date='20200101', end_trade_date='20200820',
    #                                 index_ts_code=row['ts_code'])

#! /usr/bin/env python
# *-* coding:utf-8 *-*
import datetime
import time
import tushare as ts
import pymysql.cursors
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


# 查询当前所有正常上市交易的股票列表
def download_stock_basic(stock_date=''):
    is_need_downloaded = True

    while is_need_downloaded:
        try:
            data = pro.stock_basic(exchange='', list_status='L',
                                   fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
            time.sleep(1)
            is_need_downloaded = False
        except Exception as e:
            print("retry download_stock_basic")

    sql = """
    insert into stock_basic (
        dt,ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs
    )
    values
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """
    for index, row in data.iterrows():
        result = cur.execute(sql, (
            stock_date,
            str(row['ts_code']).encode('utf-8'),
            str(row['symbol']).encode('utf-8'),
            str(row['name']).encode('utf-8'),
            str(row['area']).encode('utf-8'),
            str(row['industry']).encode('utf-8'),
            str(row['fullname']).encode('utf-8'),
            str(row['enname']).encode('utf-8'),
            str(row['market']).encode('utf-8'),
            str(row['exchange']).encode('utf-8'),
            str(row['curr_type']).encode('utf-8'),
            str(row['list_status']).encode('utf-8'),
            str(row['list_date']).encode('utf-8'),
            str(row['delist_date']).encode('utf-8'),
            str(row['is_hs']).encode('utf-8')
        ))
        conn.commit()
        LOG_INFO("download_stock_basic", row['ts_code'], row['symbol'], result)
        perf(namespace='stock_basic', subtag=row['ts_code'])


if __name__ == '__main__':
    pass
    print('参数个数为:', len(sys.argv), '个参数。')
    print('参数列表:', str(sys.argv))
    today_date = sys.argv[1]
    # value = sys.argv[2]
    # today_date = time.strftime("%Y%m%d", time.localtime())
    print(today_date)
    download_stock_basic(today_date)

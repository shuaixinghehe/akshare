#! /usr/bin/env python
# *-* coding:utf-8 *-*
import sys
import time

import pymysql.cursors
import tushare as ts

reload(sys)
sys.setdefaultencoding('utf8')

ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="akshare", \
                       charset='utf8')
cur = conn.cursor()


def get_ak_share_action_data():
    pass
    ak_feature_map = {}
    stock_daily_map = {}

    sql = "select ts_code,trade_date,price,volumn,kind from stock_realtime_action"

    cur.execute(sql, ())

    result = cur.fetchall()

    cnt = 0
    start_time = time.time()
    for row in result:
        cnt += 1
        if cnt % 100 == 0:
            print  row
            print("time cost", time.time() - start_time)


if __name__ == '__main__':
    pass
    print "start"
    get_ak_share_action_data()

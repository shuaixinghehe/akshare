#! /usr/bin/env python
# *-* coding:utf-8 *-*
import datetime
import time
import tushare as ts
import pymysql.cursors
import sys

# reload(sys)
# sys.setdefaultencoding('utf8')

ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="tushare", \
                       charset='utf8')
cur = conn.cursor()


def download_top_inst(trade_date=''):
    sql = """
            insert into top_inst (
                 `trade_date`, `ts_code`, `exalter`, `buy`,
                 `buy_rate`, `sell`, `sell_rate`, `net_buy`
            )
            values
            (%s, %s, %s, %s, %s, %s, %s, %s);
            """
    is_need_downloaded = True
    while is_need_downloaded:
        try:
            df = pro.top_inst(trade_date=trade_date,
                              fields='trade_date,ts_code,exalter,buy,buy_rate,sell,sell_rate,net_buy')
            time.sleep(2)
            is_need_downloaded = False
        except Exception as  e:
            print("retry stock_daily_basic")

    for index, row in df.iterrows():
        # print row
        result = cur.execute(sql, (
            str(row['trade_date']).encode('utf-8'),
            str(row['ts_code']).encode('utf-8'),
            str(row['exalter']).encode('utf-8'),
            str(row['buy']).encode('utf-8'),
            str(row['buy_rate']).encode('utf-8'),
            str(row['sell']).encode('utf-8'),
            str(row['sell_rate']).encode('utf-8'),
            str(row['net_buy']).encode('utf-8')
        ))
        print
        "download_top_inst", row['ts_code'], row['trade_date'], result
        conn.commit()
        # time.sleep(1)


if __name__ == '__main__':
    pass
    today_date = time.strftime("%Y%m%d", time.localtime())
    print
    today_date
    download_top_inst('20200327')

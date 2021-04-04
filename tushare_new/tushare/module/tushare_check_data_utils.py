#! /usr/bin/env python
# *-* coding:utf-8 *-*
import datetime
import time

import pymysql.cursors
import tushare as ts

ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="tushare", \
                       charset='utf8')

cur = conn.cursor()

NEED_DOWWLOAD_MAP = {}
NEED_CHECK_TABLE_NAME_LIST = [
    'stock_basic',
    'stock_daily',
    'stock_daily_basic',
    'top_inst',
    'money_flow',
    'index_daily'  # 指数信息
]
CHECK_LAST_DAYS_NUM = 60


# 查询工作日 最近一半月可以交易的工作日
def get_trade_cal():
    end_date = time.strftime("%Y%m%d", time.localtime())
    today = datetime.datetime.now()
    start_date = (today + datetime.timedelta((CHECK_LAST_DAYS_NUM * -1))).strftime("%Y%m%d")
    is_need_downloaded = True
    while is_need_downloaded:
        try:
            df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
            trade_date_list = []
            for index, row in df.iterrows():
                if row['is_open'] == 1 and row['cal_date'] not in trade_date_list:
                    trade_date_list.append(row['cal_date'])
            time.sleep(1)
            is_need_downloaded = False
        except Exception as e:
            print("retry get_trade_cal")
    # return False

    print("check date list", trade_date_list)
    return trade_date_list


def get_need_downloaded(dt=''):
    # 检查最近30天报表信息是否下载完成
    trade_date_list = get_trade_cal()
    for table_name in NEED_CHECK_TABLE_NAME_LIST:
        for trade_date in trade_date_list:
            if is_downloaded(trade_date, table_name):
                if trade_date in NEED_DOWWLOAD_MAP.keys():
                    NEED_DOWWLOAD_MAP[trade_date].append(table_name)
                else:
                    NEED_DOWWLOAD_MAP[trade_date] = []
                    NEED_DOWWLOAD_MAP[trade_date].append(table_name)
    return NEED_DOWWLOAD_MAP


# 通过传入的表名和时间，检查是否当天下载，适用于检查一天的数据一次被完整下载的情况
# 不适用于单条记录检查
def is_downloaded(dt='', table_name=''):
    pass
    sql = ""
    if table_name == "stock_basic":
        sql = "select * from " + table_name + " where dt=%s;"
    else:
        sql = "select * from " + table_name + " where trade_date=%s;"

    cur.execute(sql, (dt))
    result = cur.fetchall()
    print("check", dt, "downloaded ", table_name, len(result))
    if len(result) > 1:
        return False
    print("    need", dt, "downloaded ", table_name, len(result))
    return True


if __name__ == '__main__':
    pass
    # print get_trade_cal()
    # end_date = time.strftime("%Y%m%d", time.localtime())
    # today = datetime.datetime.now()
    # print end_date, today
    #
    # check_date_data_downloaded('20191222', 'stock_basic')
    # get_need_downloaded()
    # for trade_date in sorted(NEED_DOWWLOAD_MAP.keys()):
    #     print trade_date, NEED_DOWWLOAD_MAP[trade_date]

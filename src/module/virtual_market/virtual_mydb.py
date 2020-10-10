#! /usr/bin/env python
# *-* coding:utf-8 *-*

import datetime
import sys
import time

import akshare as ak
import pymysql.cursors

# 获取mysql等信息的配置
# 一些常量信息

ts_conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                          password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                          db="tushare", \
                          charset='utf8')

ts_cur = ts_conn.cursor()

ak_conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                          password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                          db="akshare", \
                          charset='utf8')

ak_cur = ak_conn.cursor()


# 获取股票价格
def get_code_price(code='', trade_date='', timestamp=''):
    ts_cur.execute('sql', '')


# 根据股票价格获取成交数量
def get_code_volumn_by_price(code='', trade_date='', timestamp='', price=''):
    pass

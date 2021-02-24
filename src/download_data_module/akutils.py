# coding:utf8
import signal
import datetime
import sys
import time

import akshare as ak
import pymysql.cursors
from multiprocessing import Process

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

monitor_conn = pymysql.connect(host="127.0.0.1", user="diabetes", \
                               password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                               db="monitor", \
                               charset='utf8')

monitor_cur = monitor_conn.cursor()


# 自定义超时异常
class TimeoutError(Exception):
    def __init__(self, msg):
        super(TimeoutError, self).__init__()
        self.msg = msg


def time_out(interval, callback):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError("run func timeout")

        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)  # interval秒后向进程发送SIGALRM信号
                result = func(*args, **kwargs)
                signal.alarm(0)  # 函数在规定时间执行完后关闭alarm闹钟
                return result
            except TimeoutError as e:
                raise TimeoutError("error")

        return wrapper

    return decorator


def timeout_callback(e):
    print(e.msg)


# 根据传入的trade_date，查询最近的code,
# 参数 is_today 判断是否是今天
def get_stock_code(trade_date, is_today=True):
    sql = """
            select
                distinct ts_code
            from stock_daily
            where trade_date =%s ;
        """
    if not is_today:
        sql = """
            select
                distinct ts_code
            from stock_daily
            where trade_date >=%s ;
        """
    ts_cur.execute(sql, (trade_date))
    result = ts_cur.fetchall()
    code_list = []
    for code in result:
        code_list.append(code[0])

    return code_list


def ts_code_2_ak_code(ts_code):
    code = ts_code.split('.')[0]
    market_prefix = ts_code.split('.')[1]
    return market_prefix.lower() + code


def get_realtime_action_download_code_by_date(trade_date):
    pass
    sql = """ 
        select ts_code from check_stock_realtime_action where trade_date=%s
    """
    ak_cur.execute(sql, ())
    result = ak_cur.fetchall()
    for item in result:
        pass


def perf(namespace='', subtag='', extra='', value=1):
    pass
    monitor_cur.execute("""
        insert into  akshare_run_log (namespace,subtag,extra,value) values 
        (%s,%s,%s,%s)
    """, (str(namespace), str(subtag), str(extra), str(value)))
    monitor_conn.commit()


if __name__ == '__main__':
    pass

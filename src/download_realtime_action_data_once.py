# coding:utf8
import datetime
import sys
import time

import akshare as ak
import pymysql.cursors
from akutils import time_out, timeout_callback

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
# 默认不复权的数据;
# qfq: 返回前复权后的数据;
# hfq: 返回后复权后的数据;
# hfq-factor: 返回后复权因子; hfq-factor: 返回前复权因子
adjust_list = ['hfq', 'qfq']


def ts_code_2_ak_code(ts_code):
    code = ts_code.split('.')[0]
    market_prefix = ts_code.split('.')[1]
    return market_prefix.lower() + code


def history_stock_daily(ts_code='', adjust=""):
    pass
    ak_code = ts_code_2_ak_code(ts_code)
    stock_zh_a_daily_hfq_df = ak.stock_zh_a_daily(symbol=ak_code, adjust=adjust)
    sql = """
    insert into akshare_daily (
        ts_code, trade_date, open, high, low, close, adjust, volume, outstanding_share, turnover )
    values
    (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s);
    """

    for index, row in stock_zh_a_daily_hfq_df.iterrows():
        stock_date = str(index).split(" ")[0].replace("-", '')
        result = ak_cur.execute(sql, (
            ts_code,
            stock_date,
            str(row['open']).encode('utf-8'),
            str(row['high']).encode('utf-8'),
            str(row['low']).encode('utf-8'),
            str(row['close']).encode('utf-8'),
            adjust,
            str(row['volume']).encode('utf-8'),
            str(row['outstanding_share']).encode('utf-8'),
            str(row['turnover']).encode('utf-8'),
        ))
        ak_conn.commit()
    return False


@time_out(10, timeout_callback)
def stock_zh_a_tick_tx_timeout(ak_code, trade_date):
    return ak.stock_zh_a_tick_tx(code=ak_code, trade_date=trade_date)


def realtime_stock_detail(ts_code, trade_date):
    pass
    ak_code = ts_code_2_ak_code(ts_code)
    is_retry_times = 5
    stock_zh_a_tick_tx_df = None
    while is_retry_times > 0:
        try:
            stock_zh_a_tick_tx_df = stock_zh_a_tick_tx_timeout(ak_code, trade_date)
            is_retry_times = 0
        except Exception as e:
            print("realtime_stock_detail error", "code:", ts_code, " date:", trade_date, e)
            time.sleep(1)
            is_retry_times -= 1

    sql = """
    insert into stock_realtime_action (
        ts_code, trade_date, trade_time, price, price_change, volumn, value, kind )
    values
    (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    if stock_zh_a_tick_tx_df is None:
        return 0

    for index, row in stock_zh_a_tick_tx_df.iterrows():
        result = ak_cur.execute(sql, (
            ts_code,
            trade_date,
            str(row['成交时间']).encode('utf-8'),
            str(row['成交价格']).encode('utf-8'),
            str(row['价格变动']).encode('utf-8'),
            str(row['成交量(手)']).encode('utf-8'),
            str(row['成交额(元)']).encode('utf-8'),
            str(row['性质']).encode('utf-8'),
        ))
        ak_conn.commit()
    return is_retry_times


def download_realtime_stock_action(trade_date, hashmod, value):
    code_list = get_stock_code(start_date)
    trade_date_list = get_stock_trade_date(trade_date)

    sql = """
        select trade_date,ts_code from stock_realtime_action where trade_date>=%s group by trade_date,ts_code;
    """

    ak_cur.execute(sql, (trade_date))

    result = ak_cur.fetchall()

    already_download_realtime_stock_map = {}
    for item in result:
        trade_date = item[0]
        ts_code = item[1]
        if trade_date in already_download_realtime_stock_map:
            already_download_realtime_stock_map[trade_date].append(ts_code)
        else:
            already_download_realtime_stock_map[trade_date] = []
            already_download_realtime_stock_map[trade_date].append(ts_code)
    print("already download ", already_download_realtime_stock_map)
    for code in code_list:
        if abs(hash(code)) % int(hashmod) != int(value):
            continue
        print("download_realtime_stock_action ", code, " hash(code)", hash(code), " mod", hashmod, " value", value)
        start_time = time.time()
        for trade_date_item in trade_date_list:
            if trade_date_item in already_download_realtime_stock_map \
                    and code in already_download_realtime_stock_map[trade_date_item]:
                print("skip download ", trade_date_item, "code", code)
                continue
            print('download', code, trade_date_item)
            realtime_stock_detail(code, trade_date_item)
        print("download_realtime_stock_action " + code + " cost" + str(time.time() - start_time))


def get_stock_trade_date(trade_date):
    pass
    sql = """
            select
                distinct trade_date
            from stock_daily
            where trade_date >=%s ;
        """
    ts_cur.execute(sql, (trade_date))
    result = ts_cur.fetchall()
    trade_date_list = []
    for trade_item in result:
        trade_date_list.append(trade_item[0])
    print("get_stock_trade_date " + str(trade_date_list))
    return trade_date_list


def get_already_download_stock(trade_date):
    pass


def get_stock_code(trade_date):
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


def dowload_stock_daily():
    code_list = get_stock_code(start_date)
    sql = """
           select ts_code, count(distinct adjust) cnt from akshare_daily group by ts_code having cnt>=2;
       """

    ak_cur.execute(sql, ())
    result = ak_cur.fetchall()
    for code in result:
        if code[0] in code_list:
            code_list.remove(code[0])
            print("already download " + code[0])
    print("ready to download " + str(len(code_list)) + " stocks")
    print("code_list" + str(code_list))

    print("code_list" + str(code_list))
    for ts_code in code_list:
        print("ts_code" + ts_code)
        for adjust in adjust_list:
            is_retry = True
            while (is_retry):
                try:
                    is_retry = history_stock_daily(ts_code, adjust)
                    # time.sleep(1)
                except Exception as e:
                    print(e)
                    is_retry = True


if __name__ == '__main__':
    print("股市有风险，入市需谨慎")
    print("目标翻一倍")
    print('参数个数为:', len(sys.argv), '个参数。')
    print('参数列表:', str(sys.argv))
    print(time.strftime("%Y%m%d", time.localtime()))
    today = datetime.datetime.now()
    start_date = (today + datetime.timedelta(-18)).strftime("%Y%m%d")
    hashmod = sys.argv[1]
    value = sys.argv[2]
    start_time = time.time()
    hashmod = 1
    value = 0
    # start_date =
    print("start_date", start_date, "mod:", hashmod, " value", value)
    download_realtime_stock_action(start_date, hashmod, value)
    print("Total cost ", time.time() - start_time)

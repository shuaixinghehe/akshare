# coding:utf8
import datetime
import sys
import time

import akshare as ak
import pymysql.cursors
from akutils import time_out, timeout_callback
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

# 默认不复权的数据;
# qfq: 返回前复权后的数据;
# hfq: 返回后复权后的数据;
# hfq-factor: 返回后复权因子; hfq-factor: 返回前复权因子
adjust_list = ['hfq', 'qfq']


def ts_code_2_ak_code(ts_code):
    code = ts_code.split('.')[0]
    market_prefix = ts_code.split('.')[1]
    return market_prefix.lower() + code


@time_out(5, timeout_callback)
def stock_zh_a_daily_timeout(symbol, adjust):
    if int(time.time()) % 2 == 0:
        return ak.stock_zh_kcb_daily(symbol=symbol, adjust=adjust)
    else:
        return ak.stock_zh_a_daily(symbol=symbol, adjust=adjust)


def history_stock_daily(ts_code='', adjust="", trade_date=''):
    pass
    ak_code = ts_code_2_ak_code(ts_code)
    is_retry_times = 5
    stock_zh_a_daily_hfq_df = None
    start_time = time.time()
    # while is_retry_times > 0:
    try:
        stock_zh_a_daily_hfq_df = stock_zh_a_daily_timeout(symbol=ak_code, adjust=adjust)
        is_retry_times = 0
    except Exception as e:
        print("error is_retry_times", is_retry_times, ts_code, adjust, trade_date)
        is_retry_times -= 1

    if stock_zh_a_daily_hfq_df is None:
        return True
    else:
        print("download from web", ts_code, " ", adjust, " cost:", time.time() - start_time)

    start_time = time.time()
    sql = """
    insert into akshare_daily (
        ts_code, trade_date, open, high, low, close, adjust, volume, outstanding_share, turnover )
    values
    (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s);
    """

    for index, row in stock_zh_a_daily_hfq_df.iterrows():
        stock_date = str(index).split(" ")[0].replace("-", '')
        if (trade_date != stock_date):
            continue
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
        print("insert table ", ts_code, " ", adjust, " cost:", time.time() - start_time)
    return False


def realtime_stock_detail(ts_code, trade_date):
    pass
    ak_code = ts_code_2_ak_code(ts_code)
    is_retry = True
    while is_retry:
        try:
            stock_zh_a_tick_tx_df = ak.stock_zh_a_tick_tx(code=ak_code, trade_date=trade_date)
            is_retry = False
        except Exception:
            print("realtime_stock_detail error", "code:", ts_code, " date:", trade_date)
            time.sleep(1)

    sql = """
    insert into stock_realtime_action (
        ts_code, trade_date, trade_time, price, price_change, volumn, value, kind )
    values
    (%s, %s, %s, %s, %s, %s, %s, %s);
    """

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
    return is_retry


def download_realtime_stock_action(trade_date, hashmod, value):
    code_list = get_stock_code(start_date)
    trade_date_list = get_stock_trade_date(trade_date)
    for code in code_list:
        if hash(code) % int(hashmod) != int(value):
            continue
        print("download_realtime_stock_action ", code, " hash(code)", hash(code), " mod", hashmod, " value", value)
        start_time = time.time()
        for trade_date_item in trade_date_list:
            print(code, trade_date_item)
            is_retry = True
            while is_retry:
                try:
                    is_retry = realtime_stock_detail(code, trade_date_item)
                except Exception:
                    print("retry download_realtime_stock_action " + code)
                    is_retry = True
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
    sql = """
             select ts_code ,count(distinct adjust) cnt from akshare_daily where trade_date=%s  group by ts_code having cnt>=2;
         """
    ak_cur.execute(sql, (trade_date))
    result = ak_cur.fetchall()
    already_download_code_list = []
    for code in result:
        already_download_code_list.append(code[0])
    return already_download_code_list


def check_realtime_action_data():
    pass
    # 检查实时数据完整


# 检查最近几个月的实时日志行为
def get_stock_trade_date(start_check_date=''):
    pass
    sql = """
            select
                 ts_code,trade_date
            from stock_daily
            where trade_date >=%s 
            group by ts_code, trade_date;
        """


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


def check_download_all_stock(start_date):
    code_list = get_stock_code(start_date)
    already_download_code_list = get_already_download_stock(start_date)
    code_list = list(set(code_list).difference(set(already_download_code_list)))
    if len(code_list) == 0:
        return False
    return True


def dowload_stock_daily(start_date, hashmod, value):
    code_list = get_stock_code(start_date)
    already_download_code_list = get_already_download_stock(start_date)
    for code in already_download_code_list:
        if code in code_list:
            code_list.remove(code)
            print("already download " + code)
    print("ready to download " + str(len(code_list)) + " stocks")
    download_cnt = 0
    for ts_code in code_list:
        if hash(ts_code) % int(hashmod) != int(value):
            continue
        print("\n")
        print("start \n dowload_stock_daily ts_code" + ts_code, " hashmod", hashmod, " value", value)
        start_time = time.time()
        download_cnt += 1
        for adjust in adjust_list:
            is_retry = history_stock_daily(ts_code, adjust, start_date)
        print("end dowload_stock_daily ts_code cost ", time.time() - start_time, ts_code, adjust, 'download cnt ',
              download_cnt)
        print("\n")


if __name__ == '__main__':
    start_time = time.time()
    print("股市有风险，入市需谨慎")
    print("目标翻一倍")
    print('参数个数为:', len(sys.argv), '个参数。')
    print('参数列表:', str(sys.argv))
    # print(time.strftime("%Y%m%d", time.localtime()))
    # today = datetime.datetime.now()
    # start_date = (today + datetime.timedelta(-2)).strftime("%Y%m%d")
    hashmod = sys.argv[1]
    value = sys.argv[2]
    start_date = sys.argv[3]
    # hashmod = 1
    # value = 0
    # start_date = '20200729'
    print("mod:", hashmod, " value", value, " start date", start_date)
    # for i in range(0, int(hashmod)):
    #    p1 = Process(target=dowload_stock_daily, args=(start_date, hashmod, value))  # 必须加,号
    #    # download_realtime_stock_action(start_date, hashmod, value)
    #    p1.start()
    while (check_download_all_stock(start_date)):
        dowload_stock_daily(start_date, hashmod, value)
        print("Total cost:", time.time() - start_time)

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


@time_out(10, timeout_callback)
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
    start_time = time.time()
    while is_retry_times > 0:
        try:
            stock_zh_a_tick_tx_df = stock_zh_a_tick_tx_timeout(ak_code, trade_date)
            is_retry_times = 0
        except Exception as e:
            print("realtime_stock_detail error", "code:", ts_code, " date:", trade_date, e)
            time.sleep(1)
            is_retry_times -= 1
    if stock_zh_a_tick_tx_df is None:
        print("ts_code", ts_code, "download fail")
        return None
    else:
        print("download ts_code from web", ts_code, trade_date, "cost", time.time() - start_time)
    start_time = time.time()
    sql = """ insert into stock_realtime_action_""" + str(ts_code).replace('.', '') + """ (
        ts_code, trade_date, trade_time, price, price_change, volumn, value, kind )
    values
    (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    insert_data_list = []
    for index, row in stock_zh_a_tick_tx_df.iterrows():
        insert_data_list.append(
            (
                ts_code,
                trade_date,
                str(row['成交时间']).encode('utf-8'),
                str(row['成交价格']).encode('utf-8'),
                str(row['价格变动']).encode('utf-8'),
                str(row['成交量(手)']).encode('utf-8'),
                str(row['成交额(元)']).encode('utf-8'),
                str(row['性质']).encode('utf-8'),
            )
        )
        # result = ak_cur.execute(sql, (
        #     ts_code,
        #     trade_date,
        #     str(row['成交时间']).encode('utf-8'),
        #     str(row['成交价格']).encode('utf-8'),
        #     str(row['价格变动']).encode('utf-8'),
        #     str(row['成交量(手)']).encode('utf-8'),
        #     str(row['成交额(元)']).encode('utf-8'),
        #     str(row['性质']).encode('utf-8'),
        # ))
    ak_cur.executemany(sql, insert_data_list)
    ak_conn.commit()
    print("insert ts_code ", ts_code, " total cost ", time.time() - start_time)
    return is_retry_times


def create_realtime_stock_action_table(ts_code):
    pass
    ts_code = str(ts_code).replace('.', '')
    sql = """
               CREATE TABLE if not exists `stock_realtime_action_""" + ts_code + """` (
           `ts_code` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
           `trade_date` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
           `trade_time` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
           `price` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
           `price_change` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
           `volumn` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
           `value` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
           `kind` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL
           )   ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
           """
    ak_cur.execute(sql, ())
    ak_conn.commit()
    print("create table stock_realtime_action_" + ts_code)


def get_realtime_stock_action_table_name_list():
    pass
    sql = "SHOW TABLES LIKE '%stock_realtime_action_%';"
    ak_cur.execute(sql)
    result = ak_cur.fetchall()
    print(result)
    table_name_list = []
    for row in result:
        # print(row[0])
        table_name_list.append(row[0])
    return table_name_list


def check_realtime_action_data():
    pass
    table_name_list = get_realtime_stock_action_table_name_list()
    for table_name in table_name_list:
        sql = """select count(distinct trade_date) cnt from """ + table_name
        ak_cur.execute(sql)
        result = ak_cur.fetchall()
        table_name_download_map = {}
        for row in result:
            table_name_download_map[table_name] = row[0]
            print(table_name, row[0])
    return table_name_download_map


def is_download_realtime_stock_action(trade_date, ts_code):
    pass
    ts_code = str(ts_code).replace('.', '')
    sql = "SHOW TABLES LIKE '%" + ts_code + "%';"
    # print(sql)
    ak_cur.execute(sql)
    result = ak_cur.fetchall()
    if len(result) == 0:
        # todo: create table
        create_realtime_stock_action_table(ts_code)
        return False
    sql = "select * from stock_realtime_action_" + ts_code + " where trade_date=%s"
    ak_cur.execute(sql, (trade_date))
    result = ak_cur.fetchall()
    if len(result) == 0:
        return False
    print("stock_realtime_action_" + ts_code, trade_date, "is downloaded")
    return True


def download_realtime_stock_action(trade_date, hashmod, value):
    code_list = get_stock_code(start_date)
    trade_date_list = []
    trade_date_list.append(trade_date)
    download_num = 0
    for code in code_list:
        download_num += 1
        if abs(hash(code)) % int(hashmod) != int(value):
            continue

        start_time = time.time()
        # 增加查重，如果已经存入到mysql里面了 就不再插入
        if not is_download_realtime_stock_action(trade_date, code):
            r = realtime_stock_detail(code, trade_date)
            print("process ", download_num * 1.0 / len(code_list), " ",
                  download_num, " download_realtime_stock_action ", code,
                  " hash(code)", hash(code), " mod", hashmod, " value", value)
            if r is not None:
                print("download ts_code ", code, " total cost:", str(time.time() - start_time))
        # print("download_realtime_stock_action " + code + " cost" + str(time.time() - start_time))


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


def get_stock_code(trade_date):
    sql = """
            select
                distinct ts_code
            from stock_daily
            where trade_date =%s ;
        """
    ts_cur.execute(sql, (trade_date))
    result = ts_cur.fetchall()
    code_list = []
    for code in result:
        code_list.append(code[0])

    return code_list


def dowload_stock_daily(input_start_date):
    code_list = get_stock_code(input_start_date)
    sql = """
           select ts_code, count(distinct adjust) cnt 
           from akshare_daily 
           where trade_date=%s
           group by ts_code having cnt>=2;
       """

    ak_cur.execute(sql, (input_start_date))
    result = ak_cur.fetchall()
    for code in result:
        if code[0] in code_list:
            code_list.remove(code[0])
    print("ready to download " + str(len(code_list)) + " stocks")
    print("code_list" + str(code_list))
    for ts_code in code_list:
        print("ts_code" + ts_code)
        for adjust in adjust_list:
            try:
                is_retry = history_stock_daily(ts_code, adjust)
                # time.sleep(1)
            except Exception as e:
                print(e)


def check_akshare_stock_daily(back_check_trade_date='20200620'):
    pass
    # 查找akshare daily 缺失个数,检查每天复权前后的stock 是否一致
    sql = """
       select trade_date,adjust,count(distinct ts_code)  ts_code_cnt
       from akshare.akshare_daily
       where trade_date>=%s
       group by trade_date,adjust; 
    """
    ak_cur.execute(sql, (back_check_trade_date))
    result = ak_cur.fetchall()
    download_stock_item_map = {}
    download_stock_trade_date_map = {}
    tushare_sql = """
        select trade_date,count(distinct ts_code ) cnt
        from tushare.stock_daily
        where trade_date>=%s 
        group by trade_date
    """

    for item in result:
        print('item', item)
        download_stock_item_map[item[0] + "_" + item[1]] = item[2]
        download_stock_trade_date_map[item[0]] = 1

    ts_cur.execute(tushare_sql, (back_check_trade_date))
    result = ts_cur.fetchall()
    tushare_trade_date_map = {}
    for item in result:
        print('item', item)
        tushare_trade_date_map[item[0]] = item[1]

    for key in download_stock_item_map.keys():
        print("key", key, "value", download_stock_item_map[key])

    for trade_date in download_stock_trade_date_map.keys():
        if download_stock_item_map[trade_date + "_" + "hfq"] == download_stock_item_map[trade_date + "_" + "qfq"] and \
                download_stock_item_map[trade_date + "_" + "hfq"] == tushare_trade_date_map[trade_date]:
            pass
        else:
            print("not match need redownload", trade_date, 'tushare download', tushare_trade_date_map[trade_date],
                  'akshare download', download_stock_item_map[trade_date + "_" + "hfq"],
                  download_stock_item_map[trade_date + "_" + "qfq"])
            dowload_stock_daily(trade_date)


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
    start_date = sys.argv[3]
    start_time = time.time()
    print("start_date", start_date, "mod:", hashmod, " value", value)
    check_akshare_stock_daily('20200620')
    print("Total cost ", time.time() - start_time)

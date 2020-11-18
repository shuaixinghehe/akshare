# coding:utf8
import datetime
import sys
import time

import akshare as ak
import pymysql.cursors
from multiprocessing import Process
from akutils import time_out, timeout_callback, get_stock_code, ts_code_2_ak_code

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


def get_realtime_action_stock_action_map():
    sql = """ select trade_date,ts_code,count(1)cnt 
        from check_stock_realtime_action  
        group by trade_date,ts_code """
    ak_cur.execute(sql, ())
    result = ak_conn.fetchall()
    realtime_action_map = {}
    for item in result:
        trade_date = item[0]
        ts_code = item[1]
        realtime_action_map[trade_date + "_" + ts_code] = 1

    return realtime_action_map


# 检查历史的股票realtime action 是否下载完成
# 传入一个起始检查的时间
def update_download_all_realtime_stock_action(start_trade_date):
    code_list = get_stock_code(start_trade_date, False)
    #download_realtime_action_map = get_realtime_action_stock_action_map()
    for ts_code in code_list:
        ts_code = str(ts_code).replace('.', '')
        print("update download code ", ts_code)
        sql = " select trade_date,ts_code,count(1) cnt from stock_realtime_action_" + str(
            ts_code) + " where trade_date>=%s group by trade_date,ts_code"
        try:
            ak_cur.execute(sql, (start_trade_date))
            result = ak_cur.fetchall()

            for item in result:
                download_code = item[1]
                download_trade_date = item[0]
                print("download code:", download_code, "download_trade_date:", download_trade_date)
                insert_sql = """ insert into check_stock_realtime_action
                (ts_code,trade_date,is_download) values (%s,%s,%s)  """
                ak_cur.execute(insert_sql, (download_code, download_trade_date, "1"))
                ak_conn.commit()
        except  Exception as e:
            pass


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
    # hashmod = 1
    # value = 0
    # start_date = '20200729'
    print("start_date", start_date, "mod:", hashmod, " value", value)
    update_download_all_realtime_stock_action(start_date)
    # check_realtime_action_data()
    # for i in range(0, hashmod):
    #    p1 = Process(target=download_realtime_stock_action, args=(start_date, hashmod, value))  # 必须加,号
    #    # download_realtime_stock_action(start_date, hashmod, value)
    #    p1.start()
    print("Total cost ", time.time() - start_time)
    # is_download_realtime_stock_action(trade_date='20200703', ts_code='300843.SZ')

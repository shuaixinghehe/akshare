#! /usr/bin/env python
# *-* coding:utf-8 *-*
import datetime
import sys

import pymysql.cursors
import scipy.stats

reload(sys)
sys.setdefaultencoding('utf8')

conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="tushare", \
                       charset='utf8')
cur = conn.cursor()

seed_stock_map = {
    '002953.SZ': '20200310',
    '300048.SZ': '20200325',
    '603879.SH': "20200305",
    '603879.SH': "20200305",
    '603879.SH': "20200316",
    '600538.SH': "20200311"
}


def get_stock_list(trade_date):
    print "获取最近股票"
    sql = """
               select
                   ts_code,count(1) cnt
               from stock_daily
               where trade_date=%s
               group by ts_code
           """
    cur.execute(sql, (trade_date))
    result = cur.fetchall()
    stock_list = []
    for row in result:
        stock_list.append(row[0])
    return stock_list


def get_stock_trade_detail(ts_code, start_trade_date, end_trade_date):
    sql = """
        select ts_code,trade_date,pct_chg,vol
        from stock_daily
        where trade_date>=%s and trade_date<=%s and ts_code=%s
        order by trade_date
    """
    cur.execute(sql, (start_trade_date, end_trade_date, ts_code))
    result = cur.fetchall()
    vol_list = []
    pct_chg_list = []
    vol_total = 0.0
    for row in result:
        vol_list.append(float(row[3]))
        vol_total += float(row[3])
        pct_chg_list.append(float(row[2]))
    vol_rate = []
    for vol in vol_list:
        vol_rate.append(vol / vol_total)
    return vol_rate, pct_chg_list


def cal_kl_distance(x=[], y=[]):
    if len(x) != len(y):
        return 1.0
    x_number = []
    y_number = []
    for i in x:
        x_number.append(float(i))
    for i in y:
        y_number.append(float(i))
    kl = scipy.stats.entropy(x_number, y_number)
    return str(kl)


def write_file(hashmod, value, ts_code, content):
    ifile = open("./" + str(hashmod) + "_" + str(value) + ".txt", "a+")
    ifile.write(content + "\n")
    ifile.close()


def history():
    pass


if __name__ == '__main__':
    pass
    print("股市有风险，入市需谨慎")
    print("目标翻一倍")
    print("计算KL距离 demo")
    ts_code = '002594.SZ'
    start_trade_date = '20201102'
    end_trade_date = '20201202'

    vol_list, pct_chg_list = get_stock_trade_detail(ts_code=ts_code, start_trade_date=start_trade_date,
                                                    end_trade_date=end_trade_date)

    print(vol_list)
    print(pct_chg_list)
    stock_list = get_stock_list('20201202')
    for stock in stock_list:
        t_vol_list, t_pct_chg_list = get_stock_trade_detail(stock, start_trade_date, end_trade_date)
        print(stock, cal_kl_distance(t_vol_list, vol_list))
        print(stock, cal_kl_distance(vol_list, t_vol_list))

    # print seed_vol_list
    # for i in range(50, 80):
    #     day = datetime.date.today() + datetime.timedelta(days=i * -1)
    #     day = str(day).replace('-', '')
    #     for ts_code in stock_list:
    #         if hash(ts_code) % hashmod == value:
    #             target_vol_list = get_stock_trade_detail(ts_code, day, 10, column_index)
    #             if len(seed_vol_list) == len(target_vol_list):
    #                 if hash(ts_code) % 50 == 0:
    #                     print "002953.SZ", ts_code, day, seed_vol_list, target_vol_list, cal_kl_distance(seed_vol_list,
    #                                                                                                      target_vol_list)
    #                 write_file(hashmod, value, ts_code,
    #                            "002953.SZ," + ts_code + "," + day + "," + cal_kl_distance(target_vol_list,
    #                                                                                       seed_vol_list))

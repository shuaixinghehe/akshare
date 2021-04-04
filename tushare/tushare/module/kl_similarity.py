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


def get_stock_list():
    print "获取最近股票",
    sql = """
               select
                   ts_code,count(1) cnt
               from stock_daily
               where trade_date >=%s and trade_date<=%s
               group by ts_code
           """
    cur.execute(sql, ('20200501', '20200531'))
    result = cur.fetchall()
    stock_list = []
    for row in result:
        stock_list.append(row[0])
    return stock_list


def get_stock_trade_detail(ts_code, end_trade_date, back_length, volumn_name_index):
    pass

    sql = """
        select *
        from stock_daily_basic
        where trade_date<=%s and trade_date>='20200201' and ts_code=%s
        order by trade_date desc
    """
    cur.execute(sql, (end_trade_date, ts_code))
    result = cur.fetchall()
    value_list = []
    for row in result:
        if hash(row[0]) % 100 == 1:
            print row
        back_length -= 1
        value_list.append(row[volumn_name_index])
        if back_length <= 0:
            break
    return value_list


def cal_kl_distance(x=[], y=[]):
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
    print('参数个数为:', len(sys.argv), '个参数。')
    print('参数列表:', str(sys.argv))
    hashmod = int(sys.argv[1])
    value = int(sys.argv[2])

    # hashmod = 1
    # value = 0
    column_index = 4
    stock_list = get_stock_list()
    seed_vol_list = get_stock_trade_detail('002953.SZ', '20200310', 10, column_index)
    print seed_vol_list
    for i in range(50, 80):
        day = datetime.date.today() + datetime.timedelta(days=i * -1)
        day = str(day).replace('-', '')
        for ts_code in stock_list:
            if hash(ts_code) % hashmod == value:
                target_vol_list = get_stock_trade_detail(ts_code, day, 10, column_index)
                if len(seed_vol_list) == len(target_vol_list):
                    if hash(ts_code) % 50 == 0:
                        print "002953.SZ", ts_code, day, seed_vol_list, target_vol_list, cal_kl_distance(seed_vol_list,
                                                                                                         target_vol_list)
                    write_file(hashmod, value, ts_code,
                               "002953.SZ," + ts_code + "," + day + "," + cal_kl_distance(target_vol_list,
                                                                                          seed_vol_list))

#! /usr/bin/env python
# *-* coding:utf-8 *-*
import os
import pymysql.cursors

conn = pymysql.connect(host="49.235.90.127", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="tushare", \
                       charset='utf8')

cur = conn.cursor()
sql = "select ts_code from stock_basic;"
cur.execute(sql)
result = cur.fetchall()
print result


def get_detail():
    pass
    trade_date = '20191205'
    ts_code = '000409.SZ'
    fileds = "`trade_date`,`close`,`turnover_rate`,`turnover_rate_f`,`volume_ratio`,`pe`," \
             "`pe_ttm`,`pb`,`ps`,`ps_ttm`,`total_share`,`float_share`,`free_share`,`total_mv`,`circ_mv`"
    fileds_list = fileds.replace("`", "").replace(" ", "").split(",")
    sql = "select " + fileds + "" \
                               "from stock_daily_basic " \
                               "where trade_date<=%s and ts_code=%s " \
                               "order by trade_date desc " \
                               "limit 30"
    cur.execute(sql, (trade_date, ts_code))
    result = cur.fetchall()
    feature_map = {}
    feature_map['ts_code'] = ts_code
    day_num = 0
    print "result:len", len(result)
    for row in result:
        for index in range(0, len(row)):
            if row[index] is not None and row[index] != 'NaN' and row[index] != 'None' and row[index] != 'nan':
                feature_map["f" + str(day_num) + "_day_before_daily_" + fileds_list[index]] = row[index]
            else:
                feature_map["f" + str(day_num) + "_day_before_daily_" + fileds_list[index]] = 0.0
        day_num += 1
        print feature_map
    return


if __name__ == '__main__':
    pass
    get_detail()

# coding:utf8

import pymysql.cursors
import time
import sys
import json

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


def get_ts_code_list():
    pass
    sql = """
        select ts_code
        from akshare_daily
        where trade_date>='20200401'
        group by ts_code
    """
    ak_cur.execute(sql, ())
    result = ak_cur.fetchall()
    ts_code_list = []
    for k in result:
        ts_code_list.append(k[0])
    return ts_code_list


insert_ts_code_map = {}


def insert_daily_report_up_down_detail(trade_date=''):
    select_sql = "select * from tushare.stock_daily_report_basic where trade_date={}".format(trade_date)

    ts_cur.execute(select_sql, ())
    result = ts_cur.fetchall()
    if len(result) != 0:
        pass
    else:
        print("select is null, insert into tushare.stock_daily_report_basic   ")
        ofile_sql_templaet = open('./stock_daily_report_up_down_detail_template.sql', 'r')
        sql = ''
        column_name_list = []
        for line in ofile_sql_templaet:
            line = line.strip()
            sql = sql + " " + line
            # print(line, line.split(' ')[-1].replace(',', ''))
            if str(line).find(',') != -1:
                column_name_list.append(line.split(' ')[-1].replace(',', ''))
        sql = sql.format(trade_date, trade_date)
        # print("sql", sql)
        ts_cur.execute(sql, ())
        result = ts_cur.fetchall()
        column_value_list = []
        column_map = {}
        for row in result:
            print('len(row)', len(row), 'len(column_name_list)', len(column_name_list))
            for i in range(0, len(row)):
                pass
                column_value_list.append(str(row[i]))
                column_map[column_name_list[i]] = row[i]
            # print(column_name_list[i], row[i])

        # inset_sql = "insert into tushare.stock_daily_report_basic ({})".format(",".join(column_name_list))
        # inset_sql += " values ({});".format(",".join(column_value_list))
        print("column_map", column_map.values())
        insert_sql = "insert into tushare.stock_daily_report_basic (trade_date,detail) values ('{}','{}')" \
            .format(trade_date, json.dumps(column_map, ensure_ascii=False))
        print("insert sql", insert_sql)
        ts_cur.execute(insert_sql, ())
        ts_conn.commit()


def insert_daily_report_continue_high(trade_date=''):
    print("update stock_daily_report_basic ")
    ofile_sql_templaet = open('./stock_daily_report_up_down_detail_template.sql', 'r')
    sql = ''
    column_name_list = []
    for line in ofile_sql_templaet:
        line = line.strip()
        sql = sql + " " + line
        # print(line, line.split(' ')[-1].replace(',', ''))
        if str(line).find(',') != -1:
            column_name_list.append(line.split(' ')[-1].replace(',', ''))
    sql = sql.format(trade_date, trade_date)
    # print("sql", sql)
    ts_cur.execute(sql, ())
    result = ts_cur.fetchall()
    column_value_list = []
    column_map = {}
    for row in result:
        print('len(row)', len(row), 'len(column_name_list)', len(column_name_list))
        for i in range(0, len(row)):
            pass
            column_value_list.append(str(row[i]))
            column_map[column_name_list[i]] = row[i]
        # print(column_name_list[i], row[i])

    # inset_sql = "insert into tushare.stock_daily_report_basic ({})".format(",".join(column_name_list))
    # inset_sql += " values ({});".format(",".join(column_value_list))
    print("column_map", column_map.values())
    insert_sql = "insert into tushare.stock_daily_report_basic (trade_date,detail) values ('{}','{}')" \
        .format(trade_date, json.dumps(column_map, ensure_ascii=False))
    print("insert sql", insert_sql)
    ts_cur.execute(insert_sql, ())
    ts_conn.commit()


if __name__ == '__main__':
    pass
    insert_daily_report_up_down_detail('20200807')
    # create_shareding_table()
    # sharding_action_table(batch_size=10000, offset_pos=0)
    print('参数个数为:', len(sys.argv), '个参数。')
    print('参数列表:', str(sys.argv))
    # hashmod = sys.argv[1]
    # value = sys.argv[2]
    # hashmod = 50
    # value = 0
    # start_sharding(int(hashmod), int(value))
    # truncate_shareding_table()
    # sql = """
    #        (ts_code,trade_date,trade_time,price,price_change,volumn,value,kind)
    #         values
    #         ({0},%s,%s,%s,  %s,%s,%s,%s );
    #     """
    # sql = sql.format(1, 2, 3, 4, 5, 6, 7, 8)
    # print(sql)
    # sharding_action_table()

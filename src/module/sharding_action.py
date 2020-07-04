# coding:utf8

import pymysql.cursors

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


def sharding_action_table():
    pass
    sql = """
            select * from stock_realtime_action limit 10
        """
    ak_cur.execute(sql, ())
    result = ak_cur.fetchall()
    for row in result:
        print(row[0])
        # insert_sql = """
        #     insert into table stock_realtime_action_
        # """


def create_shareding_table(ts_code='default'):
    pass
    ts_code_list = get_ts_code_list()
    for code in ts_code_list:
        print(code, str(code).replace('.', ""))
        ts_code = str(code).replace('.', "")
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


if __name__ == '__main__':
    pass
    create_shareding_table()
    # sharding_action_table()

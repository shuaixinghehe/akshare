# coding:utf8

import pymysql.cursors
import time

# ts_conn = pymysql.connect(host="127.0.0.1", user="tushare", \
#                           password="&QwX0^4#Sm^&t%V6wBnZC%78", \
#                           db="tushare", \
#                           charset='utf8')
#
# ts_cur = ts_conn.cursor()

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


def sharding_action_table(batch_size=0, offset_pos=0):
    pass
    sql = """ select * from stock_realtime_action limit """ + str(offset_pos) + "," + str(batch_size)
    print("sql", sql)
    ak_cur.execute(sql, ())
    result = ak_cur.fetchall()
    insert_sql = ""

    for row in result:
        table_name_part = str(row[0]).replace(".", "")
        insert_sql = """  ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}'),""".format(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
        )
        if table_name_part in insert_ts_code_map.keys():
            pass
            insert_ts_code_map[table_name_part] += insert_sql
        else:
            pass
            insert_ts_code_map[table_name_part] = insert_sql
    exce_insert_ts_code_map(insert_ts_code_map, 10)


def exce_insert_ts_code_map(map={}, limit=1000):
    pass
    insert_sql = ""
    for key in map.keys():
        if len(insert_ts_code_map[key]) > limit:
            insert_sql = """ insert into stock_realtime_action_""" + key + " (ts_code,trade_date,trade_time,price,price_change,volumn,value,kind) values "
            insert_sql += insert_ts_code_map[key][0:-1]
            insert_sql += ";"
            # print("merge sql", insert_sql)
            insert_ts_code_map[key] = ""
            ak_cur.execute(insert_sql, ())
            ak_conn.commit()
    # print("insert_sql->", insert_sql)
    # ak_cur.execute(insert_sql, ())
    # ak_conn.commit()


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


def truncate_shareding_table(ts_code='default'):
    pass
    ts_code_list = get_ts_code_list()
    sql = ""
    for code in ts_code_list:
        print(code, str(code).replace('.', ""))
        ts_code = str(code).replace('.', "")
        sql = "select * from  stock_realtime_action_" + ts_code
        ak_cur.execute(sql, ())
        result = ak_cur.fetchall()
        if len(result) > 0:
            sql = """ truncate table stock_realtime_action_""" + ts_code + """;"""
            print(sql)
            ak_cur.execute(sql, ())
            ak_conn.commit()
            time.sleep(1)
        else:
            print(ts_code, " is empty", len(result))


def start_sharding():
    pass
    batch_size = 500
    end_round = 30000
    for i in range(100, end_round):
        start_time = time.time()
        sharding_action_table(batch_size, offset_pos=i * batch_size)
        print(i, " round  cost ", time.time() - start_time)
    print(insert_ts_code_map)
    exce_insert_ts_code_map(insert_ts_code_map, 0)


if __name__ == '__main__':
    pass
    # create_shareding_table()
    # sharding_action_table(batch_size=10000, offset_pos=0)
    # start_sharding()
    truncate_shareding_table()
    # sql = """
    #        (ts_code,trade_date,trade_time,price,price_change,volumn,value,kind)
    #         values
    #         ({0},%s,%s,%s,  %s,%s,%s,%s );
    #     """
    # sql = sql.format(1, 2, 3, 4, 5, 6, 7, 8)
    # print(sql)

#! /usr/bin/env python
# *-* coding:utf-8 *-*
import time

import pymysql.cursors
import tushare as ts

from tushare_global_config import VALID_TRADE_DATE_LIST, \
    ak_share_stock_daily_fileds_list, ak_share_stock_daily_fileds

ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="akshare", \
                       charset='utf8')
cur = conn.cursor()
AK_SHARE_STOCK_DAILY_MEMORY_HFQ = {}  # akshare 股票情况数据
AK_SHARE_STOCK_DAILY_MEMORY_QFQ = {}  # akshare 股票情况数据


# ak share 数据daily
def download_ak_stock_daily_hfq_in_memory(start_trade_date='', end_trade_date='', ts_code_list=[]):
    print
    "download_ak_stock_daily_hfq_in_memory", start_trade_date
    start_time = time.time()
    sql = "select " + ak_share_stock_daily_fileds + " from akshare_daily where adjust='hfq' and trade_date>=%s and ts_code in ("
    for ts_code in ts_code_list:
        sql += "'" + ts_code + "',"
    sql = sql[:-1]
    sql += ")  group by " + ak_share_stock_daily_fileds + "  order by ts_code,trade_date desc"
    ak_share_stock_daily_map = {}
    cur.execute(sql, (start_trade_date))
    result = cur.fetchall()
    run_num = 0
    for row in result:
        ak_share_stock_daily_map[str(row[0]) + "_" + row[1]] = {}
        feature_map = {}
        run_num += 1
        for index in range(0, len(ak_share_stock_daily_fileds_list)):
            if index >= 0 and index <= 1:
                feature_map[ak_share_stock_daily_fileds_list[index]] = row[index]
            elif index > 1:
                feature_map[ak_share_stock_daily_fileds_list[index]] = float(row[index])
            else:
                feature_map[ak_share_stock_daily_fileds_list[index]] = 0.0
        ak_share_stock_daily_map[str(row[0]) + "_" + row[1]] = feature_map
    global AK_SHARE_STOCK_DAILY_MEMORY_HFQ
    AK_SHARE_STOCK_DAILY_MEMORY_HFQ = ak_share_stock_daily_map
    print
    "download_ak_stock_daily_hfq_in_memory fetch time", time.time() - start_time, len(
        AK_SHARE_STOCK_DAILY_MEMORY_HFQ)
    return ak_share_stock_daily_map


# ak share 数据daily
def download_ak_stock_daily_qfq_in_memory(start_trade_date='', end_trade_date='', ts_code_list=[]):
    print
    "download_ak_stock_daily_qfq_in_memory", start_trade_date
    start_time = time.time()
    sql = "select " + ak_share_stock_daily_fileds + " from akshare_daily where adjust='qfq' and trade_date>=%s and ts_code in ("
    for ts_code in ts_code_list:
        sql += "'" + ts_code + "',"
    sql = sql[:-1]
    sql += ") group by " + ak_share_stock_daily_fileds + " order by ts_code,trade_date desc"
    ak_share_stock_daily_map = {}
    cur.execute(sql, (start_trade_date))
    result = cur.fetchall()
    run_num = 0
    for row in result:
        ak_share_stock_daily_map[str(row[0]) + "_" + row[1]] = {}
        feature_map = {}
        run_num += 1
        for index in range(0, len(ak_share_stock_daily_fileds_list)):
            if index >= 0 and index <= 1:
                feature_map[ak_share_stock_daily_fileds_list[index]] = row[index]
            elif index > 1:
                feature_map[ak_share_stock_daily_fileds_list[index]] = float(row[index])
            else:
                feature_map[ak_share_stock_daily_fileds_list[index]] = 0.0
        ak_share_stock_daily_map[str(row[0]) + "_" + row[1]] = feature_map
    global AK_SHARE_STOCK_DAILY_MEMORY_QFQ
    AK_SHARE_STOCK_DAILY_MEMORY_QFQ = ak_share_stock_daily_map
    print
    "download_ak_stock_daily_qfq_in_memory fetch time", time.time() - start_time, len(
        AK_SHARE_STOCK_DAILY_MEMORY_QFQ)
    return ak_share_stock_daily_map


def get_ak_stock_daily_hfq_in_memory(start_trade_date, end_trade_date, ts_code):
    result = []
    # TODO: sb 操作
    for trade_date in VALID_TRADE_DATE_LIST:  # 逆序，最新的日期排在最前面
        if trade_date >= start_trade_date and trade_date <= end_trade_date:
            key = str(ts_code) + "_" + str(trade_date)
            temp_result = []
            if AK_SHARE_STOCK_DAILY_MEMORY_HFQ.has_key(key):
                for filed in ak_share_stock_daily_fileds_list:
                    temp_result.append(AK_SHARE_STOCK_DAILY_MEMORY_HFQ[key][filed])
                result.append(temp_result)
            else:
                print
                "get_ak_stock_daily_hfq_in_memory no key", key
                for filed in ak_share_stock_daily_fileds_list:
                    temp_result.append(0.0)
                result.append(temp_result)
    return result


def get_ak_stock_daily_qfq_in_memory(start_trade_date, end_trade_date, ts_code):
    result = []
    # TODO: sb 操作
    for trade_date in VALID_TRADE_DATE_LIST:  # 逆序，最新的日期排在最前面
        if trade_date >= start_trade_date and trade_date <= end_trade_date:
            key = str(ts_code) + "_" + str(trade_date)
            temp_result = []
            if AK_SHARE_STOCK_DAILY_MEMORY_QFQ.has_key(key):
                for filed in ak_share_stock_daily_fileds_list:
                    temp_result.append(AK_SHARE_STOCK_DAILY_MEMORY_QFQ[key][filed])
                result.append(temp_result)
            else:
                print("get_ak_stock_daily_qfq_in_memory no key", key)
                for filed in ak_share_stock_daily_fileds_list:
                    temp_result.append(0.0)
                result.append(temp_result)
    return result


# 生成特征
def get_ak_stock_daily_hfq_feature(key_trade_date='', start_trade_date='', end_trade_date='', ts_code=''):
    result = get_ak_stock_daily_hfq_in_memory(start_trade_date, end_trade_date, ts_code)
    feature_map = {}
    feature_map['ts_code'] = ts_code
    day_num = 0
    for row in result:
        for index in range(2, len(row)):
            if row[index] is not None and row[index] != 'NaN' and row[index] != 'None' and row[index] != 'nan':
                feature_map[
                    "f" + str(day_num) + "_day_before_ak_hfq_daily_" + ak_share_stock_daily_fileds_list[index]] = \
                    row[index]
            else:
                feature_map[
                    "f" + str(day_num) + "_day_before_ak_hfq_daily_" + ak_share_stock_daily_fileds_list[index]] = 0.0
        day_num += 1

    key = key_trade_date + "_" + ts_code

    # print "get_stock_money_flow_feature", feature_map
    # feature_config_map = get_feature_config_map()
    # new_feature_map = create_feature(feature_config_map, feature_map, key)
    # print "get_daily_feature new feature map", feature_map
    return key, feature_map


# 生成特征
def get_ak_stock_daily_qfq_feature(key_trade_date='', start_trade_date='', end_trade_date='', ts_code=''):
    result = get_ak_stock_daily_qfq_in_memory(start_trade_date, end_trade_date, ts_code)
    feature_map = {}
    feature_map['ts_code'] = ts_code
    day_num = 0
    for row in result:
        for index in range(2, len(row)):
            if row[index] is not None and row[index] != 'NaN' and row[index] != 'None' and row[index] != 'nan':
                feature_map[
                    "f" + str(day_num) + "_day_before_ak_qfq_daily_" + ak_share_stock_daily_fileds_list[index]] = \
                    row[index]
            else:
                feature_map[
                    "f" + str(day_num) + "_day_before_ak_qfq_daily_" + ak_share_stock_daily_fileds_list[index]] = 0.0
        day_num += 1

    key = key_trade_date + "_" + ts_code

    # print "get_stock_money_flow_feature", feature_map
    # feature_config_map = get_feature_config_map()
    # new_feature_map = create_feature(feature_config_map, feature_map, key)
    # print "get_daily_feature new feature map", feature_map
    return key, feature_map


if __name__ == '__main__':
    pass
    today_date = time.strftime("%Y%m%d", time.localtime())
    print(today_date)
    # download_stock_money_flow('20200612')

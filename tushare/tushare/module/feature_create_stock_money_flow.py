#! /usr/bin/env python
# *-* coding:utf-8 *-*
# 查询当前股票资金流向 由数据库导入到内存，提升效率
import time

from tushare_global_config import stock_money_flow_fileds, cur, stock_money_flow_fileds_list, LOG_INFO, perf, \
    VALID_TRADE_DATE_LIST
import tushare as ts
import pymysql.cursors

ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="tushare", \
                       charset='utf8')
cur = conn.cursor()
STOCK_MONEY_FLOW_MEMORY = {}


def download_stock_money_flow_in_memory(start_trade_date='', end_trade_date='', ts_code_list=[]):
    print("download_stock_money_flow_in_memory", start_trade_date)
    start_time = time.time()
    global STOCK_MONEY_FLOW_MEMORY
    sql = "select " + stock_money_flow_fileds + " from money_flow where trade_date>=%s and ts_code in ("
    for ts_code in ts_code_list:
        sql += "'" + ts_code + "',"
    sql = sql[:-1]
    sql += ") order by ts_code,trade_date desc"
    stock_money_flow_map = {}
    cur.execute(sql, (start_trade_date))
    result = cur.fetchall()
    run_num = 0
    for row in result:
        STOCK_MONEY_FLOW_MEMORY[str(row[0]) + "_" + row[1]] = {}
        feature_map = {}
        run_num += 1
        for index in range(0, len(stock_money_flow_fileds_list)):
            if index >= 0 and index <= 1:
                feature_map[stock_money_flow_fileds_list[index]] = row[index]
            elif index > 1:
                feature_map[stock_money_flow_fileds_list[index]] = float(row[index])
            else:
                feature_map[stock_money_flow_fileds_list[index]] = 0.0
        STOCK_MONEY_FLOW_MEMORY[str(row[0]) + "_" + row[1]] = feature_map
    LOG_INFO("download_stock_money_flow_in_memory fetch time", time.time() - start_time, len(STOCK_MONEY_FLOW_MEMORY))
    return STOCK_MONEY_FLOW_MEMORY


# 查询当前股票资金流向
def download_stock_money_flow(stock_date=''):
    is_need_downloaded = True

    while is_need_downloaded:
        try:
            data = pro.moneyflow(trade_date=stock_date)
            time.sleep(1)
            is_need_downloaded = False
        except Exception as  e:
            print("retry download_stock_money_follow")

    sql = """
    insert into money_flow (
        ts_code,trade_date,
        buy_sm_vol,buy_sm_amount,
        sell_sm_vol,sell_sm_amount,
        buy_md_vol,buy_md_amount,
        sell_md_vol,sell_md_amount,
        buy_lg_vol,buy_lg_amount,
        sell_lg_vol,sell_lg_amount,
        buy_elg_vol,buy_elg_amount,
        sell_elg_vol,sell_elg_amount,
        net_mf_vol,net_mf_amount
    )
    values
    (%s,%s,%s,%s,%s,
     %s,%s,%s,%s,%s,
     %s,%s,%s,%s,%s,
     %s,%s,%s,%s,%s);
    """
    for index, row in data.iterrows():
        result = cur.execute(sql, (
            str(row['ts_code']).encode('utf-8'),
            str(row['trade_date']).encode('utf-8'),
            str(row['buy_sm_vol']).encode('utf-8'),
            str(row['buy_sm_amount']).encode('utf-8'),
            str(row['sell_sm_vol']).encode('utf-8'),
            str(row['sell_sm_amount']).encode('utf-8'),
            str(row['buy_md_vol']).encode('utf-8'),
            str(row['buy_md_amount']).encode('utf-8'),
            str(row['sell_md_vol']).encode('utf-8'),
            str(row['sell_md_amount']).encode('utf-8'),
            str(row['buy_lg_vol']).encode('utf-8'),
            str(row['buy_lg_amount']).encode('utf-8'),
            str(row['sell_lg_vol']).encode('utf-8'),
            str(row['sell_lg_amount']).encode('utf-8'),
            str(row['buy_elg_vol']).encode('utf-8'),
            str(row['buy_elg_amount']).encode('utf-8'),
            str(row['sell_elg_vol']).encode('utf-8'),
            str(row['sell_elg_amount']).encode('utf-8'),
            str(row['net_mf_vol']).encode('utf-8'),
            str(row['net_mf_amount']).encode('utf-8')
        ))
        conn.commit()
        LOG_INFO(row['ts_code'], row['trade_date'], result)
        perf(namespace='stock_money_flow', subtag=row['ts_code'])


def get_stock_money_flow_in_memory(start_trade_date, end_trade_date, ts_code):
    result = []
    # TODO: sb 操作
    for trade_date in VALID_TRADE_DATE_LIST:  # 逆序，最新的日期排在最前面
        if trade_date >= start_trade_date and trade_date <= end_trade_date:
            key = str(ts_code) + "_" + str(trade_date)
            temp_result = []
            if key in STOCK_MONEY_FLOW_MEMORY.keys():
                for filed in stock_money_flow_fileds_list:
                    temp_result.append(STOCK_MONEY_FLOW_MEMORY[key][filed])
                result.append(temp_result)
            else:
                # LOG_INFO("get_stock_money_flow_in_memory no key", key)
                for filed in stock_money_flow_fileds_list:
                    temp_result.append(0.0)
                result.append(temp_result)
    return result


# 生成特征
def get_stock_money_flow_feature(key_trade_date='', start_trade_date='', end_trade_date='', ts_code=''):
    result = get_stock_money_flow_in_memory(start_trade_date, end_trade_date, ts_code)
    feature_map = {}
    feature_map['ts_code'] = ts_code
    day_num = 0
    for row in result:
        for index in range(2, len(row)):
            if row[index] is not None and row[index] != 'NaN' and row[index] != 'None' and row[index] != 'nan':
                feature_map["f" + str(day_num) + "_day_before_money_flow_" + stock_money_flow_fileds_list[index]] = row[
                    index]
            else:
                feature_map["f" + str(day_num) + "_day_before_money_flow_" + stock_money_flow_fileds_list[index]] = 0.0
        day_num += 1

    key = key_trade_date + "_" + ts_code

    # print "get_stock_money_flow_feature", feature_map
    # feature_config_map = get_feature_config_map()
    # new_feature_map = create_feature(feature_config_map, feature_map, key)
    # print "get_daily_feature new feature map", feature_map
    return key, feature_map


if __name__ == '__main__':
    pass

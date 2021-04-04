#! /usr/bin/env python
# *-* coding:utf-8 *-*
import sys
import time

import pymysql.cursors
import tushare as ts
import logging

from feature_create_stock_realtime_action_detail_basic import STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY
from tushare_global_config import stock_money_flow_fileds, stock_money_flow_fileds_list, VALID_TRADE_DATE_LIST, \
    ak_share_realtime_action_fileds, ak_share_realtime_action_fileds_list, LOG_INFO, LOG_ERROR

# reload(sys)
# sys.setdefaultencoding('utf8')

ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="tushare", \
                       charset='utf8')
cur = conn.cursor()

logging.basicConfig(level=logging.INFO,
                    filename='/tmp/realtime_action_download.log',
                    filenode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("realtime_action")

LOG = logger


def get_stock_realtime_action_detail_basic(start_trade_date, end_trade_date, ts_code):
    result = []
    # TODO: sb 操作
    for trade_date in VALID_TRADE_DATE_LIST:  # 逆序，最新的日期排在最前面
        if trade_date >= start_trade_date and trade_date <= end_trade_date:
            key = str(ts_code) + "_" + str(trade_date)
            temp_result = []
            if key in STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY.keys():
                for filed in ak_share_realtime_action_fileds_list:
                    temp_result.append(STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY[key][filed])
                result.append(temp_result)
            else:
                LOG_INFO("get_stock_realtime_action_detail_basic no key", key)
                for filed in ak_share_realtime_action_fileds_list:
                    temp_result.append(0.0)
                result.append(temp_result)
    return result


# 生成特征
def get_stock_realtime_action_detail_basic_feature(key_trade_date='', start_trade_date='', end_trade_date='',
                                                   ts_code=''):
    result = get_stock_realtime_action_detail_basic(start_trade_date, end_trade_date, ts_code)
    feature_map = {}
    feature_map['ts_code'] = ts_code
    day_num = 0
    for row in result:
        for index in range(2, len(row)):
            if row[index] is not None and row[index] != 'NaN' and row[index] != 'None' and row[index] != 'nan':
                feature_map[
                    "f" + str(day_num) + "_day_before_realtime_action_basic_"
                    + ak_share_realtime_action_fileds_list[index]] = row[index]
            else:
                feature_map[
                    "f" + str(day_num) + "_day_before_realtime_action_basic_"
                    + ak_share_realtime_action_fileds_list[index]] = 0.0
        day_num += 1
        if day_num >= 7:  # 只使用最近7天的交易数据
            break

    key = key_trade_date + "_" + ts_code
    return key, feature_map


if __name__ == '__main__':
    pass
    today_date = time.strftime("%Y%m%d", time.localtime())
    print
    today_date
    # download_stock_money_flow('20200612')

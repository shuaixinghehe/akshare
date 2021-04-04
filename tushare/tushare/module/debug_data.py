#! /usr/bin/env python
# *-* coding:utf-8 *-*


# 检查create feature pre 数据少问题
from create_feature_pre import insert_stock_realtime_action_detail_basic
from tushare_global_config import cur, LOG_INFO, get_stock_daily_trade_date


def check_create_feature_pre_data(trade_date='20201228'):
    pass
    table_name = 'tushare.realtime_action_detail_basic'
    sql = '''
        select ts_code from {} where trade_date={}
    '''.format(table_name, trade_date)
    LOG_INFO(sql)
    cur.execute(sql, ())
    result = cur.fetchall()
    all_ready_download_code_list = []
    for item in result:
        # print(item[0])
        all_ready_download_code_list.append(item[0])
    sql = '''
        select ts_code from tushare.stock_daily where trade_date={}
    '''.format(trade_date)

    cur.execute(sql, ())
    result = cur.fetchall()
    daily_code_list = []
    for item in result:
        daily_code_list.append(item[0])

    # 查看哪些没有下载
    for ts_code in daily_code_list:
        if ts_code not in all_ready_download_code_list:
            reason, download_len = check_create_feature_pre_failed_reason(trade_date=trade_date, ts_code=ts_code)
            LOG_INFO(ts_code, trade_date, "need download", 'reason', reason, download_len)
            insert_stock_realtime_action_detail_basic(ts_code=ts_code, start_trade_date=trade_date)


# 回答为啥没有下载
def check_create_feature_pre_failed_reason(trade_date, ts_code):
    ts_code_simple = str(ts_code).replace('.', '')
    # 如果有每天交易实时特征
    # 1.要realtime action 有每天的交易数据
    reason = "unknown"
    sql = '''
        select * from akshare.stock_realtime_action_{} where trade_date={}
    '''.format(ts_code_simple, trade_date)

    cur.execute(sql, ())
    result = cur.fetchall()
    if len(result) == 0:
        reason = "no realtime action trade detail"
    return reason, len(result)


# debug 数据
if __name__ == '__main__':
    trade_date_list = get_stock_daily_trade_date(start_trade_date='20201201')
    LOG_INFO(trade_date_list)
    for trade_date in trade_date_list:
        check_create_feature_pre_data(trade_date=trade_date)

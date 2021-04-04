#! /usr/bin/env python
# *-* coding:utf-8 *-*

# 创建label，短期
import tushare_utils

from tushare_global_config import cur, get_valid_stock

from tushare_global_config import get_stock_daily_trade_date

BACK_TRACE_STOCK_LIST = []  # 查询可交易的股票
START_TRADE_DATE = '20200701'
END_TRADE_DATE = '20200708'


# 获取最佳的交易方式
def get_stock_daily_trade_max_profit():
    pass
    sql = """
        select
            ts_code,trade_date,high,low
        from stock_daily
        where trade_date>=%s
        and trade_date<=%s
        and ts_code not like %s
        and high!=low
    """
    cur.execute(sql, (START_TRADE_DATE, END_TRADE_DATE, '688%'))
    result = cur.fetchall()
    print "可以查询到交易天数", len(result)
    stock_daily_map = {}
    trade_date_list = get_stock_daily_trade_date()
    ts_code_index = 0
    trade_date_index = 1
    high_index = 2
    low_index = 3
    for row in result:
        if stock_daily_map.has_key(row[trade_date_index]):
            stock_daily_map[row[trade_date_index]][row[ts_code_index]] = {}
            stock_daily_map[row[trade_date_index]][row[ts_code_index]]['high'] = row[high_index]
            stock_daily_map[row[trade_date_index]][row[ts_code_index]]['low'] = row[low_index]
        else:
            stock_daily_map[row[trade_date_index]] = {}
            stock_daily_map[row[trade_date_index]][row[ts_code_index]] = {}
            stock_daily_map[row[trade_date_index]][row[ts_code_index]]['high'] = row[high_index]
            stock_daily_map[row[trade_date_index]][row[ts_code_index]]['low'] = row[low_index]
    for trade_date in stock_daily_map.keys():
        print trade_date
        print len(stock_daily_map[trade_date])
        print stock_daily_map[trade_date]
        break
    trade_date_list.reverse()
    trade_valid_stock = get_valid_stock(START_TRADE_DATE)
    target_stock_map = {}
    not_target_stock_map = {}
    for i in range(0, len(trade_date_list) - 1):
        print i, trade_date_list[i]
        today = trade_date_list[i]
        tomorrow = trade_date_list[i + 1]
        max_increase_rate = -1.0
        min_increase_rate = 1.0
        stock_detail_map = {}
        for stock in trade_valid_stock:
            try:
                today_low = float(stock_daily_map[today][stock]['low'])
                tomorrow_high = float(stock_daily_map[tomorrow][stock]['high'])
                tomorrow_low = float(stock_daily_map[tomorrow][stock]['low'])
                today_high = float(stock_daily_map[today][stock]['high'])
                new_max_increase_rate = max(max_increase_rate, (tomorrow_high - today_low) / today_low)
                new_min_increase_rate = min(min_increase_rate, (tomorrow_low - today_high) / today_high)
                stock_detail_map[stock] = float((tomorrow_high - today_low) / today_low)
                if new_max_increase_rate > max_increase_rate:
                    max_increase_rate = new_max_increase_rate
                    target_stock_map[today] = {}
                    target_stock_map[today]['stock'] = stock
                    target_stock_map[today]['max_increase_rate'] = max_increase_rate

                if new_min_increase_rate < min_increase_rate:
                    min_increase_rate = new_min_increase_rate
                    not_target_stock_map[today] = {}
                    not_target_stock_map[today]['stock'] = stock
                    not_target_stock_map[today]['min_increase_rate'] = min_increase_rate

            except Exception, e:
                pass
        printMapTopValue(stock_detail_map, 5)
    total_rate = 1.0
    for key in trade_date_list[:-1]:
        print key, target_stock_map[key]
        total_rate = total_rate * (1 + float(target_stock_map[key]['max_increase_rate']))
    print "max_increase_rate", total_rate

    total_rate = 1.0
    for key in trade_date_list[:-1]:
        print key, not_target_stock_map[key]
        total_rate = total_rate * (1 + float(not_target_stock_map[key]['min_increase_rate']))
    print "min_increase_rate", total_rate


def printMapTopValue(map={}, required_cnt=10):
    pass
    l = sorted(map.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    # 取出前几个， 也可以在sorted返回的list中取前几个
    cnt = 0
    for item in l:
        cnt += 1
        if cnt > required_cnt:
            break
        print "   ", item
    print


if __name__ == '__main__':
    print "获取可以交易的日期", "start date", START_TRADE_DATE, "end date", END_TRADE_DATE
    print get_stock_daily_trade_date()

    print "最佳交易记录"
    print get_stock_daily_trade_max_profit()

    # before = {
    #     "key1": 5,
    #     "key2": 6,
    #     "key3": 4,
    #     "key4": 3,
    # }
    # # printMapTopValue(before, 4)

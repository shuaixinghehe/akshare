#! /usr/bin/env python
# *-* coding:utf-8 *-*
import datetime
import sys
import time

import tushare as ts

# ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')


# reload(sys)
# sys.setdefaultencoding('utf8')


# 查询当前所有正常上市交易的股票列表
def stock_basic():
    data = pro.stock_basic(exchange='', list_status='L',
                           fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    print(type(data))
    for index, row in data.iterrows():
        print(row)


# 查询工作日
def trade_cal():
    end_date = time.strftime("%Y%m%d", time.localtime())
    today = datetime.datetime.now()
    start_date = (today + datetime.timedelta(-30)).strftime("%Y%m%d")
    df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
    trade_date_list = []
    for index, row in df.iterrows():
        if row['is_open'] == 1:
            trade_date_list.append(row['cal_date'])
    print(trade_date_list)
    return trade_date_list


# 日线行情
def daily():
    df = pro.daily(trade_date='20191204')
    print(df)
    df = pro.daily(trade_date='20200608')
    # print df


# 周线行情
def weekly():
    df = pro.weekly(ts_code='000001.SZ', start_date='20191101', end_date='20191125',
                    fields='ts_code,trade_date,open,high,low,close,vol,amount')
    print(df)
    # df = pro.weekly(trade_date='20191126', fields='ts_code,trade_date,open,high,low,close,vol,amount')
    # print df


# 月线行情
def monthly():
    df = pro.monthly(ts_code='000001.SZ', start_date='20180101', end_date='20181101',
                     fields='ts_code,trade_date,open,high,low,close,vol,amount')
    print(df)


# 每日指标
def daily_basic():
    # df = pro.daily_basic(ts_code='000001.SZ', trade_date='20180726',
    #                      fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
    # print  df

    df = pro.daily_basic(ts_code='000001.SZ', start_date='20191204', end_date='20191204',
                         fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
    print(df)
    # df = pro.daily_basic(ts_code='', trade_date='20191204',
    # df = pro.daily_basic(ts_code='',
    #                      trade_date='20200608',
    #                      fields='ts_code, trade_date, close, turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,ps_ttm,total_share,float_share,free_share,total_mv,circ_mv'
    #                      )
    print(df)


def moneyflow():
    # 获取单日全部股票数据
    df = pro.moneyflow(trade_date='20200612')
    # 获取单个股票数据
    df = pro.moneyflow(ts_code='000001.SZ', start_date='20191110', end_date='20191116')
    print(df)
    # df = pro.moneyflow(ts_code='000001.SZ', start_date='20191110', end_date='20191116')
    # print df


def income():
    df = pro.income(ts_code='600000.SH', start_date='20180101', end_date='20180730',
                    fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,basic_eps,diluted_eps,distable_profit')
    print(df)


def tiger(lastNDays, ts_code):
    trade_days = trade_cal();
    dict = {}
    for date in trade_days:
        dict[date] = {}
        df = pro.query('top_inst', trade_date=date, ts_code=ts_code)
        for index, item in df.iterrows():
            dict[date][item['exalter']] = {}
            dict[date][item['exalter']]['buy'] = item['buy']
            dict[date][item['exalter']]['sell'] = item['sell']

    tiger_dict = {}
    for date, value in dict.items():
        if value:
            for exalter, v in value.items():
                ###打印每天龙虎榜交易明细
                # print(date, exalter, v['buy'], v['sell'])
                print(date, exalter, v['buy'], v['sell'])
                if tiger_dict.__contains__(exalter):
                    tiger_dict[exalter] += v['buy'] - v['sell']
                else:
                    tiger_dict[exalter] = v['buy'] - v['sell']
    for key, value in sorted(tiger_dict.items(), key=lambda x: x[1], reverse=True):
        print(key.decode('string_escape'), value)


# dict[df.exalter][date]['buy'] = df.buy
# dict[df.exalter][date]['sell']= df.sell
# print (df.exalter, dict[df.exalter][date]['buy'], dict[df.exalter][date]['sell'])
# print (df)


def pro_bar():
    df = ts.pro_bar(ts_code='000001.SZ', freq='1min', start_date='20200615', end_date='20200616')
    # print df


def index_daily():
    pass
    df = pro.index_daily(ts_code='399300.SZ', start_date='20200101', end_date='20200808')
    for index, row in df.iterrows():
        print(row['ts_code'], row['name'], row['publisher'])


def index_basic():
    df = pro.index_basic(market='SZSE')
    for index, row in df.iterrows():
        print(row['ts_code'], str(row['name']).encode('utf-8'), str(row['publisher']).encode('utf-8'))

    df = pro.index_basic(market='SSE')
    for index, row in df.iterrows():
        print(row['ts_code'], str(row['name']).encode('utf-8'), str(row['publisher']).encode('utf-8'))


def index_daily_basic():
    pass
    # df = pro.index_dailybasic(trade_date='20181018', fields='ts_code,trade_date,turnover_rate,pe')
    df = pro.index_daily(ts_code='000001.SH', start_date='20200821', end_date='20200821')
    # df = pro.index_daily(ts_code='000001.SH', start_date='20200821', end_date='20200821')
    for index, row in df.iterrows():
        print(index, row)


if __name__ == '__main__':
    pass
    # stock_basic()
    trade_cal()
    # daily()
    # weekly()
    # monthly()
    # daily_basic()
    # moneyflow()
    # income()
    # tiger(30, '600527.SH')
    # pro_bar()
    # tiger(30, '600178.SH')
    # index_basic()
    # index_daily_basic()

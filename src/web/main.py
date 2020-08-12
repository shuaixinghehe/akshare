#! /usr/bin/env python
# *-* coding:utf-8 *-*
import random
import time
import json
import web
import datetime

import mydb

urls = (
    '/check(.*)', 'Check',
    '/daily_report_(.*)', 'DailyReport',
    '/daily_high_report_(.*)', 'DailyHighReport',
    '/daily_industry_report', 'DailyIndustryReport',
    '/daily_change_aggr_report', 'DailyChangeAggrReport',
    '/daily_top_inst_report', 'DailyTopInstReport'
)
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'),
                              initializer={'state': 0, 'community_name': 'unknown'})
t_globals = {
    'cookie': web.cookies,
    'datestr': web.datestr,
    'session': session,
}
render = web.template.render('templates/', globals=t_globals)


class DailyTopInstReport:
    def GET(self):
        input_data = web.input()
        trade_date = input_data.trade_date
        back_trade_date = datetime.datetime.strptime(trade_date, '%Y%m%d')
        list_date = (back_trade_date + datetime.timedelta(-90)).strftime("%Y%m%d")
        data = mydb.get_stock_daily_top_inst(trade_date, list_date)

        print('trade_date', trade_date, 'data', data)
        # for item in data:
        #     print(item)
        return render.daily_top_inst_report(trade_date, data)


class DailyChangeAggrReport:
    def GET(self):
        pass
        input_data = web.input()
        trade_date = input_data.trade_date
        back_trade_date = datetime.datetime.strptime(trade_date, '%Y%m%d')
        list_trade_date = (back_trade_date + datetime.timedelta(-90)).strftime("%Y%m%d")
        day_5_before_trade_date = (back_trade_date + datetime.timedelta(-7)).strftime("%Y%m%d")
        day_10_before_trade_date = (back_trade_date + datetime.timedelta(-14)).strftime("%Y%m%d")
        day_20_before_trade_date = (back_trade_date + datetime.timedelta(-28)).strftime("%Y%m%d")
        data = mydb.get_stock_change_aggr(trade_date, list_trade_date, day_5_before_trade_date,
                                          day_10_before_trade_date, day_20_before_trade_date)
        return render.daily_change_aggr_report(trade_date, data)
        # for item in data:
        #     print(item)


class DailyReport:
    def GET(self, trade_date):
        if trade_date == '':
            pass
        else:
            data = mydb.get_stock_daily_report_detail(trade_date)
            trade_date = ''
            detail_map = {}
            detail_high_map = []
            for item in data:
                print('item trade_date', item['trade_date'])
                print('item detail', item['detail'])
                trade_date = item['trade_date']
                detail_map = json.loads(item['detail'])
                break
            # trade_date = data.list()[0].values()[0]1
            # detail = data.list()[0].values()[1]
            # print("trade_date", trade_date, "detail", detail)
            stock_name_data = mydb.get_stock_name(trade_date)
            stock_name_map = {}
            stock_basic_map = {}
            for item in stock_name_data:
                stock_name_map[item['ts_code']] = item['name']
                stock_basic_map[item['ts_code']] = {}
                stock_basic_map[item['ts_code']]['industry'] = item['industry']
            stock_daily_map = {}
            stock_daily_data = mydb.get_stock_daily(trade_date)
            for item in stock_daily_data:
                stock_daily_map[item['ts_code']] = {}
                stock_daily_map[item['ts_code']]['pct_chg'] = str(item['pct_chg'])[0:4]
            print("stock_daily_map", stock_daily_map)

            stock_daily_basic_data = mydb.get_stock_daily_basic(trade_date)
            stock_daily_basic_map = {}
            for item in stock_daily_basic_data:
                stock_daily_basic_map[item['ts_code']] = {}
                stock_daily_basic_map[item['ts_code']]['circ_mv'] = str(int(float(item['circ_mv']) / 10000))

            up_9_stock_industry_map = {}  # 按照行业分类
            for ts_code in str(detail_map['up_9_stock_set']).split(","):
                print("stock", ts_code)
                if stock_basic_map[ts_code]['industry'] in up_9_stock_industry_map.keys():
                    pass
                    up_9_stock_industry_map[stock_basic_map[ts_code]['industry']][ts_code] = \
                        int(stock_daily_basic_map[ts_code]['circ_mv'])
                else:
                    up_9_stock_industry_map[stock_basic_map[ts_code]['industry']] = {}
                    up_9_stock_industry_map[stock_basic_map[ts_code]['industry']][ts_code] = \
                        int(stock_daily_basic_map[ts_code]['circ_mv'])
            up_9_stock_industry_list = sorted(up_9_stock_industry_map.items(), key=lambda item: len(item[1].keys()),
                                              reverse=True)
            up_9_stock_industry_tuple_list = []
            for t in up_9_stock_industry_list:
                up_9_stock_industry_tuple_list.append(
                    (t[0], sorted(t[1].items(), key=lambda item: item[1], reverse=True)))
            print('up_9_stock_industry_tuple_list', up_9_stock_industry_tuple_list)
            print('up_9_stock_industry_list', json.dumps(up_9_stock_industry_list))
            for industry in up_9_stock_industry_map.keys():
                tuple_list = sorted(up_9_stock_industry_map[industry].items(), key=lambda item: item[1],
                                    reverse=True)
                print(industry, tuple_list)
                for i in tuple_list:
                    print(i[0], i[1])
            print("up_9_stock_industry_order_map", json.dumps(up_9_stock_industry_map))
            return render.daily_report(trade_date, detail_map, stock_name_map, stock_daily_map, stock_basic_map,
                                       stock_daily_basic_map, up_9_stock_industry_tuple_list)


class DailyIndustryReport:
    def GET(self):
        input_data = web.input()
        print('input data', input_data)
        data = mydb.get_industry_report(input_data.trade_date, input_data.industry)
        # for item in data:
        #     print(item)
        return render.daily_industry_report(input_data.trade_date, data)


class DailyHighReport:
    def GET(self, trade_date):
        pass
        back_trade_date = datetime.datetime.strptime(trade_date, '%Y%m%d')
        start_date = (back_trade_date + datetime.timedelta(-9)).strftime("%Y%m%d")
        print(start_date, back_trade_date)
        stock_continue_high_data = mydb.get_stock_continue_high(start_date, trade_date)
        stock_continue_high_list = []
        for item in stock_continue_high_data:
            temp_map = {}
            temp_map['ts_code'] = item['ts_code']
            temp_map['name'] = item['name']
            temp_map['cnt'] = item['cnt']
            temp_map['trade_date_list'] = sorted(str(item['trade_date_list']).split(','))
            print(temp_map)
            stock_continue_high_list.append(temp_map)
        stock_name_data = mydb.get_stock_name(trade_date)
        stock_name_map = {}
        stock_basic_map = {}
        for item in stock_name_data:
            stock_name_map[item['ts_code']] = item['name']
            stock_basic_map[item['ts_code']] = {}
            stock_basic_map[item['ts_code']]['industry'] = item['industry']

        stock_daily_basic_data = mydb.get_stock_daily_basic(trade_date)
        stock_daily_basic_map = {}
        for item in stock_daily_basic_data:
            stock_daily_basic_map[item['ts_code']] = {}
            stock_daily_basic_map[item['ts_code']]['circ_mv'] = str(int(float(item['circ_mv']) / 10000))

        return render.daily_report_continue_high(trade_date, stock_continue_high_list, stock_basic_map,
                                                 stock_daily_basic_map)


if __name__ == "__main__":
    app.run()

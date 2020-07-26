#! /usr/bin/env python
# *-* coding:utf-8 *-*
import random
import time
import json
import web

import mydb

urls = (
    '/check(.*)', 'Check',
    '/daily_report_(.*)', 'DailyReport'
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


class Check:
    def GET(self, name):
        # data = web.input()
        data = None
        if name == 'random':
            data = get_random_data()
        else:
            data = mydb.get_model_reco_stock_detail(name)
        print(data)
        trade_history_key_list = []
        trade_history_detail_map = {}
        buy_date_map = {}
        for item in data:
            ts_code = item['ts_code']
            buy_date = item['buy_date']
            key = buy_date + "_" + ts_code
            trade_history_key_list.append(key)
            sell_date = item['sell_date']
            print
            item['ts_code'], item['buy_date'], item['sell_date']
            stock_detail_data = mydb.get_stock_detail(ts_code=ts_code, trade_date=buy_date)
            history_item_map = {}
            if stock_detail_data is not None:
                for detail in stock_detail_data:
                    history_item_map['ts_code'] = ts_code
                    history_item_map['buy_date'] = buy_date
                    history_item_map['sell_date'] = sell_date
                    history_item_map['buy_high'] = detail['high']
                    history_item_map['buy_open'] = detail['open']
                    history_item_map['buy_low'] = detail['low']
                    history_item_map['buy_close'] = detail['close']

            stock_detail_data = mydb.get_stock_detail(ts_code=ts_code, trade_date=sell_date)
            if stock_detail_data is not None:
                for detail in stock_detail_data:
                    history_item_map['sell_high'] = detail['high']
                    history_item_map['sell_open'] = detail['open']
                    history_item_map['sell_low'] = detail['low']
                    history_item_map['sell_close'] = detail['close']
                buy_date_map[buy_date] = True

            trade_history_detail_map[key] = history_item_map
            if trade_history_detail_map[key].has_key('buy_open') and trade_history_detail_map[key].has_key('sell_high'):
                trade_history_detail_map[key]['strategy1'] = strategy1(trade_history_detail_map[key]['buy_open'],
                                                                       trade_history_detail_map[key]['sell_high'])
            if trade_history_detail_map[key].has_key('buy_open') and trade_history_detail_map[key].has_key('sell_open'):
                trade_history_detail_map[key]['strategy2'] = strategy2(trade_history_detail_map[key]['buy_open'],
                                                                       trade_history_detail_map[key]['sell_open'])
                trade_history_detail_map[key]['strategy3'] = strategy3(
                    trade_history_detail_map[key]['buy_low'],
                    trade_history_detail_map[key]['buy_high'],
                    trade_history_detail_map[key]['sell_low'],
                    trade_history_detail_map[key]['sell_high']

                )
        buy_date_strategys_map = {}
        for buy_date in buy_date_map.keys():
            buy_cnt = 0
            for key in trade_history_detail_map.keys():
                if key.split('_')[0] == buy_date and trade_history_detail_map[key].has_key('strategy1'):
                    buy_cnt += 1
                    if buy_date_strategys_map.has_key(buy_date):
                        buy_date_strategys_map[buy_date]['total_strategy1'] += trade_history_detail_map[key][
                            'strategy1']
                        buy_date_strategys_map[buy_date]['total_strategy2'] += trade_history_detail_map[key][
                            'strategy2']
                        buy_date_strategys_map[buy_date]['total_strategy3'] += trade_history_detail_map[key][
                            'strategy3']
                    else:
                        buy_date_strategys_map[buy_date] = {}
                        buy_date_strategys_map[buy_date]['total_strategy1'] = trade_history_detail_map[key]['strategy1']
                        buy_date_strategys_map[buy_date]['total_strategy2'] = trade_history_detail_map[key]['strategy2']
                        buy_date_strategys_map[buy_date]['total_strategy3'] = trade_history_detail_map[key]['strategy3']
            if buy_date_strategys_map.has_key(buy_date):
                buy_date_strategys_map[buy_date]['total_strategy1_rate'] = round(buy_date_strategys_map[buy_date][
                                                                                     'total_strategy1'] / (
                                                                                         buy_cnt * 10000), 2)
                buy_date_strategys_map[buy_date]['total_strategy2_rate'] = round(buy_date_strategys_map[buy_date][
                                                                                     'total_strategy2'] / (
                                                                                         buy_cnt * 10000), 2)
                buy_date_strategys_map[buy_date]['total_strategy3_rate'] = round(buy_date_strategys_map[buy_date][
                                                                                     'total_strategy3'] / (
                                                                                         buy_cnt * 10000), 2)
        print('trade_history_detail_map', buy_date_strategys_map)

        trade_history_key_list = sorted(trade_history_key_list)
        return render.check(trade_history_detail_map, trade_history_key_list, buy_date_strategys_map)


class DailyReport:
    def GET(self, trade_date):
        if trade_date == '':
            pass
        else:
            data = mydb.get_stock_daily_report_detail(trade_date)
            trade_date = ''
            detail_map = {}
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
            for item in stock_name_data:
                stock_name_map[item['ts_code']] = item['name']
            stock_daily_map = {}
            stock_daily_data = mydb.get_stock_daily(trade_date)
            for item in stock_daily_data:
                stock_daily_map[item['ts_code']] = {}
                stock_daily_map[item['ts_code']]['pct_chg'] = item['pct_chg']
            print("stock_daily_map", stock_daily_map)
            return render.daily_report(trade_date, detail_map, stock_name_map, stock_daily_map)


# 开盘买 最高卖
def strategy1(buy_open, sell_high):
    pass
    return round(10000 / float(buy_open) * (float(sell_high) - float(buy_open)), 2)


# 开盘买 开盘卖
def strategy2(buy_open, sell_open):
    pass
    return round(10000 / float(buy_open) * (float(sell_open) - float(buy_open)), 2)


def get_random_data():
    pass
    stock_data = mydb.get_stock_list('20200617')
    print
    len(stock_data)
    stock_list = []
    data = []
    test_1 = 0
    test_2 = 0
    for item in stock_data:
        if int(hash(item['vol']) + time.time()) % 1000 > 600 and test_1 < 20:
            item_map = {}
            item_map['ts_code'] = item['ts_code']
            item_map['buy_date'] = '20200615'
            item_map['sell_date'] = '20200616'
            data.append(item_map)
            test_1 += 1
        elif int(hash(item['vol']) + time.time()) % 1000 > 800 and test_2 < 20:
            item_map = {}
            item_map['ts_code'] = item['ts_code']
            item_map['buy_date'] = '20200616'
            item_map['sell_date'] = '20200617'
            data.append(item_map)
            test_2 += 1
    return data


# 随机买 随机卖
def strategy3(buy_low, buy_high, sell_low, sell_high):
    pass
    random_buy = random.uniform(float(buy_low), float(buy_high))
    random_sell = random.uniform(float(sell_low), float(sell_high))
    return round(10000 / random_buy * (random_sell - random_buy), 2)


if __name__ == "__main__":
    app.run()

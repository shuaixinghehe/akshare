#! /usr/bin/env python
# *-* coding:utf-8 *-*
import datetime
import json
import random

import mydb
import web
import string

urls = (
    '/index', 'Index',
    '/check(.*)', 'Check',
    '/daily_report_(.*)', 'DailyReport',
    '/daily_high_report_(.*)', 'DailyHighReport',
    '/daily_industry_report', 'DailyIndustryReport',
    '/create_admin_skill_id', 'CreateAdminSkillId',  # 创建userId
    '/submit_admin_skill_answer', 'SubmitAdminSkillAnswer',  # 提交结果
    '/admin_skill_rank', 'AdminSkillRank',  # 查询结果排行
    '/next_admin_skill_question', 'NextAdminSkillQuestion',  # 查询结果排行
    '/daily_change_aggr_report', 'DailyChangeAggrReport',
    '/daily_top_inst_report', 'DailyTopInstReport',
    '/data_check_report', 'DataCheckReport',
    '/data_js_echart_demo', 'DataJsEchartDemo',
    '/data_echart_admin_skill', 'DataEchartAdminSkill',
    '/stock_change_aggr', 'StockChangeAggr',

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


class StockChangeAggr:
    def GET(self):
        input_data = web.input()
        start_date = input_data.start_date
        end_date = input_data.end_date;
        type = input_data.type
        data = mydb.get_recent_stock_change_aggr(start_date=start_date, end_date=end_date, type=type)
        return render.stock_change_aggr(start_date, end_date, type, data)


class Index:
    def GET(self):
        pass
        today_date_time = datetime.datetime.now()
        trade_date = (today_date_time + datetime.timedelta(0)).strftime("%Y%m%d")
        return render.index(trade_date)


class NextAdminSkillQuestion:
    def POST(self):
        input_data = web.input()
        #  获取下一个预测的stock信息
        # 随机选取100个连续的交易日，展示98个交易日，然后预测99，100两个交易日的涨跌情况
        result_list, selected_ts_code = get_admin_skill_stocks()
        print("result_list", result_list)
        result_list = get_random_stock_daily(result_list)
        print("result json", json.dumps(result_list, ensure_ascii=False))
        start_trade_date = result_list[0][0]
        end_trade_date = result_list[len(result_list) - 2][0]
        predict_trade_date = result_list[len(result_list) - 1][0]
        fact = result_list[len(result_list) - 1][4] > result_list[len(result_list) - 2][2] * 1.01
        params = {
            "user_id": input_data.user_id,
            "ts_code": selected_ts_code,
            "start_trade_date": start_trade_date,
            "end_trade_date": end_trade_date,
            "predict_trade_date": predict_trade_date,
            "fact": str(fact),
            "before_close": result_list[len(result_list) - 2][2],
            "today_high": result_list[len(result_list) - 1][4],
            "process": "(1/50)"
        }
        print("params", params)
        return json.dumps({
            "err_code": 1,
            "stock_daily_list": result_list[0:len(result_list) - 1],
            "selected_ts_code": selected_ts_code,
            "result_list": result_list,
            "params": params
        })


class CreateAdminSkillId:
    def POST(self):
        pass
        input_data = web.input()
        print(input_data.user_id)

        user_id, cnt = get_and_check_user_id(input_data.user_id)

        err_code = 1
        # 1:表示新的userId，2：表示旧userId 3：表示新生成的userId

        if cnt == 0:
            err_code = 1
        elif cnt < 50:
            err_code = 2
        else:
            err_code = 3

        return json.dumps({
            "err_code": err_code,
            "process": "(" + str(int(cnt) % 50) + "/50)",
            "user_id": user_id
        })
        # 提交用户创建的userId，判断是否已经存在，查询用户提交结果表中的userId
        # 查询创建的ID是否满足需求 唯一性；返回结果


def get_and_check_user_id(user_id):
    pass
    data = mydb.get_admin_skill_user_id(user_id)
    cnt = 0
    for item in data:
        cnt = item['cnt']

    if cnt == 0:
        user_id = user_id  # 如果之前不存在，则返回这次userId
    elif cnt < 50:
        user_id = user_id  # 如果之前存在 userId 但是次数没有满50 ，则使用之前的id 继续答题
    else:
        user_id = user_id + '_' + ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 6))

    return user_id, cnt


class SubmitAdminSkillAnswer:
    def POST(self):
        pass
        # 提交用户id，ts_code, start_date,end_date,predict_date,
        # fact,user_answer,result
        input_data = web.input()

        # 1. 检查userId 是否是第一次出现，如果第一次出现，继续执行，
        #  如果是之前数据里面存储，则查询出现的次数，如果满足50个，则
        #  重新创建一个随机的userId，使用继续使用
        # 
        user_id, cnt = get_and_check_user_id(input_data.user_id)

        print("input_data", input_data)
        mydb.insert_admin_skill_answer_log(
            user_id,
            input_data.ts_code,
            input_data.start_trade_date,
            input_data.end_trade_date,
            input_data.predict_trade_date,
            input_data.fact,
            input_data.user_answer,
            input_data.result,
            input_data.detail
        )

        data = mydb.get_admin_skill_user_id(user_id)
        cnt = 0
        for item in data:
            cnt = item['cnt']

        #  获取下一个预测的stock信息
        # 随机选取100个连续的交易日，展示98个交易日，然后预测99，100两个交易日的涨跌情况
        # result_list,selected_ts_code = get_admin_skill_stocks()
        # print("result_list", result_list)
        # result_list = get_random_stock_daily(result_list)
        # print("result json", json.dumps(result_list, ensure_ascii=False))
        # start_trade_date=result_list[0][0]
        # end_trade_date=result_list[len(result_list) - 2][0]
        # predict_trade_date=result_list[len(result_list)-1][0]
        # fact = result_list[len(result_list)-1][4] > result_list[len(result_list)-2][2] * 1.01
        # params = {
        #        "user_id":input_data.user_id,
        #        "ts_code":selected_ts_code,
        #        "start_trade_date":start_trade_date,
        #        "end_trade_date": end_trade_date,
        #        "predict_trade_date":predict_trade_date,
        #        "fact":str(fact),
        #        "process":"(1/50)"
        # }
        # print("params",params)
        err_code = 1
        if cnt == 0:
            err_code = 1
        elif cnt <= 50:
            err_code = 2
        else:
            err_code = 3

        return_result = json.dumps({
            "err_code": err_code,  # 1:表示新的userId，2：表示旧userId 3：表示新生成的userId
            "process": "(" + str(cnt) + "/50)",
            "user_id": user_id
            # "stock_daily_list":result_list[0:len(result_list) - 2],
            # "selected_ts_code":selected_ts_code,
            # "result_list":result_list,
            # "params":params
        })
        print(return_result)
        return return_result


class AdminSkillRank:
    def GET(self):
        pass
        data = mydb.get_answer_log_score_by_user_id()
        return render.admin_skill_log_rank(data)
        # 读取用户提交表，统计每个用户的得分


class DataJsEchartDemo:
    def GET(self):
        # 数据格式 Date,Open,Close,Lowest,Highest
        print("DataJsEchartDemo")
        return render.data_js_echart_demo()


class DataEchartAdminSkill:
    def GET(self):
        # 随机选取100个连续的交易日，展示98个交易日，然后预测99，100两个交易日的涨跌情况
        result_list, selected_ts_code = get_admin_skill_stocks()
        print("result_list", result_list)
        result_list = get_random_stock_daily(result_list)
        print("result json", json.dumps(result_list, ensure_ascii=False))
        start_trade_date = result_list[0][0]
        end_trade_date = result_list[len(result_list) - 2][0]
        predict_trade_date = result_list[len(result_list) - 1][0]
        fact = result_list[len(result_list) - 1][4] > result_list[len(result_list) - 2][2] * 1.01
        params = {
            "user_id": "",
            "ts_code": selected_ts_code,
            "start_trade_date": start_trade_date,
            "end_trade_date": end_trade_date,
            "predict_trade_date": predict_trade_date,
            "fact": str(fact),
            "before_close": result_list[len(result_list) - 2][2],
            "today_high": result_list[len(result_list) - 1][4],
            "process": "(1/50)"
        }
        print("params", params)
        return render.admin_stock_echart_skill(
            json.dumps(result_list[0:len(result_list) - 1], ensure_ascii=False),
            selected_ts_code,
            result_list,
            params
        )


def get_random_stock_daily(result_list):
    pass
    if len(result_list) <= 100:
        return result_list
    else:
        random_index = random.randint(0, len(result_list) - 100)
        return result_list[random_index:random_index + 100]


def get_admin_skill_stocks():
    today_date_time = datetime.datetime.now()
    back_trade_date = (today_date_time + datetime.timedelta(-360)).strftime("%Y%m%d")
    ts_code_list_data = mydb.get_stock_code(back_trade_date)
    ts_code_list = []
    for item in ts_code_list_data:
        ts_code_list.append(item['ts_code'])
    # print("ts_code_list_data lenth", len(ts_code_list), ts_code_list)
    selected_ts_code = ts_code_list[random.randint(0, len(ts_code_list))]
    print("selected ts_code", selected_ts_code)
    stock_daily_history_data = mydb.get_stock_daily_history(back_trade_date, selected_ts_code)
    result_list = []
    for item in stock_daily_history_data:
        # print('trade_date', item['trade_date'], 'high', item['open'])
        result_list.append(
            [item['trade_date'], float(item['open']),
             float(item['close']), float(item['low']),
             float(item['high']), int(float(item['vol']) * 1000)])

    # 随机选取100个连续的交易日，展示98个交易日，然后预测99，100两个交易日的涨跌情况
    # print("result_list", result_list)
    return result_list, selected_ts_code


class DataCheckReport:
    def GET(self):
        pass
        # 需要检查的表名，检查的sql，个数,检查最近5天
        # db存储需要查询的表名，对应的sql结果，比如 tushare.stock_daily , select dt,count(1) cnt from tushare.stock_daily where dt>='{}' group by dt order by dt desc ;
        # create table if not exsits tushare.check_data_report (
        # )
        input_data = web.input()
        trade_date = input_data.trade_date
        check_data_report_map = {}  # key=table_name, value=list
        data = mydb.get_check_data_report()
        trade_date_list = []
        for item in data:
            table_name = item['table_name']
            print('table name', item['table_name'], item['detail'])
            sql = str(item['detail']).format(trade_date)
            cnt_data = mydb.get_tushare_query(item['db_name'], sql)
            check_data_report_map[table_name] = {}
            for cnt_item in cnt_data:
                if cnt_item['trade_date'] not in trade_date_list and table_name == 'stock_daily':
                    trade_date_list.append(cnt_item['trade_date'])
                if 'trade_date' not in check_data_report_map[table_name].keys():
                    check_data_report_map[table_name][cnt_item['trade_date']] = {}
                check_data_report_map[table_name][cnt_item['trade_date']]['trade_date'] = cnt_item['trade_date']
                check_data_report_map[table_name][cnt_item['trade_date']]['cnt'] = cnt_item['cnt']
        trade_date_list = sorted(trade_date_list)
        print("check_data_report_map", check_data_report_map)
        for key in check_data_report_map.keys():
            print("key", check_data_report_map[key])
            print("key", len(check_data_report_map[key]))
            # for item in check_data_report_map[key]:
            #     print("cnt_data", item['trade_date'], item['cnt'])
        print(check_data_report_map, trade_date_list)
        return render.check_data_report(check_data_report_map, trade_date_list)


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
        check_trade_date = (back_trade_date + datetime.timedelta(-90)).strftime("%Y%m%d")
        data = mydb.get_stock_trade_list(check_trade_date)

        trade_data_list = []
        for item in data:
            trade_data_list.append(item['trade_date'])
        back_trade_date = datetime.datetime.strptime(trade_date, '%Y%m%d')
        list_trade_date = (back_trade_date + datetime.timedelta(-90)).strftime("%Y%m%d")
        day_5_before_trade_date = trade_data_list[5]
        day_10_before_trade_date = trade_data_list[10]
        day_20_before_trade_date = trade_data_list[20]
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

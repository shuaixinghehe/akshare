#! /usr/bin/env python
# *-* coding:utf-8 *-*
import random

# 设计一个游戏
# 1000元本金，参与一个获胜期望是60%的游戏，每次下注多少不一定，限定最大交易次数是100次，
# 赢了获取等额的下注金额，输了丢失下注金额
# 可以提前终止交易，求最大利润的交易方法(需要考虑复利计算)

# 每次交易x元，
import time

total_fund = 1000
max_trade_times = 100
exp_record = {}


def trade():
    for per_trade_fund_rate in range(1, 100):  # 每次交易的金额的百分比
        rate = per_trade_fund_rate / 100.0
        experiment_total_fund = total_fund
        for trade_times in range(1, 100):  # 交易的次数
            per_trade_fund_tmp = experiment_total_fund * rate
            if random.randint(0, 99) <= 70:  # 如果盈利
                experiment_total_fund += per_trade_fund_tmp
            else:
                experiment_total_fund -= per_trade_fund_tmp

            if experiment_total_fund <= 0:  # 如果本金小于等于0 实验结束
                break
        increase_rate = (experiment_total_fund - total_fund) * 1.0 / total_fund
        # print "实验 本金1000元 仓位比例:", rate, " 收益:", experiment_total_fund, "收益率:", increase_rate

        exp_record_key = "仓位比例:" + str(rate)
        if exp_record.has_key(exp_record_key):
            exp_record[exp_record_key]['收益'].append(experiment_total_fund)
            exp_record[exp_record_key]['收益率'].append(increase_rate)
        else:
            exp_record[exp_record_key] = {}
            exp_record[exp_record_key]['收益'] = []
            exp_record[exp_record_key]['收益率'] = []
            exp_record[exp_record_key]['收益'].append(experiment_total_fund)
            exp_record[exp_record_key]['收益率'].append(increase_rate)

            # for key in exp_record:
            #     print key, len(exp_record[key]), len(exp_record[key]['收益']), len(exp_record[key]['收益率'])


# 打印每个仓位，平均盈利和平均盈利率
def analysis_exp_record(exp_record_map={}):
    for key in exp_record_map:
        print key, '平均收益:', avg_list(exp_record_map[key]['收益']), '平均收益率:', avg_list(exp_record_map[key]['收益率'])


def avg_list(float_list=[]):
    res = 0.0
    num = 0
    if len(float_list) == 0:
        return 0
    for i in float_list:
        res += i
        num += 1
    return res / num


if __name__ == '__main__':
    t = time.time()
    for i in range(0, 10000):
        trade()
        if i % 1000 == 0:
            print t, time.time() - t
            t = time.time()
    analysis_exp_record(exp_record)

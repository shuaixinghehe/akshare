#! /usr/bin/env python
# *-* coding:utf-8 *-*
import os, sys

from feature_create_stock_basic_detail import download_stock_basic_detail_in_memory
from feature_create_stock_daily import download_stock_daily_in_memory, STOCK_DAILY_MEMORY
from feature_create_stock_daily_basic import STOCK_DAILY_BASIC_MEMORY, download_stock_daily_basic_in_memory
from feature_create_stock_money_flow import download_stock_money_flow_in_memory, get_stock_money_flow_feature, \
    STOCK_MONEY_FLOW_MEMORY
from feature_create_stock_realtime_action_detail_basic import download_stock_realtime_action_detail_basic_in_memory, \
    STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)
LOCAL_SYS_PATH = ['/Users/beacher/Workspace/tushare/tushare/module',
                  '/Users/beacher/Workspace',
                  '/Users/beacher/Workspace/tushare/tushare/module',
                  '/Users/beacher/Workspace/tushare/tushare', ]
for p in LOCAL_SYS_PATH:
    sys.path.append(p)
print("sys.path", sys.path)

import datetime
import json
import math
import time
import tushare_utils
from ak_share_stock_daily import download_ak_stock_daily_hfq_in_memory, download_ak_stock_daily_qfq_in_memory, \
    get_ak_stock_daily_hfq_feature, get_ak_stock_daily_qfq_feature
from stock_realtime_action_basic_detail import get_stock_realtime_action_detail_basic, \
    get_stock_realtime_action_detail_basic_feature

get_stock_realtime_action_detail_basic_feature, get_stock_realtime_action_detail_basic
from tushare_global_config import cur, get_stock_daily_trade_date, get_valid_stock, VALID_TRADE_DATE_LIST, \
    stock_daily_fileds, stock_daily_fileds_list, stock_detail_const_fileds, stock_detail_const_fileds_list, market_map, \
    industry_map, area_map, ak_share_realtime_action_fileds_list, ak_share_realtime_action_fileds, LOG, LOG_INFO, \
    LOG_ERROR
from tushare_global_config import stock_basic_fileds, stock_basic_fileds_list

all_start_time = time.time()

BACK_TRACE_TRADE_DATE_NUM = 60  # 查询多长时间数据
BACK_TRACE_TRADE_DATE_INTERVAL = 30  # 每个股票计算最近多长时间的数据

FEATURES_NAME_LIST = []


# 生成特征
def get_stock_realtime_action_detail_basic_label(key_trade_date='', start_trade_date='', end_trade_date='',
                                                 ts_code=''):
    result = get_stock_realtime_action_detail_basic(start_trade_date, end_trade_date, ts_code)
    result.reverse()  # 默认返回值是最新的日期数据排在前面，最为label 需要逆序
    feature_map = {}
    feature_map['ts_code'] = ts_code
    day_num = 1
    for row in result:
        for index in range(2, len(row)):
            if row[index] is not None and row[index] != 'NaN' and row[index] != 'None' and row[index] != 'nan':
                feature_map[
                    "f" + str(day_num) + "_day_afer_realtime_action_basic_"
                    + ak_share_realtime_action_fileds_list[index]] = row[index]
            else:
                feature_map[
                    "f" + str(day_num) + "_day_after_realtime_action_basic_"
                    + ak_share_realtime_action_fileds_list[index]] = 0.0
        day_num += 1
        if day_num >= 7:  # 只使用最近7天的交易数据
            break

    key = key_trade_date + "_" + ts_code
    label_config_map = get_label_config_map()
    new_feature_map = create_label(label_config_map, feature_map, key)
    return key, new_feature_map


def get_daily_basic_feature(key_trade_date='', start_trade_date='', end_trade_date='', ts_code=''):
    result = get_stock_daily_basic_in_memory(start_trade_date, end_trade_date, ts_code)
    feature_map = {}
    feature_map['ts_code'] = ts_code
    day_num = 0  # 当天为起点
    for row in result:
        for index in range(2, len(row)):
            if row[index] is not None and row[index] != 'NaN' and row[index] != 'None' and row[index] != 'nan':
                feature_map["f" + str(day_num) + "_day_before_daily_basic_" + stock_basic_fileds_list[index]] = row[
                    index]
            else:
                LOG_INFO("get_daily_basic_feature", key_trade_date, ts_code, "value is None")
                feature_map["f" + str(day_num) + "_day_before_daily_basic_" + stock_basic_fileds_list[index]] = 0.0
        day_num += 1

    key = key_trade_date + "_" + ts_code

    return key, feature_map


def get_daily_feature(key_trade_date='', start_trade_date='', end_trade_date='', ts_code=''):
    result = get_stock_daily_in_memory(start_trade_date, end_trade_date, ts_code)
    feature_map = {}
    feature_map['ts_code'] = ts_code
    day_num = 0
    for row in result:
        for index in range(2, len(row)):
            if row[index] is not None and row[index] != 'NaN' and row[index] != 'None' and row[index] != 'nan':
                feature_map["f" + str(day_num) + "_day_before_daily_" + stock_daily_fileds_list[index]] = row[
                    index]
            else:
                feature_map["f" + str(day_num) + "_day_before_daily_" + stock_daily_fileds_list[index]] = 0.0
        day_num += 1

    key = key_trade_date + "_" + ts_code

    # feature_config_map = get_feature_config_map()
    # new_feature_map = create_feature(feature_config_map, feature_map, key)
    # print "get_daily_feature new feature map", feature_map
    return key, feature_map


def get_daily_label(key_trade_date='', start_trade_date='', end_trade_date='', ts_code=''):
    result = get_stock_daily_in_memory(start_trade_date, end_trade_date, ts_code)
    result.reverse()  # 默认返回值是最新的日期数据排在前面，最为label 需要逆序
    feature_map = {}
    feature_map['ts_code'] = ts_code
    day_num = 1  # 明天
    for row in result:
        for index in range(2, len(row)):
            if row[index] is not None and row[index] != 'NaN' and row[index] != 'None' and row[index] != 'nan':
                feature_map["f" + str(day_num) + "_day_after_daily_" + stock_daily_fileds_list[index]] = row[
                    index]
            else:
                feature_map["f" + str(day_num) + "_day_after_daily_" + stock_daily_fileds_list[index]] = 0.0
        day_num += 1

    key = key_trade_date + "_" + ts_code

    label_config_map = get_label_config_map()
    new_feature_map = create_label(label_config_map, feature_map, key)
    # print "get_daily_label new feature map", new_feature_map
    return key, new_feature_map


def write_feature_name_and_values(text="text", path="", values=[], mode="a+"):
    ofile = open(path, mode)
    ofile.write(','.join([str(s) for s in values]) + "\n")
    ofile.close()


def get_stock_daily_basic_in_memory(start_trade_date, end_trade_date, ts_code):
    result = []
    # TODO: sb 操作
    for trade_date in VALID_TRADE_DATE_LIST:
        if trade_date >= start_trade_date and trade_date <= end_trade_date:
            key = str(ts_code) + "_" + str(trade_date)
            temp_result = []
            if key in STOCK_DAILY_BASIC_MEMORY.keys():
                for filed in stock_basic_fileds_list:
                    temp_result.append(STOCK_DAILY_BASIC_MEMORY[key][filed])
                result.append(temp_result)
                # LOG_INFO("find stock_daily_basic_in_memory", key, key in STOCK_DAILY_BASIC_MEMORY.keys(),
                #          len(STOCK_DAILY_BASIC_MEMORY.keys()))
            else:
                LOG_ERROR("get_stock_daily_basic_in_memory no key:", key,
                          key in STOCK_DAILY_BASIC_MEMORY.keys(),
                          len(STOCK_DAILY_BASIC_MEMORY.keys()))
    return result


def get_stock_daily_in_memory(start_trade_date, end_trade_date, ts_code):
    result = []
    # TODO: sb 操作
    for trade_date in VALID_TRADE_DATE_LIST:  # 逆序，最新的日期排在最前面
        if trade_date >= start_trade_date and trade_date <= end_trade_date:
            key = str(ts_code) + "_" + str(trade_date)
            temp_result = []
            if key in STOCK_DAILY_MEMORY.keys():
                for filed in stock_daily_fileds_list:
                    temp_result.append(STOCK_DAILY_MEMORY[key][filed])
                result.append(temp_result)
            else:
                LOG_ERROR("get_stock_daily_in_memory no key", str(key),
                          key in STOCK_DAILY_MEMORY.keys()
                          , len(STOCK_DAILY_MEMORY.keys()))
    return result


# 构造特征
def create_feature(feature_config_map={}, feature_map={}, key_name=""):
    feature_key_list = tushare_utils.load_local_json_file_keys_in_order('../config/feature_map.json')
    for key in feature_key_list:
        try:
            value = round(float(eval(feature_config_map[key], {'__builtins__': {}}, feature_map)), 2)
            feature_map[key] = value
        except Exception as  e:
            LOG_ERROR("exception key,value,globle_key_name", key, feature_config_map[key], key_name)
            LOG_ERROR('exception', e, str(e))
            LOG_ERROR("exception create_feature_map feature:", feature_map)
    return feature_map


# 构造label
def create_label(feature_config_map={}, feature_map={}, key_name=""):
    for key in feature_config_map.keys():
        try:
            value = eval(feature_config_map[key], {'__builtins__': {}}, feature_map)
            feature_map[key] = value
        except Exception as  e:
            LOG_ERROR("exception key,value,globle_key_name", key, feature_config_map[key], key_name)
            LOG_ERROR('exception', e, str(e))
            LOG_ERROR("exception create_feature_map feature:", feature_map)
    return feature_map


def get_label_config_map():
    label_config_map = get_config_map('../config/label.json')
    return label_config_map


def get_feature_config_map():
    label_config_map = get_config_map('../config/feature_map.json')
    return label_config_map


def get_config_map(file_path=''):
    config_json = tushare_utils.load_local_json_file(file_path)
    config_map = json.loads(config_json)
    return config_map


# 随机抽样，懒得写了，就取topN
def sample(text="", feature_map={}, sample_size=0):
    LOG.info(text)
    sample_size = min(len(feature_map), sample_size)
    keys = feature_map.keys()
    for i in range(0, sample_size):
        LOG_INFO("sample", feature_map[keys[i]])


def statistic(lable_feature_map={}):
    positive_cnt = 0
    negtive_cnt = 0

    negtive_sample_key_list = []
    for key in lable_feature_map.keys():
        if lable_feature_map[key]['label'] == True:
            positive_cnt += 1
        elif lable_feature_map[key]['label'] == False:
            negtive_cnt += 1
            negtive_sample_key_list.append(key)
        else:
            LOG_INFO("error label", key)
    LOG_INFO("positive_cnt ", str(positive_cnt), "negative_cnt ", str(negtive_cnt))
    LOG_INFO("create feature total elapsed ", str(time.time() - all_start_time))


def run_create_feature(stock_daily_basic_detail_map={}, type='train'):
    print("start run_create_feature type" + type)
    LOG_INFO("开始构造特征", type)
    global_feature_map = {}  # 存储所有的数据
    global_label_map = {}  # 存储label

    all_start_time = time.time()
    start_index = 2  # 从2天前的数据开始训练
    if type == 'predict':
        start_index = 0  # 预测从当天的数据开始训练

    for i in range(start_index, BACK_TRACE_TRADE_DATE_INTERVAL):
        start_time = time.time()
        for ts_code in valid_stock_list:
            key_trade_date = back_trace_trade_date_list[i]  # 当天的key，站在2天前，准备数据
            start_trade_date = back_trace_trade_date_list[i + BACK_TRACE_TRADE_DATE_INTERVAL]  # 两天后，再往后推30天的数据
            end_trade_date = back_trace_trade_date_list[i]  # 两天后的数据

            key, features = get_daily_basic_feature(key_trade_date=key_trade_date,
                                                    start_trade_date=start_trade_date,
                                                    end_trade_date=end_trade_date, ts_code=ts_code)
            global_feature_map[key] = {}
            global_feature_map[key] = dict(global_feature_map[key], **features)

            key, features = get_daily_feature(key_trade_date=key_trade_date,
                                              start_trade_date=start_trade_date,
                                              end_trade_date=end_trade_date, ts_code=ts_code)
            global_feature_map[key] = dict(global_feature_map[key], **features)
            # 填充板块，地域，行业信息
            global_feature_map[key] = dict(global_feature_map[key], **stock_daily_basic_detail_map[ts_code])

            key, features = get_stock_money_flow_feature(key_trade_date=key_trade_date,
                                                         start_trade_date=start_trade_date,
                                                         end_trade_date=end_trade_date, ts_code=ts_code)

            # 填充资金流向
            global_feature_map[key] = dict(global_feature_map[key], **features)

            # 填充实时交易数据的基本信息
            key, features = get_stock_realtime_action_detail_basic_feature(key_trade_date=key_trade_date,
                                                                           start_trade_date=start_trade_date,
                                                                           end_trade_date=end_trade_date,
                                                                           ts_code=ts_code)
            global_feature_map[key] = dict(global_feature_map[key], **features)

            # # 填充赋权的数据
            # key, features = get_ak_stock_daily_hfq_feature(key_trade_date=key_trade_date,
            #                                                start_trade_date=start_trade_date,
            #                                                end_trade_date=end_trade_date, ts_code=ts_code)
            # global_feature_map[key] = dict(global_feature_map[key], **features)
            #
            # key, features = get_ak_stock_daily_qfq_feature(key_trade_date=key_trade_date,
            #                                                start_trade_date=start_trade_date,
            #                                                end_trade_date=end_trade_date, ts_code=ts_code)
            # global_feature_map[key] = dict(global_feature_map[key], **features)

            global_label_map[key] = {}

            label_index = i
            # 获取label的数据范围
            if type == 'predict':
                label_index = i + 2
            label_start_trade_date = back_trace_trade_date_list[label_index - 1]  # 未来第一天的数据
            label_end_trade_date = back_trace_trade_date_list[label_index - 2]  # 未来第二天的数据
            key, label_feature_map = get_stock_realtime_action_detail_basic_label(key_trade_date=key_trade_date,
                                                                                  start_trade_date=label_start_trade_date,
                                                                                  end_trade_date=label_end_trade_date,
                                                                                  ts_code=ts_code)
            global_label_map[key] = dict(global_label_map[key], **label_feature_map)
        LOG_INFO("start create feature ", i, " round elapsed", time.time() - start_time)
        if type == "predict":
            break
    today = datetime.datetime.now().strftime('%Y%m%d')

    statistic(global_label_map)

    # 根据json 生成特征
    feature_config_map = get_feature_config_map()
    for key in global_feature_map.keys():
        new_feature_map = create_feature(feature_config_map, global_feature_map[key], key)
        global_feature_map[key] = new_feature_map
        # print "根据json 生成特征 ", time.time()
    LOG_INFO("create json config feature elapsed", time.time() - all_start_time)
    # 根据 json 生成label 在构造label 函数里面完成了

    # 读取忽略的feature_name
    ignore_feature_name = {}
    ofile = open("../config/ignore_feature_name.txt", 'r')
    for line in ofile:
        ignore_feature_name[line.strip()] = True

    # 写feature_name
    global_feature_name_list = []
    for key in global_feature_map.keys():
        for name in global_feature_map[key]:
            if str(name).startswith('f') and str(name) not in ignore_feature_name.keys():  # f开头代表特征
                global_feature_name_list.append(name)
        break
    write_feature_name_and_values("feature_names", '../train_data/feature_names_' + today + ".txt",
                                  global_feature_name_list, "w+")
    # print "global_feature_map", global_feature_map
    # print "global_label_map", global_label_map
    # 拼接数据 写入文件
    LOG_INFO("start write file ", time.time())
    file_name = "../train_data/train_data_"
    if type == "predict":
        file_name = "../train_data/predict_data_"
    for key in global_label_map.keys():
        write_train_data_list = []
        write_train_data_list.append(key)
        write_train_data_list.append(global_label_map[key]['label'])
        for feature_name in global_feature_name_list:
            if not math.isnan(float(global_feature_map[key][feature_name])):
                write_train_data_list.append(global_feature_map[key][feature_name])
            else:
                # print("write_train_data_list is None", key, feature_name)
                write_train_data_list.append(-1.0)
        write_feature_name_and_values("train data", file_name + today + '.txt', write_train_data_list,
                                      'a+')

    LOG_INFO("all_time:", time.time() - all_start_time)


# 创建训练数据

if __name__ == '__main__':
    # 获取需要计算的日期,回溯多长时间
    LOG_INFO("开始计算训练数据")
    back_trace_trade_date_list = get_stock_daily_trade_date()
    # 根据交易日list，获取最近BACK_TRACE_TRADE_DATE_NUM 的日期
    back_trace_start_trade_date = back_trace_trade_date_list[BACK_TRACE_TRADE_DATE_NUM]
    # 获取需要计算的股票，
    # 条件最近每天都可以交
    valid_stock_list = get_valid_stock(back_trace_start_trade_date, today_date=back_trace_trade_date_list[0])
    LOG_INFO("可以回溯的交易日:", len(back_trace_trade_date_list))
    LOG_INFO("开始交易日", back_trace_trade_date_list[0], '结束交易日', back_trace_start_trade_date)
    LOG_INFO("可以回溯的股票:", len(valid_stock_list))
    today = datetime.datetime.now()
    start_date = (today + datetime.timedelta(-1 * BACK_TRACE_TRADE_DATE_NUM * 2)).strftime("%Y%m%d")

    # 下载数据到内存，股票的基本信息
    LOG_INFO("下载数据到内存，股票的基本信息")
    LOG_INFO("today", today, 'start_date', start_date)

    stock_realtime_action_detai_basic_map = download_stock_realtime_action_detail_basic_in_memory(
        start_trade_date=start_date, ts_code_list=valid_stock_list)

    stock_daily_basic_memory = download_stock_daily_basic_in_memory(start_trade_date=start_date,
                                                                    ts_code_list=valid_stock_list)
    LOG_INFO("stock_daily_basic_memory", len(stock_daily_basic_memory))

    stock_daily_memory = download_stock_daily_in_memory(start_trade_date=start_date,
                                                        ts_code_list=valid_stock_list)
    LOG_INFO("stock_daily_memory", len(stock_daily_memory))

    stock_daily_basic_detail_map = download_stock_basic_detail_in_memory(today_date=back_trace_trade_date_list[0])
    LOG_INFO("stock_daily_basic_detail_map", len(stock_daily_basic_detail_map))

    # 资金买入情况 没啥用
    stock_money_flow = download_stock_money_flow_in_memory(start_trade_date=start_date, ts_code_list=valid_stock_list)
    LOG_INFO("stock_money_flow", len(stock_money_flow))

    # 不使用赋权数据
    # # 复权的数据
    # ak_share_stock_daily_hfq_map = download_ak_stock_daily_hfq_in_memory(start_trade_date=start_date,
    #                                                                      ts_code_list=valid_stock_list)
    # LOG_INFO("ak_share_stock_daily_hfq_map", len(ak_share_stock_daily_hfq_map))
    #
    # ak_share_stock_daily_qfq_map = download_ak_stock_daily_qfq_in_memory(start_trade_date=start_date,
    #                                                                      ts_code_list=valid_stock_list)
    # LOG_INFO("ak_share_stock_daily_qfq_map", len(ak_share_stock_daily_qfq_map))

    # 检查数据 feature 特征
    LOG_INFO('check features')
    # LOG_INFO('实时股票交易数据特征', len(stock_realtime_action_detai_basic_map.keys()))
    # LOG_INFO('实时股票成交量换手率基本信息', len(stock_daily_basic_memory.keys()))
    # LOG_INFO('实时股票价格基本信息', len(stock_daily_memory.keys()))
    # LOG_INFO('实时股票资金流向', len(stock_money_flow.keys()))

    LOG_INFO('实时股票交易数据特征', len(STOCK_REALTIME_ACTION_DETAIL_BASIC_MEMORY.keys()))
    LOG_INFO('实时股票成交量换手率基本信息', len(STOCK_DAILY_BASIC_MEMORY.keys()))
    LOG_INFO('实时股票价格基本信息', len(STOCK_DAILY_MEMORY.keys()))
    LOG_INFO('实时股票资金流向', len(STOCK_MONEY_FLOW_MEMORY.keys()))

    if len(stock_daily_basic_memory) != len(STOCK_DAILY_MEMORY):
        LOG_ERROR("ERROR feature size  not same ", len(stock_daily_basic_memory), len(stock_daily_memory))
    else:
        pass
    # run_create_feature(stock_daily_basic_detail_map=stock_daily_basic_detail_map, type='train')
    run_create_feature(stock_daily_basic_detail_map=stock_daily_basic_detail_map, type='predict')

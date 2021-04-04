# ! /usr/bin/env python
# *-* coding:utf-8 *-*
import tushare_utils
import json

BACK_TRACE_DATE_LIST = []


def create_stock_daily_feature_map_json():
    fileds = "`high`,`change`,`pct_chg`,`vol`,`amount` "
    fileds_list = fileds.replace("`", "").replace(" ", "").split(",")
    day_num_list = [3, 4, 5, 6, 7, 12, 17]

    for filed in fileds_list:
        fenzi = "f2_day_before_daily_" + filed
        for day_num in day_num_list:
            key = "f2_"
            key += str(day_num)
            key += "_" + filed + "_rate"
            fenmu = "(f" + str(day_num) + "_day_before_daily_" + filed + "+0.1)"
            print """ "{}": "{}", """.format(key, fenzi + " / " + fenmu)


def create_stock_daily_basic_feature_map_json():
    stock_basic_fileds = "`close`,`turnover_rate`,`turnover_rate_f`,`volume_ratio`,`pe`," \
                         "`pe_ttm`,`pb`,`ps`,`ps_ttm`,`total_share`,`float_share`,`free_share`,`total_mv`,`circ_mv`"
    stock_basic_fileds_list = stock_basic_fileds.replace("`", "").replace(" ", "").split(",")
    day_num_list = [3, 4, 5, 6, 7, 12, 17]

    for filed in stock_basic_fileds_list:
        fenzi = "f2_day_before_daily_basic_" + filed
        for day_num in day_num_list:
            key = "f2_"
            key += str(day_num)
            key += "_" + filed + "_rate"
            fenmu = "(f" + str(day_num) + "_day_before_daily_basic_" + filed + "+0.1)"
            print """ "{}": "{}", """.format(key, fenzi + " / " + fenmu)


if __name__ == '__main__':
    pass
    create_stock_daily_feature_map_json()
    print
    create_stock_daily_basic_feature_map_json()

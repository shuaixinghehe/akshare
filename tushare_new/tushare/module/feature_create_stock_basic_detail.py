#! /usr/bin/env python
# *-* coding:utf-8 *-*
import time

from tushare_global_config import LOG_INFO, stock_basic_fileds, cur, stock_basic_fileds_list, LOG_ERROR, LOG, \
    stock_daily_fileds, stock_daily_fileds_list, stock_detail_const_fileds, stock_detail_const_fileds_list, market_map, \
    industry_map, area_map


def download_stock_basic_detail_in_memory(today_date=''):
    LOG_INFO("download_stock_basic_detail_in_memory ", today_date)
    sql = "select " + stock_detail_const_fileds + " from stock_basic where dt=%s and area!=%s and market!=%s and market!=%s"
    LOG_INFO("download_stock_basic_detail_in_memory sql", sql)
    cur.execute(sql, (today_date, 'None', 'None', "CDR"))
    result = cur.fetchall()
    stock_basic_detail_map = {}
    num = 0
    for row in result:
        stock_basic_detail_map[str(row[0])] = {}
        feature_map = {}
        num += 1
        # LOG_INFO("download_stock_basic_detail_in_memory process", num * 1.0 / len(result))
        for index in range(1, len(stock_detail_const_fileds_list)):
            if stock_detail_const_fileds_list[index] == 'market':
                feature_map['f_' + stock_detail_const_fileds_list[index]] = float(market_map[row[index]])
            elif stock_detail_const_fileds_list[index] == 'industry':
                feature_map['f_' + stock_detail_const_fileds_list[index]] = float(industry_map[row[index]])
            elif stock_detail_const_fileds_list[index] == 'area':
                feature_map['f_' + stock_detail_const_fileds_list[index]] = float(area_map[row[index]])
            else:
                LOG.error("ERROR not match in download_stock_basic_detail_in_memory")
        stock_basic_detail_map[str(row[0])] = feature_map
    return stock_basic_detail_map





if __name__ == '__main__':
    pass

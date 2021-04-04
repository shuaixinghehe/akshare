#! /usr/bin/env python
# *-* coding:utf-8 *-*


stock_list = [
    '20200617|002400.SZ',
    '20200617|300816.SZ',
    '20200617|300346.SZ',
    '20200617|002103.SZ',
    '20200617|300299.SZ'
]

for item in stock_list:
    stock = item.split('|')[0]
    probility = item.split('|')[1]
    print "insert into model_reco_stock_detail (`model_name`,`ts_code`,`reco_time`,`buy_date`,`sell_date`,`threshold`) values ('train_model.m2020-06-14T14:23:38.114556','%s','20200617','20200618','20200619','%s');" % (
        stock, probility)

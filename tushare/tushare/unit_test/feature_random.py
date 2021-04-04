#! /usr/bin/env python
# *-* coding:utf-8 *-*
import random

# 把feature name 和特征 存储到外部存储
import datetime

from module.create_feature import write_feature_name_and_values

if __name__ == '__main__':
    pass
    print random.random(), int(random.random() * 100)
    m = {}
    m['20191127_300110.SZ'] = "xx"
    print  m
    del m['20191127_300110.SZ']
    print  m
    write_feature_name_and_values("test", "./test1.txt", [True] + [1, 2, 3, 46.0, -1, 20], 'a+')
    today = datetime.datetime.now()
    start_date = (today + datetime.timedelta()).strftime("%Y%m%d")
    print today

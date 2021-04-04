#! /usr/bin/env python
# *-* coding:utf-8 *-*
import time

FEATURE_NAMES_LIST = []
FEATURE_NAMES_SET = {}


def create_feature_names():
    pass
    ofile = open("../config/feature_names.txt")
    for line in ofile:
        line = line.strip()
        line = line.replace("\"", '').replace(',', '')
        FEATURE_NAMES_LIST.append(line)
        FEATURE_NAMES_SET[line] = True


if __name__ == '__main__':
    print time.time()
    create_feature_names()
    print time.time()
    for i in range(0, 100000):
        "asdfasdfwer" in FEATURE_NAMES_LIST
    print time.time()
    for i in range(0, 100000):
        FEATURE_NAMES_SET.has_key("asdfasdfwer")
    print time.time()
    for i in range(0, 100000):
        "asdfasdfwer" in FEATURE_NAMES_SET.keys()
    print time.time()

    print "f1_day_before_daily_change".index("change")

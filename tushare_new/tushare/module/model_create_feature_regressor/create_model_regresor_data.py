#! /usr/bin/env python
# *-* coding:utf-8 *-*
import datetime
import json
import math
import time
from collections import deque
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import numpy as np


def get_regression_data(file_path='', target_list=[]):
    pass

    ofile = open(file_path, 'r')
    feature_data_map = {}
    for line in ofile:
        line = line.strip()
        arr = line.split(',')
        key = arr[0]
        features_list = arr[2:]
        value_list = arr[1]
        ts_code = key.split('_')[1]
        trade_date = key.split('_')[0]
        if ts_code in target_list:
            print('ts_code', ts_code, 'trade_date', trade_date)
            if ts_code not in feature_data_map.keys():
                feature_data_map[ts_code] = {}
                feature_data_map[ts_code][trade_date] = arr
            else:
                if trade_date in feature_data_map[ts_code].keys():
                    print("error")
                    pass
                else:
                    feature_data_map[ts_code][trade_date] = arr
    for key in feature_data_map.keys():
        trade_date_list = feature_data_map[key].keys()
        trade_date_list = sorted(trade_date_list)
        ofile = open('./' + key + ".txt", 'w')
        for trade_date_key in trade_date_list:
            print('line', key, trade_date_key, feature_data_map[key][trade_date_key])
            data_str = ""
            for v in feature_data_map[key][trade_date_key]:
                data_str += v + ","
            data_str = data_str[:-1]
            ofile.write(data_str + "\n")
        ofile.close()


def train_model(file_path='', ts_code='', predict_data=[]):
    pass
    X = []
    Y = []
    ofile = open(file_path, 'r')
    for line in ofile:
        line = line.strip()
        arr = line.split(',')
        X.append(arr[2:])
        Y.append(arr[1])
    X = np.array(X)
    Y = np.array(Y)
    X = X.astype(np.float64)
    Y = Y.astype(np.float64)
    # Train classifiers
    reg1 = GradientBoostingRegressor(random_state=1)
    reg2 = RandomForestRegressor(random_state=1)
    reg3 = LinearRegression()

    X_train = X[0:-1]
    X_predict = X[-1:]

    Y_train = Y[0:-1]
    Y_predict = Y[-1:0]

    reg1.fit(X_train, Y_train)
    reg2.fit(X_train, Y_train)
    reg3.fit(X_train, Y_train)

    print("reg1 sore", reg1.score(X_predict, Y_predict))
    print("reg2 sore", reg2.score(X_predict, Y_predict))
    print("reg3 sore", reg3.score(X_predict, Y_predict))

    print("reg1 predict", reg1.predict(X_predict))
    print("reg2 predict", reg2.predict(X_predict))
    print("reg3 predict", reg3.predict(X_predict))


if __name__ == '__main__':
    file_path = '/Users/beacher/Workspace/tushare/tushare/train_data/train_data_20200709.txt'
    target_list = [
        '601788.SH',
        '603019.SH',
        '002797.SZ',
        '000066.SZ',
        '300059.SZ',
        '002239.SZ',
        '600415.SH',
        '300433.SZ',
        '000063.SZ',
    ]
    # get_regression_data(file_path=file_path, target_list=target_list)
    pass
    train_model(file_path='./000063.SZ.txt')

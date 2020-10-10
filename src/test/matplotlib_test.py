# coding:utf8
from datetime import datetime

import matplotlib.pyplot as plt
import pymysql
import random

ts_conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                          password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                          db="tushare", \
                          charset='utf8')

ts_cur = ts_conn.cursor()

ak_conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                          password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                          db="akshare", \
                          charset='utf8')

ak_cur = ak_conn.cursor()

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def test():
    plt.plot(['20200801', '20200802', '20200803', '20200804'], [1, 4, 9, 16])
    plt.ylabel('some numbers')
    plt.show()


def draw_shangzheng():
    sql = "select * from index_daily where ts_code in ('000001.SH') order by trade_date"
    ts_cur.execute(sql)
    result = ts_cur.fetchall()
    trade_date_list = []
    value_list = []
    profit_list_1 = []
    total = 100000.0
    for row in result:
        trade_date_list.append(datetime.strptime(str(row[1]), "%Y%m%d"))
        value_list.append(float(row[3]))
        if random.random() > 0.5:
            stock_num = total / float(row[3])

    plt.plot_date(trade_date_list, value_list, linestyle='solid', label='上证')
    plt.ylabel(u'上证指数')
    plt.legend()
    plt.xticks(rotation=-15)  # 设置x轴标签旋转角度
    plt.show()


def draw_plot_date():
    from matplotlib.dates import (YEARLY, DateFormatter,
                                  rrulewrapper, RRuleLocator, drange)
    import numpy as np
    import datetime

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    # tick every 5th easter
    rule = rrulewrapper(YEARLY, byeaster=1, interval=5)
    loc = RRuleLocator(rule)
    formatter = DateFormatter('%m/%d/%Y')
    date1 = datetime.date(2020, 1, 1)
    date2 = datetime.date(2020, 8, 21)
    delta = datetime.timedelta(days=1)

    dates = drange(date1, date2, delta)
    s = np.random.rand(len(dates))  # make up some random y values

    fig, ax = plt.subplots()
    plt.plot_date(dates, s, linestyle='solid')
    # ax.xaxis.set_major_locator(loc)
    # ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)

    plt.show()


if __name__ == '__main__':
    pass
    draw_shangzheng()
    start_date = datetime.strptime("20160607", "%Y%m%d")
    print(start_date)

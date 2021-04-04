#! /usr/bin/env python
# *-* coding:utf-8 *-*
import time
import tushare as ts
import pymysql.cursors
import sys
LOCAL_SYS_PATH = ['/Users/beacherlu/Workspace/akshare/tushare/tushare/module',
                  '/Users/beacherlu/Workspace/akshare',
                  '/Users/beacherlu/Workspace/akshare/tushare/tushare/module',
                  '/Users/beacherlu/Workspace/akshare/tushare/tushare', ]
for p in LOCAL_SYS_PATH:
    sys.path.append(p)
print("sys.path", sys.path)

from tushare_utils import LOG_INFO, perf

# reload(sys)
# sys.setdefaultencoding('utf8')

ts.set_token('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
pro = ts.pro_api('dc621482aab3c02b5420b3e63919c38bacccf42170d57b4fd005bb1c')
conn = pymysql.connect(host="127.0.0.1", user="tushare", \
                       password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                       db="tushare", \
                       charset='utf8')
cur = conn.cursor()


def download_stock_daily_basic(trade_date=''):
    sql = """
            insert into stock_daily_basic (
                 `ts_code`, `trade_date`, `close`, `turnover_rate`,
                 `turnover_rate_f`, `volume_ratio`, `pe`, `pe_ttm`, `pb`,
                  `ps`, `ps_ttm`,`total_share`,`float_share`,`free_share`,`total_mv`,
                  `circ_mv`
            )
            values
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s );
            """
    is_need_downloaded = True
    while is_need_downloaded:
        try:
            df = pro.daily_basic(ts_code='',
                                 trade_date=trade_date,
                                 fields='ts_code, trade_date, close, turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,ps_ttm,total_share,float_share,free_share,total_mv,circ_mv'
                                 )
            time.sleep(1)
            is_need_downloaded = False
        except Exception as  e:
            print("retry stock_daily_basic")

    for index, row in df.iterrows():
        # print row
        result = cur.execute(sql, (
            str(row['ts_code']).encode('utf-8'),
            str(row['trade_date']).encode('utf-8'),
            str(row['close']).encode('utf-8'),
            str(row['turnover_rate']).encode('utf-8'),
            str(row['turnover_rate_f']).encode('utf-8'),
            str(row['volume_ratio']).encode('utf-8'),
            str(row['pe']).encode('utf-8'),
            str(row['pe_ttm']).encode('utf-8'),
            str(row['pb']).encode('utf-8'),
            str(row['ps']).encode('utf-8'),
            str(row['ps_ttm']).encode('utf-8'),
            str(row['total_share']).encode('utf-8'),
            str(row['float_share']).encode('utf-8'),
            str(row['free_share']).encode('utf-8'),
            str(row['total_mv']).encode('utf-8'),
            str(row['circ_mv']).encode('utf-8')
        ))
        conn.commit()
        LOG_INFO("stock_daily_basic", row['ts_code'], row['trade_date'], result)
        perf(namespace='stock_daily_basic', subtag=row['ts_code'])


if __name__ == '__main__':
    pass
    print('参数个数为:', len(sys.argv), '个参数。')
    print('参数列表:', str(sys.argv))
    today_date = sys.argv[1]
    # today_date = time.strftime("%Y%m%d", time.localtime())
    print(today_date)
    download_stock_daily_basic(today_date)

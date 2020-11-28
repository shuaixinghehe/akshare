#
import akshare as ak
import time


def history_realime_data():
    stock_zh_a_tick_tx_df = ak.stock_zh_a_tick_tx(code="sh603881", trade_date="20200605")
    print(stock_zh_a_tick_tx_df)
    for index, row in stock_zh_a_tick_tx_df.iterrows():
        print(index)

        print(row['成交时间'])
    # stock_zh_a_tick_tx_df.to_csv('stock_zh_a_tick_tx_df', index=False, sep=' ', encoding='utf_8_sig')


# 全量实时数据
def all_realtime_data():
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    print(stock_zh_a_spot_df)
    print(type(stock_zh_a_spot_df))
    for row in stock_zh_a_spot_df.items:
        print(row)
    stock_zh_a_spot_df.to_csv('result.txt', index=True, sep=' ', encoding='utf_8_sig')


def stock_zh_a_daily():
    stock_zh_a_daily_hfq_df = ak.stock_zh_a_daily(symbol="sz002351", adjust="")
    print(stock_zh_a_daily_hfq_df)
    stock_zh_a_daily_hfq_df.to_csv('stock_zh_a_daily_default', index=True, sep=' ', encoding='utf_8_sig')


def realtime_data():
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    print(stock_zh_a_spot_df)
    time_str = str(time.time())
    print(time_str)
    stock_zh_a_spot_df.to_csv('test_stock_zh_a_spot_df' + time_str, index=True, sep=' ', encoding='utf_8_sig')

../test/interface_test.py


if __name__ == '__main__':
    print("股市有风险，入市需谨慎")
    print("目标翻一倍")
    # history_realime_data()
    # stock_zh_a_daily()
    realtime_data()

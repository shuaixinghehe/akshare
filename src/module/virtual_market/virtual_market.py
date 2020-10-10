#! /usr/bin/env python
# *-* coding:utf-8 *-*
import virtual_mydb
from enum import Enum


# 市场类
class VirtaulMarket:
    # 判断是否可以交易,根据提交的时间，价格和数量，判断交易情况
    # 返回值为 trade_result
    #
    def trade(self, code, trade_date, timestamp, price, volumn):
        pass
        # 获取当天价格的交易量
        trade_volumn = virtual_mydb.get_code_volumn_by_price(code=code, trade_date=trade_date, timestamp=timestamp,
                                                             price=price)
        result = MarketTradeResult
        # 确认当前价格的当天交易量，然后交易量如果大于申请的交易量的1。2倍 就默认可以全部成交
        # TODO: 交易逻辑存在问题，整手交易
        if trade_volumn >= volumn * 1.2:  # 权量成交
            result.success_trade_volumn = volumn
            result.trade_result = TradeResult.TOTAL_TRADE
        elif trade_volumn > 0 and trade_volumn < volumn * 1.2:  # 部分成交
            result.trade_result = TradeResult.PART_TRADE
            result.success_trade_volumn = int(min(trade_volumn * 0.8, volumn * 0.8))
        elif trade_volumn == 0:  # 没有成交
            result.success_trade_volumn = 0
            result.trade_result = TradeResult.FAIL_TRADE
        return result


class TradeResult(Enum):
    TOTAL_TRADE = 1  # 权量成交
    PART_TRADE = 2  # 部分成交
    FAIL_TRADE = 3  # 没有成交


class MarketTradeResult:
    trade_result = TradeResult.FAIL_TRADE  # 交易结果
    success_trade_volumn = 0  # 成功交易数量


if __name__ == '__main__':
    pass
    print(MarketTradeResult.trade_result)
    VirtaulMarket.trade(code='', trade_date='', timestamp='', price='', volumn='')

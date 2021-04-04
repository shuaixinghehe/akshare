import web

db_akshare = web.database(dbn='mysql', db='akshare', user='tushare', pw='&QwX0^4#Sm^&t%V6wBnZC%78')
db_tushare = web.database(dbn='mysql', db='tushare', user='tushare', pw='&QwX0^4#Sm^&t%V6wBnZC%78')
t = db_akshare.transaction()


def get_model_reco_stock_detail(model_name):
    data = db_akshare.select('model_reco_stock_detail', where='model_name=$model_name', vars=locals())
    return data


def get_stock_detail(ts_code, trade_date):
    return db_tushare.select('stock_daily', where='ts_code=$ts_code and trade_date=$trade_date', vars=locals())


def get_stock_list(trade_date):
    return db_tushare.select('stock_daily', where='trade_date=$trade_date', vars=locals())

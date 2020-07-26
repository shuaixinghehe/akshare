def create_total_down():
    sql = """
        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<={} and convert(pct_chg,DECIMAL(5,2))> {} ,1,0)) as char) down_{}_{}_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<={} and convert(pct_chg,DECIMAL(5,2))>{},ts_code,null)) down_{}_{}_stock_set,
    """
    for i in range(1, 10):
        print(sql.format(i * 1.0 * -1, i * 1.0 * -1 - 1, i, i + 1, i * 1.0 * -1, i * 1.0 * -1 - 1, i, i + 1))


def create_total_up():
    sql = """
        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>={} and convert(pct_chg,DECIMAL(5,2))< {} ,1,0)) as char) up_{}_{}_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>={} and convert(pct_chg,DECIMAL(5,2))<{},ts_code,null)) up_{}_{}_stock_set,
    """
    for i in range(1, 10):
        print(sql.format(i * 1.0, i * 1.0 + 1, i, i + 1, i * 1.0, i * 1.0 + 1, i, i + 1))


if __name__ == '__main__':
    pass
    create_total_up()

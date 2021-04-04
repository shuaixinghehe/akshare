# ! /usr/bin/env python
# *-* coding:utf-8 *-*

if __name__ == '__main__':
    pass
    feature_map = {}
    feature_map['a'] = 1
    feature_map['b'] = 2
    feature_map['c'] = 0.1
    feature_map['f0_day_before_daily_open'] = 4.6
    feature_map['f1_day_before_daily_close'] = 4.49
    add_result = eval("a+b", feature_map)
    print  add_result
    minus_result = eval("a-b", feature_map)
    print  minus_result
    mul_result = eval("a*b", feature_map)
    print  mul_result
    div_result = eval("a/(b*1.0)", feature_map)
    print  div_result
    min_result = eval("min(a,b,c) <= c", feature_map)
    print  min_result
    min_result = eval("f0_day_before_daily_open > (f1_day_before_daily_close*1.02) and False ", feature_map)
    print  min_result
    print min(1 * 23, 2)

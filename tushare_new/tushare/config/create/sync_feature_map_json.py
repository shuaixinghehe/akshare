# ! /usr/bin/env python
# *-* coding:utf-8 *-*

str = """
{
 "f2_3_open_rate": "f2_day_before_daily_open / (f3_day_before_daily_open+1.0)",
 "f2_4_open_rate": "f2_day_before_daily_open / (f4_day_before_daily_open+1.0)",
 "f2_5_open_rate": "f2_day_before_daily_open / (f5_day_before_daily_open+1.0)",
 "f2_6_open_rate": "f2_day_before_daily_open / (f6_day_before_daily_open+1.0)",
 "f2_7_open_rate": "f2_day_before_daily_open / (f7_day_before_daily_open+1.0)",
 "f2_12_open_rate": "f2_day_before_daily_open / (f12_day_before_daily_open+1.0)",
 "f2_17_open_rate": "f2_day_before_daily_open / (f17_day_before_daily_open+1.0)",
 "f2_3_high_rate": "f2_day_before_daily_high / (f3_day_before_daily_high+1.0)",
 "f2_4_high_rate": "f2_day_before_daily_high / (f4_day_before_daily_high+1.0)",
 "f2_5_high_rate": "f2_day_before_daily_high / (f5_day_before_daily_high+1.0)",
 "f2_6_high_rate": "f2_day_before_daily_high / (f6_day_before_daily_high+1.0)",
 "f2_7_high_rate": "f2_day_before_daily_high / (f7_day_before_daily_high+1.0)",
 "f2_12_high_rate": "f2_day_before_daily_high / (f12_day_before_daily_high+1.0)",
 "f2_17_high_rate": "f2_day_before_daily_high / (f17_day_before_daily_high+1.0)",
 "f2_3_low_rate": "f2_day_before_daily_low / (f3_day_before_daily_low+1.0)",
 "f2_4_low_rate": "f2_day_before_daily_low / (f4_day_before_daily_low+1.0)",
 "f2_5_low_rate": "f2_day_before_daily_low / (f5_day_before_daily_low+1.0)",
 "f2_6_low_rate": "f2_day_before_daily_low / (f6_day_before_daily_low+1.0)",
 "f2_7_low_rate": "f2_day_before_daily_low / (f7_day_before_daily_low+1.0)",
 "f2_12_low_rate": "f2_day_before_daily_low / (f12_day_before_daily_low+1.0)",
 "f2_17_low_rate": "f2_day_before_daily_low / (f17_day_before_daily_low+1.0)",
 "f2_3_close_rate": "f2_day_before_daily_close / (f3_day_before_daily_close+1.0)",
 "f2_4_close_rate": "f2_day_before_daily_close / (f4_day_before_daily_close+1.0)",
 "f2_5_close_rate": "f2_day_before_daily_close / (f5_day_before_daily_close+1.0)",
 "f2_6_close_rate": "f2_day_before_daily_close / (f6_day_before_daily_close+1.0)",
 "f2_7_close_rate": "f2_day_before_daily_close / (f7_day_before_daily_close+1.0)",
 "f2_12_close_rate": "f2_day_before_daily_close / (f12_day_before_daily_close+1.0)",
 "f2_17_close_rate": "f2_day_before_daily_close / (f17_day_before_daily_close+1.0)",
 "f2_3_pre_close_rate": "f2_day_before_daily_pre_close / (f3_day_before_daily_pre_close+1.0)",
 "f2_4_pre_close_rate": "f2_day_before_daily_pre_close / (f4_day_before_daily_pre_close+1.0)",
 "f2_5_pre_close_rate": "f2_day_before_daily_pre_close / (f5_day_before_daily_pre_close+1.0)",
 "f2_6_pre_close_rate": "f2_day_before_daily_pre_close / (f6_day_before_daily_pre_close+1.0)",
 "f2_7_pre_close_rate": "f2_day_before_daily_pre_close / (f7_day_before_daily_pre_close+1.0)",
 "f2_12_pre_close_rate": "f2_day_before_daily_pre_close / (f12_day_before_daily_pre_close+1.0)",
 "f2_17_pre_close_rate": "f2_day_before_daily_pre_close / (f17_day_before_daily_pre_close+1.0)",
 "f2_3_change_rate": "f2_day_before_daily_change / (f3_day_before_daily_change+1.0)",
 "f2_4_change_rate": "f2_day_before_daily_change / (f4_day_before_daily_change+1.0)",
 "f2_5_change_rate": "f2_day_before_daily_change / (f5_day_before_daily_change+1.0)",
 "f2_6_change_rate": "f2_day_before_daily_change / (f6_day_before_daily_change+1.0)",
 "f2_7_change_rate": "f2_day_before_daily_change / (f7_day_before_daily_change+1.0)",
 "f2_12_change_rate": "f2_day_before_daily_change / (f12_day_before_daily_change+1.0)",
 "f2_17_change_rate": "f2_day_before_daily_change / (f17_day_before_daily_change+1.0)",
 "f2_3_pct_chg_rate": "f2_day_before_daily_pct_chg / (f3_day_before_daily_pct_chg+1.0)",
 "f2_4_pct_chg_rate": "f2_day_before_daily_pct_chg / (f4_day_before_daily_pct_chg+1.0)",
 "f2_5_pct_chg_rate": "f2_day_before_daily_pct_chg / (f5_day_before_daily_pct_chg+1.0)",
 "f2_6_pct_chg_rate": "f2_day_before_daily_pct_chg / (f6_day_before_daily_pct_chg+1.0)",
 "f2_7_pct_chg_rate": "f2_day_before_daily_pct_chg / (f7_day_before_daily_pct_chg+1.0)",
 "f2_12_pct_chg_rate": "f2_day_before_daily_pct_chg / (f12_day_before_daily_pct_chg+1.0)",
 "f2_17_pct_chg_rate": "f2_day_before_daily_pct_chg / (f17_day_before_daily_pct_chg+1.0)",
 "f2_3_vol_rate": "f2_day_before_daily_vol / (f3_day_before_daily_vol+1.0)",
 "f2_4_vol_rate": "f2_day_before_daily_vol / (f4_day_before_daily_vol+1.0)",
 "f2_5_vol_rate": "f2_day_before_daily_vol / (f5_day_before_daily_vol+1.0)",
 "f2_6_vol_rate": "f2_day_before_daily_vol / (f6_day_before_daily_vol+1.0)",
 "f2_7_vol_rate": "f2_day_before_daily_vol / (f7_day_before_daily_vol+1.0)",
 "f2_12_vol_rate": "f2_day_before_daily_vol / (f12_day_before_daily_vol+1.0)",
 "f2_17_vol_rate": "f2_day_before_daily_vol / (f17_day_before_daily_vol+1.0)",
 "f2_3_amount_rate": "f2_day_before_daily_amount / (f3_day_before_daily_amount+1.0)",
 "f2_4_amount_rate": "f2_day_before_daily_amount / (f4_day_before_daily_amount+1.0)",
 "f2_5_amount_rate": "f2_day_before_daily_amount / (f5_day_before_daily_amount+1.0)",
 "f2_6_amount_rate": "f2_day_before_daily_amount / (f6_day_before_daily_amount+1.0)",
 "f2_7_amount_rate": "f2_day_before_daily_amount / (f7_day_before_daily_amount+1.0)",
 "f2_12_amount_rate": "f2_day_before_daily_amount / (f12_day_before_daily_amount+1.0)",
 "f2_17_amount_rate": "f2_day_before_daily_amount / (f17_day_before_daily_amount+1.0)",

  "21_22daily_rate_circ_mv": "f21_day_before_basic_circ_mv / ( f22_day_before_basic_circ_mv+1.0 )",
  "4_6daily_rate_pct_chg": "f4_day_before_daily_pct_chg / ( f6_day_before_daily_pct_chg+1.0 )",
  "13_15daily_rate_total_mv": "f13_day_before_basic_total_mv / ( f15_day_before_basic_total_mv+1.0 )",
  "8_10daily_rate_vol": "f8_day_before_daily_vol / ( f10_day_before_daily_vol+1.0 )",
  "7_12daily_rate_circ_mv": "f7_day_before_basic_circ_mv / ( f12_day_before_basic_circ_mv+1.0 )",
  "6_8daily_rate_turnover_rate": "f6_day_before_basic_turnover_rate / ( f8_day_before_basic_turnover_rate+1.0 )",
  "5_10daily_rate_total_share": "f5_day_before_basic_total_share / ( f10_day_before_basic_total_share+1.0 )"
}









"""

if __name__ == '__main__':
    pass
    for line in str.split("\n"):
        if line.find("#") > 0:
            continue

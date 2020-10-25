#!/bin/sh
echo "start" >> /tmp/akshare_start.log
v_time=`date "+%Y_%m_%d"`
run_date=`date "+%Y%m%d"`
cd /Users/beacher/Workspace/custom_virtual_env_space
source ./akshare_env/bin/activate
cd /Users/beacher/Workspace/akshare/src
mode_value=5
for((i=0;i<$mode_value;i++))
do
    python download_stock_daily_data_once.py $mode_value $i $run_date >> /tmp/download_stock_daily_data_once_mode_"$i"_$v_time.log &
    python download_realtime_action_data_once.py $mode_value $i $run_date >> /tmp/download_realtime_action_data_once_mode_"$i"_$v_time.log &
done
cd module
python stock_daily_report_action.py $run_date >> /tmp/stock_daily_report_action_$v_time.log



#cd /Users/beacher/Workspace/custom_virtual_env_space
#source ./tushare_env/bin/activate

#cd /Users/beacher/Workspace/tushare/tushare/module/
#python create_feature_pre.py 0 1  $run_date >> /tmp/create_feature_pre_$v_time.log

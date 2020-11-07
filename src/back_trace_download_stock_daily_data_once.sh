#!/bin/sh
v_time=`date "+%Y_%m_%d"`
cd /Users/beacher/Workspace/custom_virtual_env_space
source ./akshare_env/bin/activate
cd /Users/beacher/Workspace/akshare/src
for((i=1;i<7;i++))
do
    run_date=`date -v -"$i"d +%Y%m%d`
    log_date=`date -v -"$i"d +%Y_%m_%d`
    echo "back_trace_download_stock_daily_data_once  " $run_date
    python download_stock_daily_data_once.py 1 0  $run_date >> /tmp/download_stock_daily_data_once_$log_date.log & 
    if [ i%10 -eq 0 ];then
       sleep 3600
    fi
done

#!/bin/sh
v_time=`date "+%Y_%m_%d"`
cd /Users/beacher/Workspace/custom_virtual_env_space
source ./akshare_env/bin/activate
cd /Users/beacher/Workspace/tushare/tushare/module
run_date=`date -v -"1"d +%Y%m%d`
mod=1
for((i=0;i<$mod;i++))
do
    #run_date=`date -v -"$i"d +%Y%m%d`
    log_date=`date -v -"$i"d +%Y_%m_%d`
    echo "create_feature_pre.py" $run_date
    python create_feature_pre.py $mod $i  $run_date   &
done


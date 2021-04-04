#!/bin/sh
v_time=`date "+%Y_%m_%d"`
cd /Users/beacher/Workspace/custom_virtual_env_space
source ./tushare_env/bin/activate
cd /Users/beacher/Workspace/tushare/tushare/module
for((i=60;i<90;i++))
do
    run_date=`date -v -"$i"d +%Y%m%d`
    log_date=`date -v -"$i"d +%Y_%m_%d`
    echo "back_trace_create_feature_pre" $run_date
    hashmod=5
    for((value=0;value<$hashmod;value++))
    do
        python create_feature_pre_5day.py $hashmod $value $run_date >> /tmp/create_feature_pre_5day_tushare_mod_"$hashmod"_"$value"_"$v_time"_$run_date.log &
    done
done



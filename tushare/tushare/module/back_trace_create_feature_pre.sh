#!/bin/sh
v_time=`date "+%Y_%m_%d"`
cd /Users/beacher/Workspace/custom_virtual_env_space
source ~/Workspace/custom_virtual_env_space/akshare_env/bin/activate
cd /Users/beacher/Workspace/tushare/tushare/module
for((i=0;i<1;i++))
do
    run_date=`date -v -"$i"d +%Y%m%d`
    log_date=`date -v -"$i"d +%Y_%m_%d`
    hashmod=1
    for((value=0;value<$hashmod;value++))
    do
        python create_feature_pre.py $hashmod $value $run_date &
        echo create_feature_pre.py $hashmod $value $run_date
    done
done



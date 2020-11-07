#!/bin/sh
v_time=`date "+%Y_%m_%d"`
cd /Users/beacher/Workspace/custom_virtual_env_space
source ./akshare_env/bin/activate
cd /Users/beacher/Workspace/akshare/src
for((i=1;i<8;i++))
do
    run_date=`date -v -"$i"d +%Y%m%d`
    log_date=`date -v -"$i"d +%Y_%m_%d`
    echo "download_realtime_action_data_once.py  " $run_date
    hashmod=1
    for((value=0;value<$hashmod;value++))
    do
	echo $hashmod $value  $run_date
        python download_realtime_action_data_once.py $hashmod $value  $run_date >> /tmp/download_realtime_action_data_once_$log_date.log & 
    done
done

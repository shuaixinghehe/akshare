#!/bin/sh
echo "start" >> /tmp/akshare_start.log
v_time=`date "+%Y_%m_%d"`
run_date=`date "+%Y%m%d"`

cd /Users/beacher/Workspace/custom_virtual_env_space
source ~/Workspace/custom_virtual_env_space/akshare_env/bin/activate

cd /Users/beacher/Workspace/tushare/tushare/module/
mode_value=1
for((i=0;i<$mode_value;i++))
do
       python create_feature_pre.py $mode_value $i  $run_date >> /tmp/create_feature_pre_mod_"$mode_value"_"$i"_$v_time.log &
done

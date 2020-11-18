#!/bin/sh
v_time=`date "+%Y_%m_%d"`
cd /Users/beacher/Workspace/custom_virtual_env_space
source ./akshare_env/bin/activate
cd /Users/beacher/Workspace/akshare/src
python download_realtime_action_data_once.py 1 0 20201110 &
python download_realtime_action_data_once.py 1 0 20201111 &

#!/bin/sh
v_time=`date "+%Y_%m_%d"`
cd /Users/beacher/Workspace/custom_virtual_env_space
source ./akshare_env/bin/activate
cd /Users/beacher/Workspace/akshare/src
python download_realtime_action_data_once.py 1 0 20200910 &
python download_realtime_action_data_once.py 1 0 20200919 &
python download_realtime_action_data_once.py 1 0 20200920 & 

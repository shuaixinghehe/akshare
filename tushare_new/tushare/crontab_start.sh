#!/bin/sh
v_time=`date "+%Y_%m_%d"`
cd /Users/beacher/Workspace/custom_virtual_env_space
source ./tushare_env/bin/activate
cd /Users/beacher/Workspace/tushare/tushare
python a_download_tushare_data.py >> /tmp/tushare_$v_time.log


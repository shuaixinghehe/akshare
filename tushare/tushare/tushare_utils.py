#! /usr/bin/env python
# *-* coding:utf-8 *-*

import logging

import pymysql

logging.basicConfig(level=logging.INFO,
                    filename='/tmp/realtime_action_download.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("realtime_action")

LOG = logger

monitor_conn = pymysql.connect(host="127.0.0.1", user="diabetes", \
                               password="&QwX0^4#Sm^&t%V6wBnZC%78", \
                               db="monitor", \
                               charset='utf8')

monitor_cur = monitor_conn.cursor()


def LOG_INFO(*params):
    message = ""
    for p in params:
        message += " " + str(p)
    LOG.info(message)


def perf(namespace='', subtag='', extra='', value=1):
    pass
    monitor_cur.execute("""
        insert into  akshare_run_log (namespace,subtag,extra,value) values 
        (%s,%s,%s,%s)
    """, (str(namespace), str(subtag), str(extra), str(value)))
    monitor_conn.commit()


def LOG_ERROR(*params):
    message = ""
    for p in params:
        message += " " + str(p)
    LOG.error(message)


def load_local_json_file(path=''):
    config_str = ""
    ofile = open(path)
    for line in ofile:
        config_str += line
    return config_str


def load_local_json_file_keys_in_order(path=''):
    ofile = open(path)
    feature_key_list = []
    for line in ofile:
        line = line.replace('"', '').replace(" ", '').replace('{', '').replace("}", '')
        line = line.strip()
        if len(line) > 0:
            feature_key = line.split(":")[0]
            feature_key_list.append(feature_key)
    return feature_key_list


if __name__ == '__main__':
    pass
    # print(load_local_json_file_keys_in_order("./config/feature_map.json"))
    perf(namespace='test11', subtag='test22', extra='test33')

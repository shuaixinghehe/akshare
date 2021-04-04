# ! /usr/bin/env python
# *-* coding:utf-8 *-*
import tushare_utils
import json
import math

if __name__ == '__main__':
    pass
    path = "../config/feature_map_test.json"
    config_json = tushare_utils.load_local_json_file(path)
    config_map = json.loads(config_json)
    print config_map
    print config_map.keys()
    feature_map = {}
    feature_map["a"] = 1.0
    feature_map["b"] = 2.0
    feature_map["c"] = 3.0
    print "feature_map start", feature_map
    for key in feature_map.keys():
        print key, feature_map[key]
    try:
        pass
        for key in config_map.keys():
            value = eval(config_map[key], {'__builtins__': {}}, feature_map)
            # print 'key', key, 'value', value, type(value)
            feature_map[key] = value
    except Exception, e:
        print e
    print "feature_map end", feature_map
    # feature_map_copy = {}
    # for key in feature_map.keys():
    #     print key, feature_map[key]
    #     feature_map_copy[key] = feature_map[key]
    #
    # print "feature_map copy end"
    # for key in feature_map_copy.keys():
    #     print  key, feature_map_copy[key]

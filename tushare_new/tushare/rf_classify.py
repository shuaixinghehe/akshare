#! /usr/bin/env python
# *-* coding:utf-8 *-*

import datetime
import os
import pickle
import sys

from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

currentTime = datetime.datetime.today().isoformat()

origin_feature_map = {}

include_feature_map = {}
exclude_feature_map = {}

LABEL_INDEX = 1
FEATURE_INDEX = 2
UID_INDEX = 0
PREDICT_NUM = 10000
POSITIVE_CASE_CNT = 2000

POSITIVE_NEGTIVE_RATE = 80
PREDICT_COUNT = 40000

reload(sys)
sys.setdefaultencoding('utf8')


def read_train_data(train_data_path='', result_file_path='', data_date_suffix=''):
    ifile = open(train_data_path)
    featuresList = []
    targetList = []
    total = 0
    positive_cnt = 0  # 正样本，符合预期
    lineNum = 0
    for line in ifile:
        lineNum += 1
        if lineNum % 10000 == 0:
            print
            "lineNum:", lineNum
        total += 1
        line = line.strip()
        linearr = line.split(',')
        if (linearr[LABEL_INDEX] == 'True'):
            positive_cnt += 1
    #
    print("原始数据： 总共：" + str(total) + " 正样本:" + str(positive_cnt))
    POSITIVE_NEGTIVE_RATE = int((total - positive_cnt) / positive_cnt * 1.0)
    print("正反样例比例：" + str(POSITIVE_NEGTIVE_RATE))
    ifile.close()
    ifile = open(train_data_path, 'r')
    total = 0
    positive_cnt = 0
    evaluate_target_list = []
    evaluate_feature_list = []
    evaluate_key_list = []
    for line in ifile:
        total += 1
        line = line.strip()
        linearr = line.split(',')
        key = linearr[0]
        # 因为负样本较多，对负样本进行采样
        if total % (POSITIVE_NEGTIVE_RATE + 1) != 0 and linearr[LABEL_INDEX] == 'False':
            continue
        if (linearr[LABEL_INDEX] == 'True'):
            positive_cnt += 1

        # 模型离线预估抽取5%的流量
        if abs(hash(line + str(datetime.time.microsecond))) % 100 < 5:
            pass
            evaluate_target_list.append(linearr[LABEL_INDEX])
            evaluate_feature_list.append(linearr[FEATURE_INDEX:])
            evaluate_key_list.append(key)
        else:
            targetList.append(linearr[LABEL_INDEX])
            featuresList.append(linearr[FEATURE_INDEX:])
            #
    print("进行训练：总共：" + str(len(featuresList)) + "正例:", positive_cnt)
    print("测试样本集", len(evaluate_target_list))
    modelPath, importancePath = train(featuresList, targetList, result_file_path, data_date_suffix)
    evaluate(modelPath, evaluate_feature_list, evaluate_target_list, evaluate_key_list, result_file_path)


def checkFeatureIsFloat(linearr=[]):
    a = 0.0;
    try:
        for i in range(len(linearr)):
            a = float(linearr[i])
    except:
        print
        linearr
        return False
    return True


def printBadCase(linearr=[], clf=None):
    """

    :type clf: object
    """
    print
    clf.predict(linearr[2:]), "predict:"
    print
    "label:", linearr[0], " user_id:", linearr[1],

    for i in range(len(feature_title)):
        print
        feature_title[i] + ":" + linearr[i + 2]


def train(features, target, fileIndex, data_date_suffix):
    # 拆分训练集和测试集
    feature_train, feature_test, target_train, target_test = train_test_split(features, target, test_size=0.3,
                                                                              random_state=42)
    clf = RandomForestClassifier(n_estimators=800, criterion='entropy', max_depth=6)
    clf = clf.fit(features, target)
    # 评估模型准确率
    r = clf.score(feature_test, target_test)

    print
    clf.get_params(True)
    print('所有的树:%s' % clf.estimators_)
    estimators = clf.estimators_
    for estimator in estimators:
        print
        estimator.get_params(True)
    print('模型准确率:%.6f' % (r))
    ofile = open(fileIndex + '/' + 'model_accuracy_' + currentTime + '.txt', 'w')
    ofile.write("n_estimators=60 \n")
    ofile.write("max_depth=6\n")
    ofile.write('模型准确率:%.6f' % (r))
    ofile.close()
    s = pickle.dumps(clf)
    # dc = model.__getitem__(0)
    pwd = os.getcwd()
    modelPath = fileIndex + "/train_model.m" + currentTime
    importancePath = fileIndex + "/importances.txt" + currentTime
    # ofile = open("pickle.pkl" + currentTime, "w")
    # ofile.write(s)
    # ofile.close()
    joblib.dump(clf, modelPath)
    importances = clf.feature_importances_
    importancesDic = {}
    feature_title = []
    ofile = open('./train_data/feature_names_' + data_date_suffix + '.txt', 'r')
    for line in ofile:
        line = line.strip()
        linearr = line.split(',')
        for name in linearr:
            feature_title.append(name)
    for i in range(len(importances)):
        if len(importances) != len(feature_title):
            print("len(importances) != len(feature_title) not Same", len(importances), len(feature_title))
            return
        importancesDic[feature_title[i]] = importances[i] * 100

    importanceList = sorted(importancesDic.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    ofile = open(importancePath, 'w')
    for i in range(len(importanceList)):
        # print  str(importances[i] * 100) + "\t\t\t" + feature_title[i]
        ofile.write(str(importanceList[i]) + "\n")
        # evaluate()
    return modelPath, importancePath


def predict_offline(modelPath, testFilePath, fileIndex):
    clf = joblib.load(modelPath)
    ifile = open(testFilePath, 'r')
    featuresList = []
    targetList = []
    key_list = []
    for line in ifile:
        line = line.strip()
        if line.find('NULL') != -1:
            continue
        linearr = line.split(',')
        targetList.append(linearr[LABEL_INDEX])
        featuresList.append(linearr[FEATURE_INDEX:])
        key_list.append(linearr[0])

    ofile = open(fileIndex + '/predict_offline_result.csv' + currentTime, 'w')
    for i in range(0, len(featuresList)):
        print("evaluate", key_list[i])
        result = slove(str(
            clf.predict_proba([featuresList[i]])[0]))
        ofile.write(key_list[i] + "," + str(
            clf.predict([featuresList[i]])) + "," + str(result[1]) + "," + targetList[i] + "\n")
    ofile.close()


def evaluate(model_path, featuresList, targetList, key_list, result_file_path):
    clf = joblib.load(model_path)
    ofile = open(result_file_path + '/evaluate_predict_result.csv' + currentTime, 'w')
    for i in range(0, len(featuresList)):
        print("evaluate", key_list[i])
        result = slove(str(
            clf.predict_proba([featuresList[i]])[0]))
        ofile.write(key_list[i] + "," + str(
            clf.predict([featuresList[i]])) + "," + str(result[1]) + "," + targetList[i] + "\n")
    ofile.close()

    r = clf.score(featuresList, targetList)
    ofile = open(result_file_path + '/' + 'evalute_model_accuracy' + currentTime + '.txt', 'a')
    ofile.write('验证准确率:%.6f' % (r))
    ofile.close()

    print('验证准确率:%.6f' % (r))


def sloveTreeModel(modelPath, fileIndex):
    clf = joblib.load(modelPath)
    print
    type(clf.estimators_)
    i = 0
    for estimator in clf.estimators_:
        print
        estimator.get_params()
        tree.export_graphviz(estimator.tree_, out_file=fileIndex + '/' + currentTime + 'tree' + str(i) + '.dot')
        i = i + 1


def slove(str=""):
    str = str.replace("[", "")
    str = str.replace("]", "")
    return str.split(" ")


def readTitle(fileIndex):
    global feature_title
    print
    "fileIndex", fileIndex
    feature_title = []
    ofile = open(fileIndex + "/features/features.data", "r")
    for line in ofile:
        line = line.strip()
        feature_title.append(line)


if __name__ == '__main__':
    # pass
    data_date_suffix = "20201227"
    # read_train_data('./train_data/train_data_' + data_date_suffix + '.txt', './model/',
    #                 data_date_suffix)
    # evaluate(modelPath, predictFilePath, fileIndex)
    # sloveTreeModel(modelPath, fileIndex)
    # sloveTreeModel('/Users/beacher/Workspace/ml/Register_classifier/Register_classifier_qq/data/train_model.m2017-01-10T21:57:42.358617', '')

    # label  " f2_day_after_daily_high > (f1_day_after_daily_high*1.03)"
    # 使用的4月7号之前的数据
    model_path = '/Users/beacher/Workspace/tushare/model/train_model.m2020-04-12T02:03:04.382888'

    # label  " f2_day_after_daily_high > (f1_day_after_daily_high*1.03)"
    # 使用的4月10号之前的数据
    # model_path = '/Users/beacher/Workspace/tushare/model/train_model.m2020-04-14T22:02:03.665774'
    model_path = '/Users/beacher/Workspace/tushare/model/train_model.m2020-07-08T00:49:28.788645'

    model_path = '/Users/beacher/Workspace/tushare/tushare/model/train_model.m2020-12-27T20:56:25.896599'
    #
    predict_data_path = './train_data/predict_data_' + data_date_suffix + '.txt'
    predict_offline(modelPath=model_path, testFilePath=predict_data_path, fileIndex='./predict_sample/')

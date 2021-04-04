#! /usr/bin/env python
# *-* coding:utf-8 *-*
import numpy as np
import scipy.stats


def test():
    x = [np.random.randint(1, 11) for i in range(10)]
    x = [243024.42, 124005.05, 78755.43, 124045.61, 106349.98, 63541.08, 22588.55, 27236.45, 17781.28, 21773.0]
    print(x)
    print(np.sum(x))
    px = x / (np.sum(x) * 1.0)  # 归一化
    print(px)

    y = [np.random.randint(1, 11) for i in range(10)]
    y = [322899.76, 204213.73, 92289.05, 158607.03, 138239.43, 69804.79, 44781.0, 51655.42, 38020.49, 58497.01]
    print(y)
    print(np.sum(y))
    py = y / (np.sum(y) * 1.0)  # 归一化
    print(py)
    ## scipy计算函数可以处理非归一化情况，因此这里使用# scipy.stats.entropy(x, y)或scipy.stats.entropy(px, py)均可
    KL = scipy.stats.entropy(y, x)
    print(KL)


def test1():
    # 随机生成两个离散型分布
    x = [np.random.randint(1, 11) for i in range(10)]
    print(x)
    sum_x = np.sum(x)
    print(sum_x)
    px = []
    for i in x:
        px.append(i * 1.0 / sum_x)
    print(px)

    y = [np.random.randint(1, 11) for i in range(10)]
    print(y)
    sum_y = np.sum(y)
    print(sum_y)
    py = []
    for i in y:
        py.append(i * 1.0 / sum_y)
    print(py)

    # 利用scipy API进行计算
    # scipy计算函数可以处理非归一化情况，因此这里使用
    # scipy.stats.entropy(x, y)或scipy.stats.entropy(px, py)均可
    KL = scipy.stats.entropy(x, y)
    print(KL)

    # 编程实现
    KL = 0.0
    for i in range(10):
        KL += px[i] * np.log(px[i] / py[i])
        # print(str(px[i]) + ' ' + str(py[i]) + ' ' + str(px[i] * np.log(px[i] / py[i])))

    print(KL)


if __name__ == '__main__':
    pass
    test1()

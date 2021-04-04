"""
=================================================
Plot individual and voting regression predictions
=================================================

.. currentmodule:: sklearn

A voting regressor is an ensemble meta-estimator that fits several base
regressors, each on the whole dataset. Then it averages the individual
predictions to form a final prediction.
We will use three different regressors to predict the data:
:class:`~ensemble.GradientBoostingRegressor`,
:class:`~ensemble.RandomForestRegressor`, and
:class:`~linear_model.LinearRegression`).
Then the above 3 regressors will be used for the
:class:`~ensemble.VotingRegressor`.

Finally, we will plot the predictions made by all models for comparison.

We will work with the diabetes dataset which consists of 10 features
collected from a cohort of diabetes patients. The target is a quantitative
measure of disease progression one year after baseline.

"""
print(__doc__)

import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import numpy as np

if __name__ == '__main__':
    pass
    file_path = '/Users/beacher/Workspace/tushare/tushare/train_data/train_data_20200709.txt'
    ofile = open(file_path, 'r')
    X = []
    Y = []
    read_line_num = 0
    for line in ofile:
        # print(line)
        read_line_num += 1
        arr = line.split(',')
        name = arr[0]
        y_value = float(arr[1])
        x_value = []
        for i in arr[2:]:
            x_value.append(i)
        Y.append(y_value)
        X.append(x_value)
        if read_line_num > 1000:
            break
    X = np.array(X)
    Y = np.array(Y)
    X = X.astype(np.float64)
    Y = Y.astype(np.float64)
    # Train classifiers
    reg1 = GradientBoostingRegressor(random_state=1)
    reg2 = RandomForestRegressor(random_state=1)
    reg3 = LinearRegression()

    reg1.fit(X[:900], Y[:900])
    reg2.fit(X[:900], Y[:900])
    reg3.fit(X[:900], Y[:900])

    xt = X[900:]
    predict_x = X[900:]
    predict_y = Y[900:]

    pred1 = reg1.predict(predict_x)
    pred2 = reg2.predict(predict_x)
    pred3 = reg3.predict(predict_x)
    # pred4 = ereg.predict(xt)

    print("reg1 sore", reg1.score(predict_x, predict_y))
    print("reg2 sore", reg2.score(predict_x, predict_y))
    print("reg3 sore", reg3.score(predict_x, predict_y))
    print("pred1", pred1)
    print("pred2", pred2)
    print("pred3", pred3)
    print("origin", predict_y)
    # print("reg3 sore", reg3.score(X[:100], Y[:100]))
    # print("ereg sore", ereg.score(X[:100], Y[:100]))

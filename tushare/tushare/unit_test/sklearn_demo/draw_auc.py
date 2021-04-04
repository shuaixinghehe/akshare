from sklearn import datasets, svm, metrics, model_selection, preprocessing

iris = datasets.load_iris()
x = iris.data[iris.target != 0, :2]
x = preprocessing.StandardScaler().fit_transform(x)
y = iris.target[iris.target != 0]
x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y,
                                                                    test_size=0.1, random_state=25)
clf = svm.SVC(kernel='linear')
clf.fit(x_train, y_train)
metrics.f1_score(y_test, clf.predict(x_test))
0.75
fpr, tpr, thresholds = metrics.roc_curve(y_test, clf.decision_function(x_test),
                                         pos_label=2)
print(metrics.auc(fpr, tpr))

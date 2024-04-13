# Naive Bayes classifier
# Iris Naive Bayes Three Classifier python program
# Filename: Naive_Bayes.ipynb
import numpy as np
import sklearn.metrics
from sklearn import naive_bayes
from sklearn import datasets
np.random.seed(1000)
iris = datasets.load_iris()
iris_x = iris.data
iris_y = iris.target
indices = np.random.permutation(len(iris_x))

# Ramdomly fetch 140 samples
iris_x_train = iris_x[indices[:-10]]
iris_y_train = iris_y[indices[:-10]]

# 10 leftover as test set
iris_x_test = iris_x[indices[-10:]]
iris_y_test = iris_y[indices[-10:]]

# define naive_bayes_cly
naive_bayes_clf = naive_bayes.GaussianNB()
# Training
naive_bayes_clf.fit(iris_x_train, iris_y_train)
# Testing
iris_y_pred = naive_bayes_clf.predict(iris_x_test)
print("测试数据集的正确标签为：", iris_y_test)
print("测试数据集的预测标签为：", iris_y_pred)
testing_acc = sklearn.metrics.accuracy_score(iris_y_test, iris_y_pred)*100
print("朴素bayes分类器测试准确率为:{:.2f}%".format(testing_acc))
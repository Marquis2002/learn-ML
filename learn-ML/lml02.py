# KNN example
import numpy as np
import sklearn as sk
from sklearn.neighbors import KNeighborsClassifier
# Assumed that you have X(predictor) and Y(target) for training data set,
# x_test(predictor) of test_dataset, y_test(target) for testing data set.
X = np.array([[1.14,1.78], [1.18,1.96], [1.20,1.86], [1.26,2.00], [1.30,2.00], [1.28,1.96],[1.24,1.72],[1.36,1.74],
              [1.38,1.64],[1.38,1.82],[1.38,1.90],[1.40,1.70],[1.48,1.82],[1.54,2.08],[1.56,1.78]])
y = np.array([0,0,0,0,0,0,1,1,1,1,1,1,1,1,1])
# (X, y) is the training set, the six at the beginning is APf while the other 9 are Af
x_test = np.array([[1.24, 1.8],[1.28, 1.84],[1.4, 2.04]] )
y_test = np.array([0,0,0])

# Create KNeighbors classifier object model
knn = KNeighborsClassifier(n_neighbors=3)
# Experiment Arguments: k value is up to the experiment's need
# default value for n_neighbors is 5
# Train the model using the trainning data sets and check score
knn.fit(X, y)
# Predict Output
y_pred = knn.predict(X)
training_acc = 100-np.mean(np.abs(y_pred-y))*100
print("KNN classifier's trainning accuracy is: {:.2f}%".format(training_acc))
# Predict Output
y_pred = knn.predict(x_test)
print("KNN classifying results is: ", y_pred)
# Print Accuracy
from sklearn.metrics import accuracy_score
testing_acc = accuracy_score(y_test,y_pred)*100
print("KNN classifier's testing accuracy is: {:.2f}%".format(training_acc))


from sklearn.svm import SVC
import numpy as np


def svm(features, target):
	clf = SVC(kernel = "poly", degree = 2)
	clf.fit(features, target)
	return clf

features = np.array([[2,3]])
target = np.array([0])

clf = SVC(kernel = "poly", degree = 2)
clf.fit(features, target)
features = np.array([[3,4]])
target = np.array([1])
clf.fit(features,target)
print clf.predict([[3,4]])
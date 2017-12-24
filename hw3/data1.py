from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
import numpy as np
import csv

class Dataset(object):
    def _init_(self):
        self.data = None
        self.target = None
    def __init__(self, data):
        self.data = []
        self.target = []
        for row in data:
            self.data.append(row[:-1])
            self.target.append(row[-1])
 
def Value(data):
    new_data = []
    for row in data:
        new_row = []
        for x in row:
            try:
                new_row.append(float(x))
            except ValueError:
                new_row.append(x)
        new_data.append(new_row)
    return new_data 
       

file1 = open('data/iris.data','r')
data = list(csv.reader(file1))
file1.close()

#data = preprocessing.normalize(Value(data[:-1]))
iris = Dataset(data[:-1]) 
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size = 0.3)


X_train = preprocessing.normalize(Value(X_train))
X_test = preprocessing.normalize(Value(X_test))
#X_train = np.array(X_train).astype(np.float)
#X_test = np.array(X_test).astype(np.float)

#decision tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train,y_train)

result = clf.predict(X_test)
accuracy = accuracy_score(y_test, result)
print ("decision tree:  %f"%(accuracy))

#knn
neigh = KNeighborsClassifier(n_neighbors=3)
neigh = neigh.fit(X_train,y_train)

result = neigh.predict(X_test)
accuracy = accuracy_score(y_test, result)
print ("knn          :  %f"%(accuracy))

#naive bayes
gnb = GaussianNB()
gnb = gnb.fit(np.array(X_train).astype(np.float),y_train)


result = gnb.predict(X_test)
accuracy = accuracy_score(y_test, result)
print ("naive bayes  :  %f"%(accuracy))

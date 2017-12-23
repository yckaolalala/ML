from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import numpy as np
import csv
import sklearn.metrics as skm

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

def Split(data):
    continuous = []
    category = []
    for row in data:
        con_row = []
        cat_row = []
        for x in row:
            if type(x) in (int, float):
                con_row.append(x)
            else:
                cat_row.append(x)
        continuous.append(con_row)
        category.append(cat_row)
    return continuous, category 

def Convert(data):
    for i in range(len(data[0])):
        if type(data[0][i]) == str:
            category = 0
            label = {}
            for j in range(len(data)):
                if data[j][i] not in label.keys():
                    label[data[j][i]] = category
                    data[j][i] = float(category)
                    category += 1
                else:
                    data[j][i] = float(label[data[j][i]])
    return data
file1 = open('data/forestfires.csv','r')
#file1 = open('data/iris.data','r')
data = list(csv.reader(file1))
file1.close()

"""
#naive bayes
data = Value(data[1:-1])
iris = Dataset(data)
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size = 0.3)
con, cat = Split(X_train)
#gnb = GaussianNB()
#gnb = gnb.fit(con, y_train)
#result = gnb.predict(X_test)

mnb = MultinomialNB()
mnb = mnb.fit(cat, y_train)

#result = gnb.predict(X_test)
#accuracy = accuracy_score(y_test, result)


"""
data = Value(data[1:-1])
test = Convert(data)
iris = Dataset(test)
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size = 0.3)
clf = tree.DecisionTreeRegressor()
clf = clf.fit(X_train, y_train)

result = clf.predict(X_test)
mae = mean_absolute_error(result, y_test)
mse = mean_square_error(result, y_test)
r2 = r2_score(result, y_test)

print (r2)
#accuracy = accuracy_score(y_test, result)
#print (accuracy)

#knn
neigh = KNeighborsRegressor(n_neighbors=3)
neigh = neigh.fit(X_train,y_train)

result = neigh.predict(X_test)
r2 = r2_score(result, y_test)
print (r2)

#print (result)
#accuracy = accuracy_score(y_test, result)
#print (accuracy)


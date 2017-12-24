from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import r2_score
from sklearn import preprocessing
from sklearn import linear_model
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

def Mse(pred, ans):
    mse = 0
    for i in range(len(pred)):
        mse += (pred[i]-ans[i])*(pred[i]-ans[i]) 
    return mse/len(pred)

def Mae(pred, ans):
    mae = 0
    for i in range(len(pred)):
        mae += abs(pred[i]-ans[i]) 
    return mae/len(pred)


file1 = open('data/forestfires.csv','r')
#file1 = open('data/iris.data','r')
data = list(csv.reader(file1))
file1.close()

data = Value(data[1:-1])
"""
forest = Dataset(data)
X_train, X_test, y_train, y_test = train_test_split(forest.data, forest.target, test_size = 0.3)
con, cat = Split(X_train)
#gnb = GaussianNB()
#gnb = gnb.fit(con, y_train)
#result = gnb.predict(X_test)

mnb = MultinomialNB()
mnb = mnb.fit(cat, y_train)

#result = gnb.predict(X_test)
#accuracy = accuracy_score(y_test, result)


"""

test = Convert(data)
test = preprocessing.normalize(test)
forest = Dataset(test)
X_train, X_test, y_train, y_test = train_test_split(forest.data, forest.target, test_size = 0.3)

clf = tree.DecisionTreeRegressor()
clf = clf.fit(X_train, y_train)

result = clf.predict(X_test)
mae = Mae(result, y_test)
mse = Mse(result, y_test)
r2 = r2_score(result, y_test)

print ("decision tree:  %f  %f  %f"%(mse, mae, r2))


#knn
neigh = KNeighborsRegressor(n_neighbors=3)
neigh = neigh.fit(X_train,y_train)

result = neigh.predict(X_test)

mae = Mae(result, y_test)
mse = Mse(result, y_test)
r2 = r2_score(result, y_test)

print ("knn          :  %f  %f  %f"%(mse, mae, r2))

#naive bayes
reg = linear_model.BayesianRidge()
reg = reg.fit(X_train, y_train)
result = reg.predict(X_test)

mae = Mae(result, y_test)
mse = Mse(result, y_test)
r2 = r2_score(result, y_test)
print ("naive bayes  :  %f  %f  %f"%(mse, mae, r2))

from sklearn.model_selection import train_test_split
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
    new = []
    for row in new_data:
        new_row = []
        for x in range(len(row)):
            if x != 11:
                new_row.append(row[x])
        new.append(new_row)
    #return new_data 
    return new

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

def AttrClassCount(data):
    label = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0}
    for x in data:
        label[x] += 1
    return label

def Nbayes(X, y, feature):
    target_count = AttrClassCount(y) 
    #print (sum(target_count.values()))
    cond_count = [] 
    cond_proba = [] 
    laplace_n = [] 
    #target_ = {'a':{}, 'b':{}, 'c':{}, 'd':{}, 'e':{}, 'f':{}}
    target = {}
    for x in feature[-1]:
        target[x] = {}
    for i in range(len(X[0])):
        cond_count.append(target)
        cond_proba.append(target)

    #laplace smooth  
    for index in range(len(X[0])):
        for key in target.keys():
            for row in feature[index]:
                cond_count[index][key][row] = 1
        laplace_n.append(len(feature[index]))

    for row in range(len(y)):
        for index in range(len(X[0])):
            cond_count[index][y[row]][X[row][0]] += 1

    #cal proba each featue 
    for index in range(len(X[0])): # 0, 1
        for feat in feature[index]: # jun to dec , mon to sun
            for key in target.keys(): # a to f
                proba = float(cond_count[index][key][feat] / (target_count[key] + laplace_n[index]))
                cond_proba[index][key][feat] = proba

    return cond_proba, target_count

def norm_pdf(x, mu, sigma):
    pdf = np.exp(-((x - mu)**2) / (2 * sigma**2)) / (sigma * np.sqrt(2*np.pi))
    return pdf
def lgl(mean, variace, x):
        return -0.5*np.log(2 * np.pi * variace) + -((x-mean) ** 2)/(2*variace)

def Nbayes_con(X, y, feature):
    target_count = AttrClassCount(y) 
    nb = []
    for index in range(len(X[0])):
        pdf = {}
        for x in feature[-1]:
            pdf[x] = {'mean':0, 'std':0}
        
        subdata = []
        for x in feature[-1]:
            for row in range(len(y)):
                if y[row] == x:
                    subdata.append(X[row][index])
            data = np.array(subdata)
            pdf[x]['mean']= data.mean() 
            pdf[x]['std']= data.std() 
        nb.append(pdf)
    return nb

def Predict_prob(nb_cat, nb_con, tar, feature, cat, con):
    result = []
    for row in range(len(cat)):
        #target = {'a':{}, 'b':{}, 'c':{}, 'd':{}, 'e':{}, 'f':{}}
        target = {}
        for x in feature[-1]:
            target[x] = {}

        total = 0
        for key in target.keys():
            accum = 1
            for index in range(len(cat[0])):
                accum *= nb_cat[index][key][cat[row][index]] * ( int(tar[key]) / sum(tar.values()))
            for index in range(len(con[0])):
                pdf = norm_pdf(con[row][index], nb_con[index][key]['mean'], nb_con[index][key]['std'])
                #lg = lgl(con[row][index], nb_con[index][key]['mean'], nb_con[index][key]['std'])
                accum *= pdf

            target[key] = accum
            total += accum
        for key in target.keys():
            target[key] = target[key] / total
        result.append(target)
    return result

def Predict_accuracy(nb_cat, nb_con, tar, feature, cat, con, y):
    proba = Predict_prob(nb_cat, nb_con, tar, feature, cat, con)
    true = 0
    total = 0
    for index in range(len(proba)):
        result = max(proba[index], key=proba[index].get)
        if result == y[index]:
            true += 1
        total +=1
    return float(true/total)

def Feature(data):
    allcon, allcat = Split(data)
    feature = []
    for index in range(len(allcat[0])):
        count = set()
        for row in allcat:
            if row[index] not in count:
                count.add(row[index])
        feature.append(count)
    return feature

file1 = open('data/forestfires.csv','r')
data = list(csv.reader(file1))
file1.close()


data = Value(data[1:-1])
for row in data:
    target = float(row[-1]) 
    if target == 0:
        row[-1] = 'a'
    elif target <= 1:
        row[-1] = 'b'
    elif target <= 10:
        row[-1] = 'c'
    elif target <= 100:
        row[-1] = 'd'
    elif target <= 1000:
        row[-1] = 'e'
    else:
        row[-1] = 'f'

forest = Dataset(data)
X_train, X_test, y_train, y_test = train_test_split(forest.data, forest.target, test_size = 0.3)
con, cat = Split(X_train)
con_, cat_ = Split(X_test)


feature = Feature(data)
nb_cat, target = Nbayes(cat, y_train, feature)
nb_con = Nbayes_con(con, y_train, feature)

accuracy = Predict_accuracy(nb_cat, nb_con, target, feature, cat_, con_, y_test)

print (accuracy)

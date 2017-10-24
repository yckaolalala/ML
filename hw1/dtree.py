from math import log
import operator
import random

#each class number of attribute
def AttrClassCount(data, index):
    types  = {}
    for row in data:
        key = row[index]
        if key not in types.keys():
            types[key] = 0
        types[key] += 1
    return types 

def Entropy(data):
    entries = len(data)
    types = AttrClassCount(data, -1)
    sigma = 0.0 
    for key in types:
        p = float(types[key])/entries
        sigma -= p*log(p,2)
    return sigma

def InfoGain(data, index):
    n = len(data)
    boundary = 0
    entropy = Entropy(data)
    sort = sorted(data, key=operator.itemgetter(index)) 
    #continuous variable
    if type(data[0][index]) in (float, int):
        rem = {}
        bound , min_rem =  0, 0 
        for i in range(n-1):
            if sort[i][-1] != sort[i+1][-1]:
                bound = (sort[i][index]+sort[i+1][index])/2
                rem[bound] = Entropy(sort[0:i+1])*(i+1)/n + Entropy(sort[i+1:n])*(n-i-1)/n
        (boundary, min_rem) = min(rem.items(), key=lambda x: x[1])
        infogain = entropy - min_rem
    #discrete variable
    else:
        types  = AttrClassCount(data, index)
        rem = 0.0
        for key in types:
            subset = [row for row in data if row[index] == key]
            rem += Entropy(subset)*float(types[key])/n
        infogain = entropy - rem
    return infogain, boundary

def BestFeature(data, attrs):
    entropy = Entropy(data) 
    target, infogain, boundry = -1, 0.0, 0.0
    for i in attrs:
        info, bound = InfoGain(data,i)
        if info >= infogain:
            info, target, boundry = infogain, i, bound
    return target, boundry

def DecisionTree(data, pre_classlist = None, attrs = None):
    if attrs == None:
        attrs = set()
        for i in range(len(data[0])-1):
            attrs.add(i)
    classlist = [ex[-1] for ex in data]
    # majority of parent
    if len(data) == 0:
        return max(pre_classlist)
    # single label
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    # only label
    if len(attrs) == 0: 
        return max(classlist)

    (target, boundry) = BestFeature(data, attrs)
    theTree = {target:{}}
    # continuous variable
    if boundry != 0:
        subset1 = [row for row in data if row[target] < boundry]
        subset2 = [row for row in data if row[target] >= boundry]
        del data
        if len(subset1) == 0 or len(subset2) == 0 :
            attrs = attrs-{target}
        theTree[target]["- "+str(boundry)] = DecisionTree(subset1, classlist, attrs)
        theTree[target]["+ "+str(boundry)] = DecisionTree(subset2, classlist, attrs)
    # discrete variable
    else:
        types = AttrClassCount(data, target)
        for key in types:
            subset = [row for row in data if row[target] == key]
            theTree[target][key] = DecisionTree(subset, classlist, attrs-{target})
    return theTree

def RandomForest(data, features, num):
    attrs = set()
    for i in range(len(data[0])-1):
        attrs.add(i)
    group = [[]]
    feature = []
    forest = []
    for number in attrs:        
        group += [[number] + element for element in group]
    for subset in group:
        if len(subset) == features:
            feature.append(subset)
    for i in range(num):
        train = []
        for j in range(len(data)):
            index = random.randint(0, len(data)-1)
            train.append(data[index])
        tree = DecisionTree(train, attrs = set(feature[i%len(feature)]))
        forest.append(tree)
    return forest

def Predict_dt(tree, row):
    if type(tree) == str:
        return tree
    for index in tree:
        for key in tree[index]:
            value = key.split(' ')
            if value[0] == '+' or value[0] == '-':
                if row[index] >= float(value[1]):
                    return Predict_dt(tree[index]["+ "+value[1]],row)
                else:
                    return Predict_dt(tree[index]["- "+value[1]],row)
            else:
                 if row[index] == key:
                    return Predict_dt(tree[index][key],row)
        return Predict(tree[index][key],row)

def Predict_rf(forest, row):
    result = {}
    for tree in forest:
        predict = Predict_dt(tree, row)
        if predict not in result.keys():
            result[predict] = 0
        result[predict] += 1
    return max(result, key = result.get)

def Predict(tree, row, model):
    if model == 'rf':
        return Predict_rf(tree, row)
    elif model == 'dt':
        return Predict_dt(tree, row)
    

def Score(tree, labels, test, model = None):
    tp = {}
    fn = {}
    fp = {}
    target = []
    for row in test:
        if row[-1] not in target:
            target.append(row[-1])
    for key in labels:
        tp[key], fn[key], fp[key] = 0, 0, 0
    for row in test:
        predict = Predict(tree, row, model)
        if row[-1] == predict:
            tp[predict] += 1
        else:
            fn[row[-1]] += 1
            fp[predict] += 1
    precision = {}
    recall = {}
    accuracy = float(sum(tp.values())) / len(test)
    for index in target:
        precision[index] = 1 if fp[index] == 0 else float(tp[index]) / (tp[index] + fp[index])
        recall[index] = 1 if fn[index] == 0 else float(tp[index]) / (tp[index] + fn[index])
    return accuracy, precision , recall

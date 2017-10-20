import pprocess as pp
import dtree as dt
import json

#sample = pp.Load("./sample.data")
data = pp.Load("./iris.data")
labels = []
for row in data:
    if row[-1] not in labels:
        labels.append(row[-1])
k = 5
kfold = pp.Kfold(data, k)
score = {'accuracy': 0.0, 'recall': {'Iris-setosa': 0.0, 'Iris-virginica': 0.0, 'Iris-versicolor': 0.0}, 'precision': {'Iris-setosa': 0.0, 'Iris-virginica': 0.0, 'Iris-versicolor': 0.0}}

for test in kfold:
    train = []
    for j in kfold:
        if test != j:
            train.extend(j)
    tree = dt.DecisionTree(train)
    accuracy, precision, recall = dt.Score(tree, labels, test)
 #   print(precision, recall )
    
    score['accuracy'] += accuracy
    for key in labels:
        score['precision'][key] += precision[key]    
        score['recall'][key] += recall[key]  
  
#print (score)
print ("%f"%(score['accuracy']/k)) 
for key in labels:
    print("%s %f %f"%(key, score['precision'][key]/k, score['recall'][key]/k))   

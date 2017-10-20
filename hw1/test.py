import pprocess as pp
import dtree as dt
import json

#data = pp.Load("./sample.data")
data = pp.Load("./iris.data")

k = 5
data = pp.Normalize(data)
kfold = pp.Kfold(data, k)
score = {'accuracy':0.0, 'recall':{}, 'precision':{}}
labels = []
for row in data:
    if row[-1] not in labels:
        labels.append(row[-1])

for key in labels:
    score['precision'][key] = 0.0    
    score['recall'][key] = 0.0  

for i in range(k):
    test = kfold[i]
    train = []
    for j in range(k):
        if i != j:
            train.extend(kfold[j])
    tree = dt.DecisionTree(train)
    accuracy, precision, recall = dt.Score(tree, labels, test)
    
    score['accuracy'] += accuracy
    for key in precision:
        score['precision'][key] += precision[key]    
        score['recall'][key] += recall[key]  
  
rank = 0.0
print ("%f"%(score['accuracy']/k)) 
for key in labels:
    print("%s %f %f"%(key, score['precision'][key]/k, score['recall'][key]/k))
    rank += score['precision'][key]/k + score['recall'][key]/k
print (rank + score['accuracy']/k)

   

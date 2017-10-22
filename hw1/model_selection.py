import dtree as dt
import random

def Kfold(data, k):
      n = len(data)
      size = n//k
      random.shuffle(data)
      subdata = []
      for i in range(k-1):
          subdata.append(data[i*size:(i+1)*size])
      subdata.append(data[(i+1)*size:n])
      return subdata

def Cross_val_score(data, model, k):
    kfold = Kfold(data, k)
    score = {'accuracy':0.0, 'recall':{}, 'precision':{}}
    count = {}
    labels = []
    for row in data:
        if row[-1] not in labels:
            labels.append(row[-1])
            score['precision'][row[-1]] = 0.0    
            score['recall'][row[-1]] = 0.0  
            count[row[-1]] = 0

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
            count[key] += 1

    score['accuracy'] = float(score['accuracy']) / k
    for key in labels:
        score['precision'][key] = float(score['precision'][key]) / count[key]
        score['recall'][key] = float(score['recall'][key]) / count[key]
    
    return score

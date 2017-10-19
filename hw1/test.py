import pprocess as pp
import dtree as dt
import json

#sample = pp.Load("./sample.data")
sample = pp.Load("./iris.data")
tree = dt.DecisionTree(sample)

for i in sample:
    print (i, dt.Predict(tree, i))
    wait = input("pause")

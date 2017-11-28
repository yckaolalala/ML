import kdtree as kd
import random
import csv


def sort_dis(kmin, row):
    for i in range(len(kmin)):
        for j in range(i,len(kmin)):
            if kd.Distance(kmin[i],row) > kd.Distance(kmin[j], row):
                tmp = kmin[i]
                kmin[i] = kmin[j]
                kmin[j] = tmp 

def predict(kmin, k):
    attribute = {}
    for i in range(k):
        key = kmin[i][-1]            
        if key not in attribute.keys():
            attribute[key] = 0
        attribute[key] += 1

    return max(attribute, key = attribute.get)

file1 = open('train1.csv','r')
file2 = open('test1.csv','r')
train = list(csv.reader(file1))
test = list(csv.reader(file2))
file1.close()
file2.close()

klist = [1, 5, 10 ,100]
for k in klist:
    correct = 0
    for i in range(len(test)):
        tree = kd.Build_kdtree(train)
        kmin = []
        kd.Knn(tree,test[i],k,kmin)
        result = predict(kmin, k)
        if result == test[i][-1]:
            correct += 1
    print ("KNN accuracy: %f"%(correct/len(test))) 
    for i in range(3):
        tree = kd.Build_kdtree(train)
        kmin = []
        kd.Knn(tree,test[i],k,kmin)
        sort_dis(kmin, test[i])
        output = ""
        for j in range(k):
            output += str(kmin[j][0]) + " "
        print (output)
    print ()

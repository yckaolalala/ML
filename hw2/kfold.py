import random
import csv

def Kfold(data, k):
    n = len(data)
    size = n//k
    random.shuffle(data)
    subdata = [] 
    for i in range(k-1):
        subdata.append(data[i*size:(i+1)*size])
    subdata.append(data[(i+1)*size:n])
    return subdata
 

file0 = open('train.csv','r')
data = list(csv.reader(file0))


subdata = Kfold(data, 5)
train = []
test = subdata[4]
for i in range(4):
    train.extend(subdata[i])

file1 = open('train1.csv','w')
writer = csv.writer(file1)
writer.writerows(train)
file2 = open('test1.csv','w')
writer = csv.writer(file2)
writer.writerows(test)


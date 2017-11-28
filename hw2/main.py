import kdtree as kd
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

"""
file1 = open('train.csv','r')
data = list(csv.reader(file1))[1:]

subdata = Kfold(data,5)
train = []
for i in range(4):
    train.extend(subdata[i])
test = subdata[4]

f = open("train1.csv","w")
w = csv.writer(f)
w.writerows(train)
f.close()
f = open("test1.csv","w")
w = csv.writer(f)
w.writerows(test)
f.close()

"""
file = open('train.csv','r')
data0 = list(csv.reader(file))

file1 = open('train1.csv','r')
file2 = open('test1.csv','r')
train = list(csv.reader(file2))
test = list(csv.reader(file1))

for k in range(15):
#kd.Best_attribute(data)
    tree = kd.Build_kdtree(train)
    result = kd.Nearest(tree,test[k])
#result = kd.Find_nearest(tree, test[2])
    if result != None:
        print (result.data, kd.Distance(result.data, test[k]))
"""
for k in range(15):
#    print (result.data,kd.Distance(result.data,test[k]))
    minn = 99999999
    data = []
    for row in train:
        dis = kd.Distance(row,test[k])
        if dis < minn:
            minn = dis
            data = row
    print ("ans ", data,minn)
    #print (test[0])

for row in data0:
    if row[0] == '109':
        print (row,kd.Distance(row,test[0]))
"""

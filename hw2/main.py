import kdtree as kd
import csv

file = open('test1.csv','r')
file2 = open('test2.csv','r')
#file = open('train.csv','r')
data = list(csv.reader(file))[1:]
data2 = list(csv.reader(file2))[1:]

#kd.Best_attribute(data)
tree = kd.Build_kdtree(data)
kd.Nearest(tree,data2[0])

file.close()


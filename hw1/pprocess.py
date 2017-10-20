import random

def Value(line):
    row = []
    for x in line:
        try:
            row.append(float(x))
        except ValueError:
            row.append(x)
    return row

def Load(filename):
    with open(filename,'r') as load_file:
        data = load_file.read().split('\n')        
    
    result = []
    for line in data:
        row = Value(line.split(','))
        result.append(row)

    return result[:-1]

def Kfold(data, k):
    n = len(data)
    size = n//k
    index = [i for i in range(n)]
    random.shuffle(data)
    subdata = []
    for i in range(k):
        subdata.append(data[i*size:(i+1)*size])
    return subdata
        
        

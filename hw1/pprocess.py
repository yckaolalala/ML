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

def Normalize(data):
    for index in range(len(data[0])-1):
        if type(data[0][index]) in (int, float): 
            col = [x[index] for x in data]
            maximal = max(col)
            minimal = min(col)
            for row in range(len(data)):
                data[row][index] = (data[row][index] - minimal)/(maximal - minimal)
            
    return data
        

def Kfold(data, k):
    n = len(data)
    size = n//k
    index = [i for i in range(n)]
    random.shuffle(data)
    subdata = []
    for i in range(k-1):
        subdata.append(data[i*size:(i+1)*size])
    subdata.append(data[(i+1)*size:n])
    return subdata
        
        

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
    
#    classification = { 'Iris-setosa':'0', 'Iris-versicolor':'1', 'Iris-virginica':'2' }
    result = []
    for line in data:
        row = Value(line.split(','))
 #       for i,j in classification.items():
 #           row[-1] = row[-1].replace(i, j)
        result.append(row)

    return result[:-1]

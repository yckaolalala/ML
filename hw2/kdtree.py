import operator

class Node(object):
    def _init_(self):
        self.parent = None
        self.left = None
        self.right = None
        self.split = None
        self.data = None

def Variance(data, index):
    tmp1 = 0
    tmp2 = 0
    n = len(data)
    for row in data:
        tmp1 += float(row[index])*float(row[index])
        tmp2 += float(row[index])
        
    return float(tmp1/n-(tmp2/n)*(tmp2/n))

def Best_attribute(data):
    best, attribute = 0, 0 
    for index in range(2,len(data[0])-1):# fixed in this assignment data
        var = Variance(data,index)
        if var > best:
            best, attribute = var, index
    return attribute

def Get_middle(data, attribute):
    n = len(data)
    sort = sorted(data, key=operator.itemgetter(attribute))
    middle = (n+1)/2 if n % 2 == 1 else n/2
    return sort[int(middle)-1]

def Build_kdtree(data):
    
    if len(data) == 0:
        return None
    elif len(data) == 1:
        node = Node()
        node.data = data[0]
        node.split = -1
        return node
    else:
        node = Node()
        attribute = Best_attribute(data)
        middle = Get_middle(data, attribute)
        node.data = middle
        node.split = attribute
        subdata1 = []
        subdata2 = []
        for row in data:
            if row != middle:
                if row[attribute] < middle[attribute]:
                    subdata1.append(row)
                else:
                    subdata2.append(row)

        node.left = Build_kdtree(subdata1)
        node.right = Build_kdtree(subdata2)
        if node.left != None:
            node.left.parent = node            
        if node.right != None:
            node.right.parent = node            

    return node

def Search(cur, pre, row):
    if cur == None:
        return pre
    
    #if cur.left is None and cur.right is None: 
    if cur.split == -1:
        return cur

    print (cur.data)
    print (cur.split)
       
    if cur.data[cur.split] < row[cur.split]:
        print ("left")
        if cur.left != None:
            return Search(cur.left, cur, row)
    else:
        print ("right")
        if cur.right != None:
            return Search(cur.right, cur, row)
    
def Nearest(root, row, minDis = 0):
    print(Search(root, root, row))
    return None

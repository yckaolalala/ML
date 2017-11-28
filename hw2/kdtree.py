import operator

class Node(object):
    def _init_(self):
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

def get_next_attribute(attribute):
    if attribute == 9:
        return 1
    else:
        return int(attribute) + 1

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
    return node

def Distance(p, q):
    count = 0
    for index in range(2,len(p)-1):# fixed in this assignment data
        dis= float(p[index])-float(q[index])
        count += dis*dis
    return count**0.5

def Nearest(root, row):
    if root == None:
        return
    trace = []
    cur = root
    while cur != None and cur.split != -1:
        if cur.data[cur.split] < row[cur.split]:
            if cur.left != None:
                trace.append([cur,'l'])
                cur = cur.left
            else:
                trace.append([cur,'r'])
                cur = cur.right
        else:
            if cur.right != None:
                trace.append([cur,'r'])
                cur = cur.right
            else:
                trace.append([cur,'l'])
                cur = cur.left

    minDis = Distance(row, cur.data)
    for i  in trace:
        if abs(float(row[i[0].split]) - float(i[0].data[i[0].split])) < minDis:
            if Distance(row, i[0].data) < minDis:
                minDis = Distance(row, i[0].data)
                cur = i[0]

            tmp = i[0]
            if i[1] == 'l':
                if i[0].right != None:
                    tmp = Nearest(i[0].right, row)
            else:
                if i[0].left != None:
                    tmp = Nearest(i[0].left, row)
            if Distance(row, tmp.data) < minDis:
                minDis = Distance(row, tmp.data)
                cur = tmp

    return cur



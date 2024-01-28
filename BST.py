class BST:
    def __init__(self, key, idx, parent = None, left = None, right = None):
        self.left   = left
        self.right  = right 
        self.parent = parent
        self.key    = key
        self.idx    = idx  
        # self.data = data 

# end class

def computeValue(pointA, pointB, x):
    #
    ax, ay = pointA
    bx, by = pointB 

    slope = (by - ay) / (bx - ax) 
    intercept = ay - ax * slope 
    return slope * x + intercept 
# end procedure computeValue()


# Operacje na drzewie BST:
# search, insert, remove, min / max, parent, poprzednik-nastepnik, print in order
# -----------------------------------------------------------------------------------

def Insert(root, segment, idx, x):
    #
    pointA, pointB = segment 

    if root == None: 
        root = BST( segment, idx )
        return root, root

    pointer = root 
    while root != None:
        parent = root 
        if computeValue(root.key[0], root.key[1], x) < computeValue(pointA, pointB, x): root = root.right 
        else: root = root.left 
    #end 'while' loop

    root = BST( segment, idx )
    root.parent = parent 

    if computeValue(pointA, pointB, x) < computeValue(parent.key[0], parent.key[1], x):
        parent.left = root 
    else:
        parent.right = root 
    #

    return pointer, root 
# end procedure Insert()

def Search(root, segment, x):
    #
    pointA, pointB = segment

    while root != None:
        #
        if root.key == (pointA, pointB): return root

        if computeValue(root.key[0], root.key[1], x) < computeValue(pointA, pointB, x):
            root = root.right 
        else:
            root = root.left 

    #end 'while' loop 

    return None 
#end procedure Search()


def Min(x):
    #
    while x.left: 
        x = x.left 
    #
    return x
# end procedure Min()

def Max(x):
    # 
    while x.right:
        x = x.right 
    #
    return x 
# end procedure Max()

# # succ(x) - jesli x ma prawe dziecko, to znajdz minimum w prawym poddrzewie x 
# # jesli x nie ma prawego dziecka, to wedruj w gore drzewa, poki jestes prawym synem. 

def Successor(root, segment, x): #nastepnik
    #
    pointA, pointB = segment 

    if root is None: return root
    succ = None 

    while root is not None:
        #
        #innymi slowy, aby znalezc nastepnik x (ktory tam nie ma prawego dziecka), to trzeba znalezc takiego node'a, że poprzednik node'a to x. 
        if root.key == (pointA, pointB):
            if root.right is not None:
                return Min( root.right )
            return succ

        if computeValue(root.key[0], root.key[1], x) > computeValue(pointA, pointB, x):
            succ = root 
            root = root.left 

        else:
            root = root.right 
        
    #
    return succ
#end procedure Successor()

def Predecessor(root, segment, x): # poprzednik 
    #
    pointA, pointB = segment 
    
    if root is None: return root 
    pred = None 

    while root is not None:
        #
        if root.key == (pointA, pointB): 
            if root.left is not None:
                return Max( root.left )
            return pred
        
        if computeValue(root.key[0], root.key[1], x) > computeValue(pointA, pointB, x):
            root = root.left

        else:
            pred = root 
            root = root.right 
        
    #
    # return pred.key 
    return pred
#end procedure Predecessor()


# https://www.techiedelight.com/deletion-from-bst/
# Case 1: Deleting a node with no children: remove the node from the tree.
# Case 2: Deleting a node with two children: znajdz successora, zamien te wartosci ze soba i wywolaj rekurencyjnie dla wartosci successora 
# Case 3: Deleting a node with one child: remove the node and replace it with its child.



def Successor2(x):
    return Min( x.right )
#end procedure Successor()

def Predecessor2(x):
    return Max( x.left )
# end procedure Predecessor()

def Remove(root, segment, val):
    #
    pointA, pointB = segment
    parent = None 
    x = root 

    while x and x.key != segment:
        parent = x 

        if computeValue(pointA, pointB, val) < computeValue(x.key[0], x.key[1], val):
            x = x.left 
        else:
            x = x.right 

    #

    if x is None: return root # - nie znaleziono wartosci 'value' do usuniecia 

    #Case 1: no children 
    if x.left is None and x.right is None:
        #
        if x != root:
            if parent.left == x:
                parent.left = None 
            else:
                parent.right = None 
            #
        else:
            root = None 
        #
    #

    #Case 2: two children 
    elif x.left and x.right: #successor ma napewno jedno dziecko 
        #
        succ = Successor2(x)
        Remove(x, succ.key, val)
        x.key = succ.key
    #

    #Case 3: one child 
    else:
        if x.left:
            child = x.left 
        else:
            child = x.right 

        if x != root:
            if x == parent.left:
                parent.left = child 
            else:
                parent.right = child 
        else:
            root = child 
        #
    #

    return root 
#end procedure Remove()
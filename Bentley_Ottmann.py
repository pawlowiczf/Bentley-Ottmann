from queue import PriorityQueue
from BST import * 

class Segment:
    def __init__(self, pointA, pointB, idx):
        self.pointA = pointA
        self.pointB = pointB 
        self.coords = (pointA, pointB)
        self.idx = idx

# end class Segment()

class CrossedPoint:
    def __init__(self, segmentA, segmentB):
        self.segmentA = segmentA
        self.segmentB = segmentB 
# end class CrossedPoint()

def Orientation(A, B, C):
    #
    ax, ay = A 
    bx, by = B 
    cx, cy = C 

    answer = (ax - cx) * (by - cy) - (ay - cy) * (bx - cx)
    return answer
#end procedure Orientation()

def doIntersect(segmentA, segmentB):
    #
    firstPointA, secondPointA = segmentA
    firstPointB, secondPointB = segmentB 

    firstOrientation  = Orientation( firstPointA, secondPointA, firstPointB  )
    secondOrientation = Orientation( firstPointA, secondPointA, secondPointB )

    thirdOrientation  = Orientation( firstPointB, secondPointB, firstPointA )
    fourthOrientation = Orientation( firstPointB, secondPointB, secondPointA )

    return ( firstOrientation * secondOrientation < 0 ) and ( thirdOrientation * fourthOrientation < 0 ) 
# end procedure doIntersect()

def pointIntersection(segmentA, segmentB):
    #
    (ax, ay), (bx, by) = segmentA
    (cx, cy), (dx, dy) = segmentB 

    a1 = (by - ay) / (bx - ax) 
    b1 = ay - a1 * ax 

    a2 = (dy - cy) / (dx - cx) 
    b2 = cy - a2 * cx 

    x = (b2 - b1) / (a1 - a2) 
    y = a1 * (b2 - b1) / (a1 - a2)  + b1

    return (x, y)
# end procedure pointIntersection()

def computeSlope(pointA, pointB):
    ax, ay = pointA
    bx, by = pointB 
    return (by - ay) / (bx - ax)
#

def computeValue(pointA, pointB, x):
    #
    ax, ay = pointA
    bx, by = pointB 

    slope = (by - ay) / (bx - ax) 
    intercept = ay - ax * slope 
    return slope * x + intercept 
# end procedure computeValue()

def prepareData(sections):
    #
    queue = PriorityQueue()
    for a in range( len(sections) ):
        pointA, pointB = sections[a]
        queue.put( (pointA, pointB, 0, Segment(pointA, pointB, a)) ) # 0 - poczatek odcinka
        queue.put( (pointB, pointA, 2, Segment(pointB, pointA, a) ) ) # 2 - koniec odcinka 
    #

    return queue
# end procedure prepareData()

def CheckForIntersect(queue, crossed, segmentA, segmentB, idxTuple):
    #
    if doIntersect(segmentA, segmentB):
        #
 
        intersection = pointIntersection(segmentA, segmentB)
        queue.put( (intersection, queue.qsize(), 1, CrossedPoint(segmentA, segmentB) ) ) 
        crossed.add( intersection ) 
    #
#end procedure CheckForIntersect()


def findIntersections(sections):
    #
    crossed = set()
    queue = prepareData(sections) 
    
    SL = None

    while not queue.empty():
    #   
        pointA, pointB, event, segmentNode = queue.get(block = False)

        if event == 0: # - poczatek odcinka 
            SL, pointer = Insert( SL, (pointA, pointB), segmentNode.idx, pointA[0] )

            succNode = Successor(SL, segmentNode.coords, pointA[0] )
            predNode = Predecessor(SL, segmentNode.coords, pointA[0] )

            if succNode is not None:
                CheckForIntersect(queue, crossed, segmentNode.coords, succNode.key, (segmentNode.idx, succNode.idx) )

            if predNode is not None:
                CheckForIntersect(queue, crossed, segmentNode.coords, predNode.key, (segmentNode.idx, predNode.idx) )
        #
            
        elif event == 2: # - koniec odcinka 
            succNode = Successor(SL, (pointB, pointA), pointA[0] )
            predNode = Predecessor(SL, (pointB, pointA), pointA[0] )
            
            if succNode is not None and predNode is not None:
                CheckForIntersect(queue, crossed, predNode.key, succNode.key, (predNode.idx, succNode.idx))
                
            #
            # SL = Remove(SL, (pointB, pointA), pointA[0])
            
            pointer = Search(SL, (pointB, pointA), pointA[0])
            if pointer is not None:
                SL = Remove(SL, pointer.key, pointA[0])
        

        elif event == 1: # punkt przeciecia 
            CONST = 0.0001

            pointerA = Search( SL, segmentNode.segmentA, pointA[0] - CONST)
            pointerB = Search( SL, segmentNode.segmentB, pointA[0] - CONST)
            
            if pointerA is None or pointerB is None: continue 

            SL = Remove(SL, pointerA.key, pointA[0] - CONST)
            SL = Remove(SL, pointerB.key, pointA[0] - CONST)
            
            SL, pointerA = Insert(SL, pointerA.key, pointerA.idx, pointA[0] + CONST)
            SL, pointerB = Insert(SL, pointerB.key, pointerB.idx, pointA[0] + CONST)

            if computeValue(pointerB.key[0], pointerB.key[1], pointA[0] + CONST) > computeValue(pointerA.key[0], pointerA.key[1], pointA[0] + CONST):
                succ = Successor( SL, pointerB.key, pointA[0] + CONST)
                pred = Predecessor(SL, pointerA.key, pointA[0] + CONST )

                if succ is not None:
                    CheckForIntersect(queue, crossed, segmentNode.segmentB, succ.key, (pointerB.idx, succ.idx) )                    

                if pred is not None:
                    CheckForIntersect(queue, crossed, segmentNode.segmentA, pred.key, (pointerA.idx, pred.idx) )

            #
            else:
                succ = Successor( SL, pointerA.key, pointA[0] + CONST)
                pred = Predecessor(SL, pointerB.key, pointA[0] + CONST)

                if succ is not None:
                    CheckForIntersect(queue, crossed, segmentNode.segmentA, succ.key, (pointerA.idx, succ.idx) )

                if pred is not None:
                    CheckForIntersect(queue, crossed, segmentNode.segmentB, pred.key, (pointerB.idx, pred.idx) )
            #
    

    return crossed 
# end procedure find_intersections()


from search import *
from fifteenpuzzle import *
import pickle
# import time
 
def patternHash(state):
    numbers = state.getOneDimentionalState()
    idx = 0
    for i in range(16):
        if numbers[i] in [1,5,6,9,10,13]:#[6,7,8,11,12]:#[1,2,3,4,5]:#[1,5,6,9,10,13]:#[2,3,4]:#[1,5,6,9,10,13]:
            val = numbers[i]
            idx = idx << 4 | val
            idx = idx << 4 | i
    return idx

def blankHash(state):
    numbers = state.getOneDimentionalState()
    idx = 0
    for i in range(16):
        if numbers[i] in [1,5,6,9,10,13,0]: #[6,7,8,11,12,0]:#[1,2,3,4,5,0]:#[1,5,6,9,10,13, 0]:#[2,3,4,0]: #[1,5,6,9,10,13, 0]:
            val = numbers[i]
            idx = idx << 4 | val
            idx = idx << 4 | i
    return idx

class LightNode:
    """A node with no parent. """
    def __init__(self, data):
        self.data = data    # tuple(state, cumulativeCost)

def createDB(problem):

    # startTime = time.time()

    fringe = Queue()
    closedSet = set()
    db = {}
    itr = 1

    fringe.push( LightNode((problem.getStartState(), 0)) )
    while len(db) < 5765760:  #524160: #5765760:
        if fringe.isEmpty():
            print('break')
            break
        node = fringe.pop()
        state, currCost = node.data
        patternHashValue = patternHash(state)
        itr += 1
        if itr % 10000 == 0:
                print(currCost)
                print(itr)
                print(len(db))

        if patternHashValue not in db:
            db[patternHashValue] = currCost

        successors = problem.getSuccessors(state)
        for successor in successors:
            sucState, _, _ = successor
            sucBlankHash = blankHash(sucState)
            if sucBlankHash not in closedSet:
                closedSet.add(sucBlankHash)
                if patternHash(sucState) != patternHashValue:
                    sucCost = currCost + 1
                else:
                    sucCost = currCost
                successorNode = LightNode((sucState, sucCost))
                
                fringe.push(successorNode)

    # endTime = time.time()
    # db['exeTime'] = endTime - startTime

    dbfile = open('DB_15691013', 'ab')
    pickle.dump(db, dbfile)                      
    dbfile.close()


numbers = [1, -1, -1, -1, 5, 6, 0, -1, 9, 10, -1, -1, 13, -1, -1, -1]
#[1, 2, 3, 4, 5, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1]
#[1, -1, -1, -1, 5, 6, 0, -1, 9, 10, -1, -1, 13, -1, -1, -1]
#[-1, -1, -1, -1, -1, -1, -1, -1, 9, 10, 0, -1, 13, 14, 15, -1]
#[-1, -1, -1, -1, -1, 6, 7, 8, 0, -1, 11, 12, -1, -1, -1, -1]
#[1, 2, 3, 4, 5, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1]
#[0, 2, 3, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

puzzle = FifteenPuzzleState(numbers)

print(puzzle)
print(patternHash(puzzle))
print(blankHash(puzzle))

problem = FifteenPuzzleSearchProblem(puzzle)
createDB(problem)
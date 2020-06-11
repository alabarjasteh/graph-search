# search.py
# ---------
#

import util
from util import *
from math import sqrt
import pickle
from sys import maxsize

class SearchProblem:

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """

    def isGoalState(self, state):
        """
           state: Search state
        Returns whether given state is goal or not.
        """

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """

class Node:
    def __init__(self, data, parent):
        self.data = data    # tuple(state, stepAction, cumulativeCost)
        self.parent = parent


def _search(problem, fringe=Stack):
    """Get fringe queuing strategy as argument, which helps
    adapt different search algorithms with just minor modifications.

    for dfs queue is LIFO stack(default)
    for bfs FIFO queue
    for UCS is priority queue
    """

    fringe = fringe()
    closedSet = set()
    path = []

    fringe.push(Node( (problem.getStartState(), 'Stop', 0), None) )
    while not fringe.isEmpty():
        node = fringe.pop()
        state, _, currCost = node.data

        #Goal check
        if problem.isGoalState(state):
            while node.parent:         #not None
                action = node.data[1]  # stepAction
                path.append(action)
                node = node.parent
            path.reverse()
            return path
        #Node expansion
        if state not in closedSet:
            closedSet.add(state)
            successors = problem.getSuccessors(state)
            for successor in successors:
                sucState, sucAction, _ = successor
                sucCost = currCost + 1
                successorNode = Node((sucState, sucAction, sucCost), node)
                fringe.push(successorNode)
    return []  # failed to find a path

def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first. """
    return _search(problem, Stack)




def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return _search(problem, Queue)

class BidirecNode:
    def __init__(self, state, action, parent):
        self.state = state 
        self.action = action
        self.parent = parent

    # def __hash__(self):
    #     return self.hash(state)

def reverseActionsDirection(actions):
    tmpList = []
    for action in actions:
        if action == 'up':
            tmpList.append('down')
        elif action == 'left':
            tmpList.append('right')
        elif action == 'right':
            tmpList.append('left')
        else:
            tmpList.append('up')
    return tmpList

def bidirectionalSearch(problem):
    """Forward search from initial state and backward search
    from goal simulaneously, until they meet at a same state."""
    
    fringe1 = Queue()
    fringe2 = Queue()
    closedDict1 = {}
    closedDict2 = {}
    path1 = []    #path from start to state that they meet
    path2 = []    #path from end to state that they meet

    fringe1.push(BidirecNode(problem.getStartState(),'Stop', None))
    fringe2.push(BidirecNode(problem.getGoalState(),'Stop', None))

    while not fringe1.isEmpty() and not fringe2.isEmpty():
        #pop from first fringe
        node1 = fringe1.pop()
        state1 = node1.state
        #goal test from start side
        if state1 in closedDict2 or problem.isGoalState(state1):
            #return path
            while node1.parent:         #not None
                action = node1.action  
                path1.append(action)
                node1 = node1.parent
            path1.reverse()
            node2 = closedDict2[state1]
            while node2.parent:         #not None
                action = node2.action  
                path2.append(action)
                node2 = node2.parent
            path2 = reverseActionsDirection(path2)
            return path1 + path2
        #Node expansion, push to first fringe
        if state1 not in closedDict1: 
            closedDict1[state1] = node1
            successors = problem.getSuccessors(state1)
            for successor in successors:
                sucState, sucAction, _ = successor
                successorNode = BidirecNode(sucState, sucAction, node1)
                fringe1.push(successorNode)

        #pop from second fringe
        node2 = fringe2.pop()
        state2 = node2.state
        #goal test from end side
        if state2 in closedDict1:
            #return path
            node1 = closedDict1[state2]
            while node1.parent:         #not None
                action = node1.action  
                path1.append(action)
                node1 = node1.parent
            path1.reverse()
            while node2.parent:         #not None
                action = node2.action  
                path2.append(action)
                node2 = node2.parent
            path2 = reverseActionsDirection(path2)
            return path1 + path2
        #Node expansion, push to second fringe
        if state2 not in closedDict2: 
            closedDict2[state2] = node2
            successors = problem.getSuccessors(state2)
            for successor in successors:
                sucState, sucAction, _ = successor
                successorNode = BidirecNode(sucState, sucAction, node2)
                fringe2.push(successorNode)
                
    return []  # failed to find a path

def _ucs(problem, heuristic, databases=None):

    fringe = PriorityQueue()
    closedSet = set()
    path = []

    fringe.push( Node(  (problem.getStartState(), 'Stop', 0)   , None) , 0)
    while not fringe.isEmpty():
        node = fringe.pop()
        state, _, currCost = node.data

        if problem.isGoalState(state):
            while node.parent:
                action = node.data[1]  # stepAction
                path.append(action)
                node = node.parent
            path.reverse()
            return path

        if state not in closedSet:
            closedSet.add(state)
            successors = problem.getSuccessors(state)
            for successor in successors:
                sucState, sucAction, stepCost = successor
                sucCost = currCost + stepCost + heuristic(sucState, problem, databases)
                successorNode = Node((sucState, sucAction, sucCost), node)

                fringe.push(successorNode, sucCost)
    return []  # failed to find a path


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    return _ucs(problem, nullHeuristic)


def nullHeuristic(state, problem, DB):
    "This heuristic is trivial."
    return 0

def manhattanHeuristic(state, problem, DB):
    "This fuction is not generic, but it is specifically developed for n2-1_puzzles"
    numbers = state.getOneDimentionalState()
    manhattan = 0
    for i in range(16):
        n = numbers[i]
        x1, y1 = i % 4, i // 4
        x2, y2 = n % 4, n // 4
        manhattan += abs(x1 - x2) + abs(y1 - y2)
    return manhattan

def linearConflictManhattanHeuristic(state, problem, DB):
    return manhattanHeuristic(state, problem, DB) + 2 * linearConflict(state, problem)

def linearConflict(state, problem):
    return _verticalLinearConflict(state, problem) + _horizontalLinearConflict(state, problem)

def _horizontalLinearConflict(state, problem):
    hConflicts = 0
    size = int(sqrt(len(state.getOneDimentionalState()))) # 4 for 15-puzzle
    for row in range(size):
        max = 0
        for col in range(size):
            value = state.cells[row][col]
            if value != 0 and value // size == row: #Each value must be in its row to be considered for linear conflict
                if value > max:    #In each row, values must be in ascending order to not count as a conflict
                    max = value
                else:
                    hConflicts += 1
    return hConflicts

def _verticalLinearConflict(state, problem):
    vConflicts = 0
    size = int(sqrt(len(state.getOneDimentionalState())))
    for col in range(size):
        max = 0
        for row in range(size):
            value = state.cells[row][col]
            if value != 0 and value % size == col:
                if value > max:
                    max = value
                else:
                    vConflicts += 1
    return vConflicts

def patternHash(state, patternList):
    """
    Returns hash value for each sublist of numbers of the puzzle.

    patternList: is a list of numbers is interested to be considered as
    a disjoint pattern in DPD heuristic, like [1,5,6,9,10,13].
    """
    numbers = state.getOneDimentionalState()
    idx = 0
    for i in range(16):
        if numbers[i] in patternList:
            val = numbers[i]
            idx = idx << 4 | val
            idx = idx << 4 | i
    return idx

def loadDBs():
    #load dictionaries from database files using pickle module
    dbFile1 = open('DB_12345', 'rb')
    db1 = pickle.load(dbFile1)
    dbFile1.close()

    dbFile2 = open('DB_6781112', 'rb')
    db2 = pickle.load(dbFile2)
    dbFile2.close()

    dbFile3 = open('DB_910131415', 'rb')
    db3 = pickle.load(dbFile3)
    dbFile3.close()
    return (db1, db2, db3)
    

def disjointHeuristic(state, problem, databases):
    
    #calc hash for each of three patterns
    p1_hash = patternHash(state, [1,2,3,4,5])
    p2_hash = patternHash(state, [6,7,8,11,12])
    p3_hash = patternHash(state, [9,10,13,14,15])

    db1, db2, db3 = databases

    #look up h1, h2, h3
    h1 = db1[p1_hash]
    h2 = db2[p2_hash]
    h3 = db3[p3_hash]

    # return max(h1, h2, h3)
    return h1 + h2 + h3

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    if heuristic == disjointHeuristic:
        return _ucs(problem, heuristic, loadDBs())
    return _ucs(problem, heuristic)

class VeryLightNode:
    def __init__(self, state, action, parent):
        self.state = state
        self.action = action 
        self.parent = parent

def iterativeDeepeningAStar(problem, heuristic=nullHeuristic):
    startState = problem.getStartState()
    startNode = VeryLightNode(startState,'Stop', None)
    threshold = heuristic(startState, problem, None)

    while True:
        temp = _idaSearch(problem, startNode, 0, threshold, heuristic)
        if isinstance(temp, VeryLightNode):
            #return path
            path = []
            node = temp
            while node.parent:
                action = node.action  # stepAction
                path.append(action)
                node = node.parent
            path.reverse()
            return path

        if temp == maxsize:  #sys.maxsize
            return []

        threshold = temp

def _idaSearch(problem, node, gValue, threshold, heuristic):
    state = node.state
    fValue = heuristic(state, problem, None) + gValue

    if fValue > threshold:
        return fValue
    if problem.isGoalState(state):
        #return node
        return node

    minValue = maxsize       #sys.maxsize

    successors = problem.getSuccessors(state)
    for successor in successors:
        sucState, sucAction, stepCost = successor
        sucgValue = gValue + stepCost
        sucNode = VeryLightNode(sucState, sucAction, node)
        temp = _idaSearch(problem, sucNode, sucgValue, threshold, heuristic)
        if isinstance(temp, VeryLightNode):
            return temp
        if temp < minValue:
            minValue = temp
    return minValue

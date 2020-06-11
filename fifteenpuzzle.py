# fifteenpuzzle.py
# ----------------
#


import search
from search import *
import random
import time


class FifteenPuzzleState:
    """
    This class defines the mechanics of the puzzle itself. The
    task of recasting this puzzles as a search problem is left to
    the FifteenPuzzleSearchProblem class.
    """

    def __init__( self, numbers ):
        """
          Constructs a new fifteen puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 15 representing an
          instance of the fifteen puzzle.  0 represents the blank
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

          represents the fifteen puzzle:
            ---------------------
            |  1 |    |  2 |  3 |
            ---------------------
            |  4 |  5 |  6 |  7 |
            ---------------------
            |  8 |  9 | 10 | 11 |
            ---------------------
            | 12 | 13 | 14 | 15 |
            ---------------------
        
        """
        # self.cells = []
        # numbers = numbers[:] # Make a copy so as not to cause side-effects.
        # numbers.reverse()
        # for row in range( 4 ):
        #     self.cells.append( [] )
        #     for col in range( 4 ):
        #         self.cells[row].append( numbers.pop() )
        #         if self.cells[row][col] == 0:
        #             self.blankLocation = row, col

        self.numbers = numbers
        for i in range(16):
            if numbers[i] == 0:
                row, col =  i // 4, i % 4
                self.blankLocation = row, col
                break

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.

            ---------------------
            |    |  1 |  2 |  3 |
            ---------------------
            |  4 |  5 |  6 |  7 |
            ---------------------
            |  8 |  9 | 10 | 11 |
            ---------------------
            | 12 | 13 | 14 | 15 |
            ---------------------

        >>> FifteenPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]).isGoal()
        True

        >>> FifteenPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]).isGoal()
        False
        """
        # current = 0
        # for row in range( 4 ):
        #     for col in range( 4 ):
        #         if current != self.cells[row][col]:
        #             return False
        #         current += 1
        # return True
        return hash(self) == 2223857479997207063 #hash  of goal state

    def getOneDimentionalState(self):
        # return [number for sublist in self.cells for number in sublist]
        return self.numbers

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> FifteenPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]).legalMoves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != 3):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != 3):
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new fifteenPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # # Create a copy of the current fifteenPuzzle
        # newPuzzle = FifteenPuzzleState([0 for _ in range(16)])
        # newPuzzle.cells = [values[:] for values in self.cells]
        # # And update it to reflect the move
        # newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        # newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        # newPuzzle.blankLocation = newrow, newcol

        oldIndex = row * 4 + (col + 1) -1
        newIndex = newrow * 4 + (newcol + 1) - 1
        newPuzzle = FifteenPuzzleState(self.numbers[:])
        newPuzzle.numbers[oldIndex] = self.numbers[:][newIndex]
        newPuzzle.numbers[newIndex] = self.numbers[:][oldIndex]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two fifteenPuzzles with the same configuration
          are equal.

          >>> FifteenPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]) == \
              FifteenPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]).result('left')
          True
        """
        # for row in range( 4 ):
        #     if self.cells[row] != other.cells[row]:
        #         return False
        # return True
        return hash(self) == hash(other)


    def __hash__(self):
        # return hash(str(self.cells))
        numbers = self.getOneDimentionalState()
        idx = 0
        for i in range(16):
            val = numbers[i]
            idx |= i << (val * 4)
        return idx


    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        # lines = []
        # horizontalLine = ('-' * (18))
        # lines.append(horizontalLine)
        # for row in self.cells:
        #     rowLine = '|'
        #     for col in row:
        #         if col == 0:
        #             col = ' '
        #         rowLine = rowLine + ' ' + col.__str__() + ' |'
        #     lines.append(rowLine)
        #     lines.append(horizontalLine)
        # return '\n'.join(lines)
        cells = []
        numbers = self.numbers[:] # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range( 4 ):
            cells.append( [] )
            for col in range( 4 ):
                cells[row].append( numbers.pop() )
        lines = []
        horizontalLine = ('-' * (21))
        lines.append(horizontalLine)
        for row in cells:
            rowLine = '|'
            for col in row:
                if col // 10 == 1:
                    rowLine = rowLine + ' ' + col.__str__() + ' |'
                else:
                    if col == 0:
                        col = ' '
                    rowLine = rowLine + '  ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)


    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class FifteenPuzzleSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Fifteen Puzzle domain

      Each state is represented by an instance of an fifteenPuzzle.
    """
    def __init__(self,puzzle):
        "Creates a new FifteenPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def getGoalState(self):
        return FifteenPuzzleState([i for i in range(16)])

    def isGoalState(self,state):
        return state.isGoal()

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


FIFTEEN_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  #1   trivial
                     [4, 1, 2, 3, 8, 5, 6, 7, 0, 9, 10, 11, 12, 13, 14, 15],    #20  joke
                     [5, 2, 6, 3, 1, 9, 7, 11, 0, 4, 13, 10, 8, 12, 14, 15],    #40  hard
                     [9, 2, 0, 3, 1, 4, 6, 11, 5, 8, 7, 10, 12, 13, 14, 15],    #70  very hard
                     [3, 1, 0, 2, 6, 4, 9, 7, 13, 8, 10, 11, 5, 12, 14, 15],    #100 insane
                     [1, 2, 11, 6, 5, 0, 7, 3, 12, 13, 9, 10, 14, 8, 15, 4]]    #150 looks like unsolvable

def loadFifteenPuzzle(puzzleNumber):
    """
      puzzleNumber: The number of the fifteen puzzle to load.

      Returns an eight puzzle object generated from one of the
      provided puzzles in FIFTEEN_PUZZLE_DATA.

      puzzleNumber can range from 0 to 5.

      >>> print(loadFifteenPuzzle(0))

    ---------------------
    |  1 |    |  2 |  3 |
    ---------------------
    |  4 |  5 |  6 |  7 |
    ---------------------
    |  8 |  9 | 10 | 11 |
    ---------------------
    | 12 | 13 | 14 | 15 |
    ---------------------
    """
    return FifteenPuzzleState(FIFTEEN_PUZZLE_DATA[puzzleNumber])

def createRandomFifteenPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random fifteen puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.
    """
    puzzle = FifteenPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    for _ in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

if __name__ == '__main__':
    """
    IMPORTANT: Uncomment any search you want to execute on puzzle. 
    """
    # grid = list(input('Enter the 15-puzzle you want to be solved as a two-dimentional list.'))
    # # [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    # numbers = [v for values in grid for v in values]
    # print(numbers)
    # puzzle = FifteenPuzzleSearchProblem(numbers)

    # puzzle = createRandomFifteenPuzzle(10)
    puzzle = loadFifteenPuzzle(3)
    loadFifteenPuzzle
    print('A random puzzle:')
    print(puzzle)

    problem = FifteenPuzzleSearchProblem(puzzle)

    startTime = time.time()

    # path = search.aStarSearch(problem, linearConflictManhattanHeuristic)
    # path = search.breadthFirstSearch(problem)
    path = search.bidirectionalSearch(problem)
    # path = search.aStarSearch(problem, manhattanHeuristic)
    # path = search.uniformCostSearch(problem)
    # path = search.aStarSearch(problem, disjointHeuristic)
    # path = search.iterativeDeepeningAStar(problem, manhattanHeuristic)

    endTime = time.time()

    print('Search found a path of %d moves: %s' % (len(path), str(path)))
    print("--- puzzle solved in %s seconds ---" % (endTime - startTime))

    print ('Results are writed in a txt file. You can watch steps that puzzle would take to reach the goal!')

    i = 1
    currPuzzle = puzzle
    f = open('results.txt', 'w+')
    f.write(str(4) + '\n')
    f.write(str(currPuzzle.numbers[i]) + ',')
    for a in path:
        currPuzzle = currPuzzle.result(a)   
        for i in range(16):
            f.write(str(currPuzzle.numbers[i]) + ',')
        f.write('\n')
    
    f.close()

    curr = puzzle
    # print(path)
    # print(curr)
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)
        
        input("Press return for the next state...")   # wait for key stroke
        i += 1


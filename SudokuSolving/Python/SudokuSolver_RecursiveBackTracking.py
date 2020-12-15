#
# Sudoku Solver... using recursive backtracking
# 
# Usage: > python SudokuSolver_RecursiveBackTracking.py  <TestFile>  [TestStats]
#
# Where: <TestFile>: the file containing the puzzle
#        [TestStats]: optional parameter to output stats; note if not present only solution is printed
#          -> FULL_SOL: output solution with timing and iteration values
#          -> JUST_STATS: output only timing and iteration values
#          -> ONLY_TIME: output only timing value
# 


import sys
import time

FunctionCallCount = 0;



#
# ReadInPuzzle: note that we are not doing anything fancy here.  We are just reading in
# numbers and verifing that things are correct or well-formed.
# 
def ReadInPuzzle (iFileName):

    puzzle = []

    #inputFile = open (iFileName, 'r')
    with open (iFileName, 'r') as inputFile:

        for line in inputFile:
            values = line.split()
            row = []

            for token in values:
                if token == '_':
                    row.append (0)
                else:
                    row.append (int(token))

            puzzle.append (row)

        inputFile.close ()

    return puzzle



#
# WriteOutPuzzle (iPuzzle)
#
def WriteOutPuzzle (iPuzzle):

    for i in range (9):

        line = ''
        for j in range (9):

            if iPuzzle[i][j] == 0:
                line += '_'
            else:
                line += str(iPuzzle[i][j])

            line += ' '

            if (j == 2 or j == 5):
                line += '| '

        print (line)
        if (i == 2 or i == 5):
            print ('------+-------+-------')



#
# TestValue... Check to see if a value is possible at a particular location
#
def TestValue (iPuzzle, iLoc, jLoc, iValue):

    # then check the row
    for j in range (9):
        if iPuzzle[iLoc][j] == iValue:
            return False;

    # then check the column
    for i in range (9):
       if iPuzzle[i][jLoc] == iValue:
           return False;

    # and finally check the region
    nRegionStartI = 3 * (iLoc // 3)
    nRegionStartJ = 3 * (jLoc // 3)
    for k in range (9):
        i = k // 3
        j = k % 3
        if iPuzzle[nRegionStartI + i][nRegionStartJ + j] == iValue:
            return False;

    return True;



#
# FindEmptySpace... returns the location of an empty space
#
def FindEmptySpace (iPuzzle):

    for nRow in range (9):
        for nCol in range (9):
            if iPuzzle[nRow][nCol] == 0:
                return (nRow, nCol)

    return (-1, -1)



#
# CountNonZeroValues: count the number of given values on the original puzzle
#
def CountNonZeroValues (iPuzzle):

    nCount = 0

    for i in range(9):
        for j in range(9):
            if iPuzzle[i][j] != 0:
                nCount += 1

    return nCount



#
# SolvePuzzle
#
def SolvePuzzle (iPuzzle):

    global FunctionCallCount
    FunctionCallCount += 1

    # Find the location of the first empty space.  If no spaces are empty
    # then the puzzle is solved... so we return true.
    (i, j) = FindEmptySpace (iPuzzle) 
    if i == -1:
        return True

    # Test out all the candidate values... 1 to 9
    for num in range (1, 10):
    
        if TestValue (iPuzzle, i, j, num):

            # If the candidate number 'works' set it in the puzzle
            iPuzzle[i][j] = num
                                       
            # Repeat this for the next space...
            if SolvePuzzle (iPuzzle):
                return True;

            # if the previous call to SolvePuzzle returned false (if no numbers were successful)
            # then make the number blank.  Since this function is recursively called, control flow
            # will return back to the previous call.
            iPuzzle[i][j] = 0;

    return False;



if __name__ == "__main__":
    
    if len(sys.argv) < 2 or len(sys.argv) > 3:

        print ('Error: incorrect number of parameters!')
        print ('Usage: ' + sys.argv[0] + ' <TestFile>  [TestStats]')
        print ()
        print ('<TestFile>: the file containing the puzzle')
        print ('[TestStats]: optional parameter to output stats; note if not present only solution is printed')
        print ('   -> FULL_SOL: output solution with timing and iteration values')
        print ('   -> JUST_STATS: output only timing and iteration values')
        print ('   -> ONLY_TIME: output only timing value')
        sys.exit ();

    # Read in the file...
    puzzleToSolve = ReadInPuzzle (sys.argv[1])

    numGivenValues = CountNonZeroValues (puzzleToSolve)

    # Output stats...
    outputStatMode = 0
    if len(sys.argv) == 3:
        if sys.argv[2] == 'FULL_SOL':
            outputStatMode = 1
        elif sys.argv[2] == 'JUST_STATS':
            outputStatMode = 2
        elif sys.argv[2] == 'ONLY_TIME':
            outputStatMode = 3

    tic = time.perf_counter_ns()
    SolvePuzzle (puzzleToSolve)
    toc = time.perf_counter_ns()
    timeElapsed = (toc - tic) / 1000

    if outputStatMode == 0 or outputStatMode == 1:
        WriteOutPuzzle (puzzleToSolve)

    if outputStatMode == 1: 
        print (f'Solved in: {timeElapsed:0.4f} microsec')
        print (f'Iterations: {FunctionCallCount}')
        print (f'Number Givens: {numGivenValues}')
    elif outputStatMode == 2:
        print (f'{timeElapsed:0.4f} {FunctionCallCount} {numGivenValues}')
    elif outputStatMode == 3:
        print (f'{timeElapsed:0.4f}')




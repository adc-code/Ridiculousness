#
# SudokuSolver_Constraints.py: Contraint based Sudoku solver.  Original implementation taken
# from github: https://gist.github.com/lucaswiman/f6769d2e866407dd784d1f29d3556771
# Note that the code was modified to to allow for input and output compared to the other
# solver implementations.
#
# Note:
# To use this code the python constraint solver must be part of one's environment.  Therefore
# one needs to call: pip install python-constraint
#
# Usage: > python SudokuSolver_Constraints.py  <TestFile>  [TestStats]
#
# Where: <TestFile>: the file containing the puzzle
#        [TestStats]: optional parameter to output stats; note if not present only solution is printed
#          -> FULL_SOL: output solution with timing and iteration values
#          -> JUST_STATS: output only timing and iteration values
#          -> ONLY_TIME: output only timing value
#


from constraint import *
import time
import sys


ROWS         = 'abcdefghi'
COLS         = '123456789'
DIGITS       = range(1, 10)
VARS         = [row + col for row in ROWS for col in COLS]
ROWGROUPS    = [[row + col for col in COLS] for row in ROWS]
COLGROUPS    = [[row + col for row in ROWS] for col in COLS]
SQUAREGROUPS = [ [ROWS[3 * rowgroup + k] + COLS[3 * colgroup + j]
                 for j in range(3) for k in range(3)]
                 for colgroup in range(3) for rowgroup in range(3) ]


def ReadInPuzzle (iFileName):

    puzzle = []
    with open (iFileName, 'r') as inputFile:

        for line in inputFile:
            values = line.split()
            for token in values:
                if token == '_':
                    puzzle.append (0)
                else:
                    puzzle.append (int(token))
        inputFile.close ()
    return puzzle


def CountNonZeroValues (values):

    nCount = 0
    for i in values:
        if i != 0:
           nCount += 1

    return nCount



def solve (hints):

    problem = Problem()
    for var, hint in zip (VARS, givenValues):
        problem.addVariables ([var], [hint] if hint in DIGITS else DIGITS)

    for vargroups in [ROWGROUPS, COLGROUPS, SQUAREGROUPS]:
        for vargroup in vargroups:
            problem.addConstraint (AllDifferentConstraint(), vargroup)

    return problem.getSolution()


def pretty (var_to_value):
    puzzle = ''
    for rownum, row in enumerate ('abcdefghi'):
        for colnum, col in enumerate ('123456789'):
            puzzle += str(var_to_value[row+col]) + ' '
            if colnum % 3 == 2 and colnum != 8:
                puzzle += '| '
        puzzle += '\n'
        if rownum % 3 == 2 and rownum != 8:
            puzzle += '------+-------+-------\n'

    return puzzle 


givenValues = (0, ) * 81


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
    givenValues = ReadInPuzzle (sys.argv[1])

    numGivenValues = CountNonZeroValues (givenValues)

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
    solution = solve (givenValues)
    toc = time.perf_counter_ns()
    timeElapsed = (toc - tic) / 1000

    if outputStatMode == 0 or outputStatMode == 1:
        print (pretty(solution))

    if outputStatMode == 1: 
        print (f'Solved in: {timeElapsed:0.4f} microsec')
        print (f'Number Givens: {numGivenValues}')
    elif outputStatMode == 2:
        print (f'{timeElapsed:0.4f} -1 {numGivenValues}')
    elif outputStatMode == 3:
        print (f'{timeElapsed:0.4f}')



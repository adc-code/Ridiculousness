#
# Compare_CppPy.py
# Used to compare various sudoku solvers.  This is done by using the various test cases, 
# and comparing the actual run time between implementations.
#


import os
import glob
import statistics 
import matplotlib.pyplot as plt
import numpy as np


def getValues (iFileName):

    inputFile = open (iFileName, 'r')

    line = inputFile.readline ()
    tokens = line.split ()

    inputFile.close ()

    return (float(tokens[0]), int(tokens[1]), int(tokens[2]))


solverType = [ '../C++V2/SudokuSolver_RecursiveBackTracking', 'python ../Python/SudokuSolver_Constraints.py', 'python ../Python/SudokuSolver_Crooks.py' ]
solverInfo = [ 'Recursive Backtracking Using C++', 'Constraint Solving Using Python', 'Crooks Algorithm Using Python' ]

testCaseDir     = '../Tests/'
testCaseTypes   = [ 'Easy', 'Medium', 'Hard', 'Evil' ]
testCaseOutput  = '.tempStats'

numTrials       = 10


results = {}

for solver in solverType:

    print ('Getting results for: ' + solver)

    solverResults = []
    for caseType in testCaseTypes:

        CaseLists = glob.glob (testCaseDir + caseType + '*') 

        for testCase in CaseLists:

            print ('  --> ', testCase)

            times  = []
            iters  = 0
            givens = 0
        
            for trial in range (numTrials):    
                cmd = solver + ' ' + testCase + ' JUST_STATS ' + ' > ' + testCaseOutput
                os.system (cmd)

                time, iters, givens = getValues (testCaseOutput)
                times.append (time)

            solverResults.append ( { 'Case' :            testCase,                 \
                                     'MeanTime':         statistics.mean(times),   \
                                     'NumberIterations': iters,                    \
                                     'GivenValues':      givens } )
    
    results[solver] = solverResults


# ...and graph them
plt.figure ()
plt.style.use ('seaborn-whitegrid')

for solver in solverType:
    
    xValues = []
    yValues = []

    for solverResults in results [solver]:

        xValues.append (solverResults ['GivenValues'])
        yValues.append (solverResults ['MeanTime'])

    plt.scatter (xValues, yValues, s=4, alpha=0.9)

    xValuesLine = []
    yValuesLine = []

    givenUniqueValues = list(set (xValues))
    givenUniqueValues.sort ()

    for givenUniqueValue in givenUniqueValues:
        meanTimePerGivenValue = []
        for index, value in enumerate (xValues):
            if value == givenUniqueValue:
                meanTimePerGivenValue.append (yValues[index])
        
        xValuesLine.append (givenUniqueValue)
        yValuesLine.append (statistics.mean(meanTimePerGivenValue))

    plt.plot (xValuesLine, yValuesLine)

plt.xlabel ('Number of given values')
plt.ylabel ('Time to solve (ms)')
plt.legend (solverInfo)
plt.title ('Time to Solve Comparison')
plt.ylim ( (0, 100000) )

plt.show ()




#
# Compare_CppPy.py
# Used to compare the C++ and Python implementations of the recursive backtracking algorithm. 
# This is done by using the various test cases, and comparing the actual run time between
# implementations.
#


import os
import glob
import statistics 
import matplotlib.pyplot as plt
import numpy as np


plt.style.use ('seaborn-whitegrid')


def getValues (iFileName):

    inputFile = open (iFileName, 'r')

    line = inputFile.readline ()
    tokens = line.split ()

    inputFile.close ()

    return (float(tokens[0]), int(tokens[1]), int(tokens[2]))


solverType = [ '../C++V2/SudokuSolver_RecursiveBackTracking' , 'python ../Python/SudokuSolver_RecursiveBackTracking.py' ]
solverInfo = [ 'Recursive Backtracking Using C++', 'Recursive Backtracking Using Python' ]

testCaseDir     = '../Tests/'
testCaseTypes   = [ 'Easy', 'Medium', 'Hard', 'Evil' ]
testCaseOutput  = '.tempStats'

# Since the computations time can vary between the two implementations we perform
# the calculation a few times and then find the average time
numTrials       = 10


# Compute the results
results = {}
timePerIter = {}

for solver in solverType:

    print ('Getting results for: ' + solver)

    solverResults = []
    solverTimePerIter = []
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
                solverTimePerIter.append (time / iters)
               

            solverResults.append ( { 'Case' :            testCase,                 \
                                     'MeanTime':         statistics.mean(times),   \
                                     'NumberIterations': iters,                    \
                                     'GivenValues':      givens } )
 
    results[solver] = solverResults
    timePerIter[solver] = solverTimePerIter


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

plt.show ()


plt.figure ()
for solver in solverType:
    print (solver)
    print ('   --> Mean Time per Iteration: ', statistics.mean (timePerIter[solver]), ' ms')
    print ('   --> Standard Deviation: ', statistics.stdev(timePerIter[solver]), ' ms')

    plt.hist (timePerIter[solver], bins=20, rwidth=0.95)
    plt.xlabel ('Average time per iteration (ms)')
    plt.ylabel ('Counts')
    plt.title ('Average Time Per Iteration Comparison')
    
plt.show ()




# 
#       _                 _     _      ____        _
#      | |_   _ _ __ ___ | |__ | | ___/ ___|  ___ | |_   _____ _ __
#   _  | | | | | '_ ` _ \| '_ \| |/ _ \___ \ / _ \| \ \ / / _ \ '__|
#  | |_| | |_| | | | | | | |_) | |  __/___) | (_) | |\ V /  __/ |
#   \___/ \__,_|_| |_| |_|_.__/|_|\___|____/ \___/|_| \_/ \___|_|
# 
# Simple tool used to solve -most- daily jumble puzzles.  The algorithm
# looks up solutions in a dictionary, hence solutions may or may not be 
# found depending on the contents of the dictionary.
#
# Usage:
# For now it is simply a command line tool...
#
# > python JumbleSolver.py  <PuzzleFile.txt>
#


import sys
import itertools


def GetWords (allWords, indices):
    # should verify that allWords and indices are the same length
    results = []
    for i in range (len(indices)):
        results.append (allWords[i][indices[i]])

    return results


def GetLetters (words, letterIndices):
    # again should verify that words and letterIndices are the same length
    results = []

    for i in range(len(letterIndices)):
        for j in range(len(letterIndices[i])):
            if letterIndices[i][j] == '*':
                results.append (words[i][j])

    return results


def GetRemainingLetters (allLetters, toBeRemoved):
    results = allLetters 
    for char in toBeRemoved:
        loc = results.find (char)
        if loc != -1:
            results = results[:loc] + results[(loc+1):]

    return results


#
# BuildWordDict: Used to build our word-dictionary hash table
#
def BuildWordDict (dictFile):
    wordDict = {}

    f = open (dictFile, 'r')

    for word in f.readlines():
  
        word = word.strip () 
        sortedChars = sorted (word)
        sortedKey = ''.join (sortedChars)
        sortedKey.upper () 

        if sortedKey in wordDict:
            wordDict [sortedKey].append (word)
        else:
            wordDict [sortedKey] = [ word ]

    f.close ();

    # uncomment for testing
    # print (len(wordDict))

    return wordDict


#
# LoadAndVerifyPuzzleFile: used to load and verify the puzzle file.
#
def LoadAndVerifyPuzzleFile (puzzleFile):

    f = open (puzzleFile, 'r')

    words         = []
    selLetters    = []
    finalClueLens = []

    selLetterCount = 0

    for line in f.readlines():

        line   = line.strip ()
        tokens = line.split ()
        
        # note that FC stands for Final Clue
        if tokens[0] == 'FC':
            for i in range(1, len(tokens)):
                finalClueLens.append (int(tokens[i]))
        else:
            words.append (tokens[0])
            selLetters.append (tokens[1])
            selLetterCount += tokens[1].count ('*')

    if selLetterCount != sum (finalClueLens):
        raise Exception ('Selected letters and final clue letters do not match up!')

    f.close ()

    return words, selLetters, finalClueLens



#
# LookupWords: used to look up a word in the hash table dictionary
#
def LookupWords (words):

    wordSolutions = []

    for word in words:

        key = sorted (word)
        key = ''.join (key)
        key.upper ()

        if key in wordDict:
            wordSolutions.append ( wordDict[key] )
        else:
            wordSolutions.append ( -1 )

    return wordSolutions

     
#
# FindWordsFromLetters: Used to recursively test combinations of letters to determine the final clue
# 
def FindWordsFromLetters (letters, finalClueLen, element, solutions, currentSolution):

    # uncomment for debugging
    # print ('FindWordsFromLetters...  num letters: ', len(letters), ' element: ', element, ' len sols: ', len(solutions), ' len currSols: ', len(currentSolution))

    if element >= len(finalClueLen):
        return

    letterCombos = list (itertools.combinations (letters, finalClueLen[element]))

    if element == 0:
        currentSolution = []

    for particularLetterCombo in letterCombos:

        # test all letter combinations for the first word
        key = sorted (particularLetterCombo)
        key = ''.join (key)
        
        if key in wordDict:
   
            # this is a possible solution remember it
            currentSolution.append (key)

            strLetters = ''.join (letters)
            remainingLetters = GetRemainingLetters (strLetters, key)
   
            # recursively solve again with the next word with the remaining letters
            FindWordsFromLetters (remainingLetters, finalClueLen, element+1, solutions, currentSolution)
          
            # if we are on the last word and it is a solution add it to the solution list if it hasn't
            # been found yet
            if currentSolution not in solutions and element == len(finalClueLen)-1:
                solutions.append (currentSolution.copy())
           
            # since we are calling this in a loop, we need to remove the element we added 
            currentSolution.pop ()



#
# MakeWordString
#
def MakeWordString (wordArray):
    
    resultStr = ''

    for word in wordArray:
        resultStr += word + '  '

    return resultStr



#
#
#
if __name__ == '__main__':

    # test to see if we have enough parameters
    if len (sys.argv) != 2:
        print ('Error: not enough parameters')
        print ()
        print ('Usage: ', sys.argv[0], '  <FileName>')

        sys.exit ()

    
    # Load puzzle file...
    puzzleFile = sys.argv[1]
    try:
        print ('Loading Puzzle...')
        words, selLetters, finalClueLen = LoadAndVerifyPuzzleFile (puzzleFile)
       
        # uncomment for testing
        # print (words, selLetters, finalClueLen)

    except Exception as e:
        print ('Error reading puzzle file... ', e)
        sys.exit ()

    
    print ('Loading dictionary file...')
    wordDict = BuildWordDict ('ScrabbleDict.txt')


    # solve the given words
    wordSolutions = LookupWords (words)
    errors = False
    for i in range (len (words)):

        solText = 'Count no find solution'
        if wordSolutions[i] == -1:
            errors = True
        else:
            solText = MakeWordString (wordSolutions[i])

        print ('  ' + words[i] + ' --> ' + solText)

    if errors:
        sys.exit ()

    
    # Add a blank line before solving
    print ()

    wordSolutionIndices = [ list(range(0, len(sol))) for sol in wordSolutions ]
    #print (wordSolutionIndices)

    wordSolCombos = list (itertools.product (*wordSolutionIndices) )

    for wordCombo in wordSolCombos:
   
        particularWordSol = GetWords (wordSolutions, wordCombo)
        print ('Solution Words: ', MakeWordString (particularWordSol))
    
        finalLetters = GetLetters (particularWordSol, selLetters)
        print ('Final Letters: ', MakeWordString (finalLetters))

        solutionKeys = []

        solutions = []
        tmp = [] 
        element = 0;
        FindWordsFromLetters (finalLetters, finalClueLen, element, solutions, tmp)

        print ('Final solution(s): ')
        
        if len (solutions) == 0:
            print ('  Could not find any solutions')
 
        # expand solutions
        for sol in solutions:
            
            wordList = []
            for key in sol:
                wordList.append (wordDict [key])
                
            combos = list (itertools.product(*wordList))
            
            for sol in combos:
                print ('  ' + MakeWordString (sol))
                   
                
        print ()



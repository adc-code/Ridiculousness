//
// Sudoku Solver... using recursive backtracking
// 

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include <ctype.h>
#include <stdlib.h>

#include <chrono>
#include <ctime>


typedef  std::vector<int>       ROW_TYPE;
typedef  std::vector<ROW_TYPE>  PUZZLE_TYPE;

long long  FunctionCallCount = 0;


// 
// ReadInPuzzle: note that we are not doing anything fancy here.  We are just reading in
// numbers and verifing that things are correct or well-formed. 
//
PUZZLE_TYPE ReadInPuzzle (char * iFileName)
{
    PUZZLE_TYPE newPuzzle;

    std::ifstream inputFile;
    inputFile.open (iFileName, std::ifstream::in);

    for (int i = 0; i < 9; i++)
    {
        ROW_TYPE newRow;

        for (int j = 0; j < 9; j++)
        {
            char newValue;
            inputFile >> newValue;

            if (!isdigit (newValue))
            {
                // it is a blank space... consider it to be zero
                newRow.push_back (0);
            }
            else
            {
                // should raise an error for zeros, but we will live with them for now
                newRow.push_back (newValue - '0');
            }
        }

        newPuzzle.push_back (newRow);
    } 
    inputFile.close ();

    return newPuzzle;
}


//
// WriteOutPuzzle 
//
void WriteOutPuzzle (PUZZLE_TYPE & iPuzzle)
{
    for (int i = 0; i < 9; i++)
    {
        for (int j = 0; j < 9; j++)
        {
            if (iPuzzle[i][j] == 0)
                std::cout << "_";
            else
                std::cout << iPuzzle[i][j];

            std::cout << " ";            
      
            if ( j == 2 || j == 5 )
                std::cout << "| ";
        }
        
        if (i == 2 || i == 5)
            std::cout << std::endl << "------+-------+-------" << std::endl;
        else
            std::cout << std::endl;
    }
}


//
// CountNonZeroValues (PUZZLE_TYPE & iPuzzle)
//
int CountNonZeroValues (PUZZLE_TYPE & iPuzzle)
{
    int nCount = 0;

    for (int i = 0; i < 9; i++)
        for (int j = 0; j < 9; j++)
            if (iPuzzle[i][j] != 0)
                nCount++;

    return nCount;
}


//
// TestValue... Check to see if a value is possible at a particular location
//
bool TestValue (PUZZLE_TYPE & iPuzzle, int iTestI, int iTestJ, int iValue)
{
    // First check the row
    for (int j = 0; j < 9; j++)
       if (iPuzzle[iTestI][j] == iValue)
           return false;       

    // then check the column
    for (int i = 0; i < 9; i++)
       if (iPuzzle[i][iTestJ] == iValue)
           return false;

    // and finally check the region
    int nRegionStartI = 3 * (iTestI / 3);
    int nRegionStartJ = 3 * (iTestJ / 3);
    for (int k = 0; k < 9; k++)
    {
        int i = k / 3;
        int j = k % 3;
        if (iPuzzle[nRegionStartI + i][nRegionStartJ + j] == iValue)
            return false;
    }

    return true;
}


//
// FindEmptySpace... returns the location of an empty space
//
bool FindEmptySpace (PUZZLE_TYPE & iPuzzle, int & nRow, int & nCol)
{
    for (nRow = 0; nRow < 9; nRow++)
        for (nCol = 0; nCol < 9; nCol++)
            if (iPuzzle[nRow][nCol] == 0)
                return true;

    return false;
}


//
// SolvePuzzle
//
bool SolvePuzzle (PUZZLE_TYPE & iPuzzle)
{
    FunctionCallCount++;

    // Find the location of the first empty space.  If no spaces are empty
    // then the puzzle is solved... so we return true.
    int i = 0;
    int j = 0;
    if (!FindEmptySpace (iPuzzle, i, j))
        return true;

    // Test out all the candidate values... 1 to 9
    for (int num = 1; num <= 9; num++)
    {
        if (TestValue (iPuzzle, i, j, num))
        {
            // If the candidate number 'works' set it in the puzzle
            iPuzzle[i][j] = num;
                                       
            // Repeat this for the next space...
            if (SolvePuzzle (iPuzzle))
                return true;

            // if the previous call to SolvePuzzle returned false (if no numbers were successful)
            // then make the number blank.  Since this function is recursively called, control flow
            // will return back to the previous call.
            iPuzzle[i][j] = 0;
        }
    }

    return false;
}


//
// Main function... where everything happens...
//
int main (int argc, char * argv [])
{
    if (argc < 2 || argc > 3)
    {
        std::cout << "Error: incorrect number of parameters!"              << std::endl << std::endl;
        std::cout << "Usage: " << argv[0] << " <TestFile>   [TestStats]"   << std::endl << std::endl;
        std::cout << "<TestFile>: the file containing the puzzle"          << std::endl;
        std::cout << "[TestStats]: optional parameter to output stats; note if not present only solution is printed" << std::endl;
        std::cout << "  -> FULL_SOL: output solution with timing and iteration values" << std::endl;
        std::cout << "  -> JUST_STATS: output only timing and iteration values"        << std::endl;
        std::cout << "  -> ONLY_TIME: output only timing value"                        << std::endl;

        exit (EXIT_FAILURE);
    }

    // Read in the puzzle file...
    PUZZLE_TYPE puzzleToSolve = ReadInPuzzle (argv[1]);

    int nonZeroValues = CountNonZeroValues (puzzleToSolve);

    // Output stats...
    int outputStatMode = 0;
    if (argc == 3)
    {
        std::string strOutputMode (argv[2]);
        if (strOutputMode == "FULL_SOL")
            outputStatMode = 1;
        else if (strOutputMode == "JUST_STATS")
            outputStatMode = 2;
        else if (strOutputMode == "ONLY_TIME")
            outputStatMode = 3;
    }

    // Solve the puzzle and time it
    auto start = std::chrono::steady_clock::now();
    SolvePuzzle (puzzleToSolve);
    auto end = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    if (outputStatMode == 0 || outputStatMode == 1)
    {
        std::cout << "Final Solution" << std::endl;
        WriteOutPuzzle (puzzleToSolve);
    }

    if (outputStatMode == 1)
    {
        std::cout << "Solving Time: "      << elapsed.count()   << " microseconds" << std::endl;
        std::cout << "Given Values: "      << nonZeroValues     << std::endl;
        std::cout << "FunctionCallCount: " << FunctionCallCount << std::endl; 
    }
    else if (outputStatMode == 2)
    {
        std::cout << elapsed.count()   << " " 
                  << FunctionCallCount << " " 
                  << nonZeroValues     << std::endl;
    }
    else if (outputStatMode == 3)
    {
        std::cout << elapsed.count() << std::endl;
    }

    return 0;
}




var FunctionCallCount = 0;


//
// FindEmptySpace... returns the location of an empty space
//
function FindEmptySpace (iPuzzle)
{
    for (var nRow = 0; nRow < 9; nRow++)
    {
        for (var nCol = 0; nCol < 9; nCol++)
        {
            if (iPuzzle[nRow][nCol] == 0)
                return [nRow, nCol];
        }
    }

    return [-1, -1];
}


//            
// TestValue... Check to see if a value is possible at a particular location
//
function TestValue (iPuzzle, iLoc, jLoc, iValue)
{
    // first check the row
    for (var j = 0; j < 9; j++)
        if (iPuzzle[iLoc][j] == iValue)
            return false;

    // then check the column
    for (var i = 0; i < 9; i++)
        if (iPuzzle[i][jLoc] == iValue)
            return false;

    // and finally check the region
    var nRegionStartI = 3 * Math.floor (iLoc / 3);
    var nRegionStartJ = 3 * Math.floor (jLoc / 3);
    for (var k = 0; k < 9; k++)
    {
        var i = Math.floor (k / 3);
        var j = k % 3;

        if (iPuzzle[nRegionStartI + i][nRegionStartJ + j] == iValue)
            return false;
    }

    return true;
}


//
// SolvePuzzle: used to recursively solved sudoku puzzles with backtracking
//              Note: puzzles need to be valid 
//
function SolvePuzzle (iPuzzle)
{
    FunctionCallCount ++;

    // Find the location of the first empty space.  If no spaces are empty
    // then the puzzle is solved... so we return true.
    var emptyLoc = FindEmptySpace (iPuzzle) 
    var i = emptyLoc[0];
    var j = emptyLoc[1];
    if (i == -1)
        return true;

    // Test out all the candidate values... 1 to 9
    for (var num = 1; num <= 9; num++)
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



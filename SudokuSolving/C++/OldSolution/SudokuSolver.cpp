//
// Soduku Solver... first test version
//


#include <iostream>
#include <fstream>
#include <string>


#include "Sudoku_Output.h"



using namespace std;


#define EMPTY_SPACE  -1



//
// ReadPuzzle
//
int ReadPuzzle (char * sFilename, int (*pPuzzle)[9][9])
{
    int nRetVal = 0;
    
    if (pPuzzle)
    {
        ifstream inputFile (sFilename);
        
        int i = 0;
        int j = 0;
        int nTemp = 0;
        while (!inputFile.eof() && j < 9)
        {
            inputFile >> nTemp;
            
            if (nTemp >= 1 && nTemp <= 9)
                (*pPuzzle)[i][j] = nTemp;
            else
                (*pPuzzle)[i][j] = EMPTY_SPACE;
            
            i++;
            if (i == 9)
            {
                i = 0;
                j++;
            }
        }
        
        nRetVal = 1;
    }
    
    return nRetVal;
}



//
// CopyPuzzle
//
bool CopyPuzzle (int (*pSrcPuzzle)[9][9], int (*pDestPuzzle)[9][9])
{
    bool bRetVal = false;
    
    if (pSrcPuzzle && pDestPuzzle)
    {
        for (int i = 0; i < 9; i++)
            for (int j = 0; j < 9; j++)
                (*pDestPuzzle)[i][j] = (*pSrcPuzzle)[i][j];
        
        bRetVal = true;
    }
    
    return bRetVal;
}



//
// ZoneToRow
//
int ZoneToRow (int iZone)
{
    return 3 * ((iZone - 1) / 3);
}



//
// ZoneToCol
//
int ZoneToCol (int iZone)
{
    return 3 * ((iZone - 1) % 3);
}



//
// ExistsInZone
//
bool ExistsInZone (int (*pPuzzle)[9][9], int iZone, int iValue)
{
    bool bFound = false;
    
    if (pPuzzle)
    {
        int i_start = ZoneToCol (iZone);
        int j_start = ZoneToRow (iZone);
        
        for (int j = j_start; j < j_start+3; j++)
        {
            for (int i = i_start; i < i_start+3; i++)
            {
                if ((*pPuzzle)[i][j] == iValue)
                {
                    bFound = true;
                    break;
                }
            }
        }
    }
    
    return bFound;
}



//
// DumpPuzzle
//
void DumpPuzzle (int (*pPuzzle)[9][9])
{
    if (pPuzzle)
    {
        for (int j = 0; j < 9; j++)
        {
            for (int i = 0; i < 9; i++)
            {
                cout << (*pPuzzle)[i][j] << " ";
            }
            cout << endl;
        }
    }
}



//
// TestValue
//
bool TestValue (int (*pPuzzle)[9][9], int iZone, int iPosI, int iPosJ)
{
    bool bFound = false;
    
    if (pPuzzle)
    {
        for (int i = 0; i < 9; i++)
        {
            if (i != iPosI && (*pPuzzle)[i][iPosJ] == (*pPuzzle)[iPosI][iPosJ])
            {
                bFound = true;
                break;
            }
        }
        
        if (!bFound)
        {
            for (int j = 0; j < 9; j++)
            {
                if (j != iPosJ && (*pPuzzle)[iPosI][j] == (*pPuzzle)[iPosI][iPosJ])
                {
                    bFound = true;
                    break;
                }
            }
        }
    }
    
    return bFound;
}



//
// SolvePuzzle
//
int SolvePuzzle (int (*pPuzzle)[9][9], int iValue=1, int iZone=1, int iPosition=1)
{
    int nRetValue = 0;

    if (pPuzzle)
    {
        if (ExistsInZone (pPuzzle, iZone, iValue))
        {
            if (iZone < 9)
            {
                return SolvePuzzle (pPuzzle, iValue, iZone+1);
            }
            else if (iValue < 9)
            {
                return SolvePuzzle (pPuzzle, iValue+1, 1);
            }
            else
            {
                //DumpPuzzle(pPuzzle);
                return -1;
            }
        }
        else
        {
            int i_start = ZoneToCol (iZone);
            int j_start = ZoneToRow (iZone);
            
            bool bFailed = true;
            for (int j = j_start; j < j_start+3; j++)
            {
                for (int i = i_start; i < i_start+3; i++)
                {
                    if ((*pPuzzle)[i][j] < 0)
                    {
                        (*pPuzzle)[i][j] = iValue;
                        if (TestValue (pPuzzle, iZone, i, j))
                        {
                            (*pPuzzle)[i][j] = -1;
                        }
                        else
                        {
                            if (iZone < 9)
                            {
                                bFailed = false;
                                
                                nRetValue = SolvePuzzle (pPuzzle, iValue, iZone+1);
                                if (nRetValue > 0)
                                {
                                    (*pPuzzle)[i][j] = -1;
                                }
                                else break;
                            }
                            else if (iValue < 9)
                            {
                                bFailed = false;
                                nRetValue = SolvePuzzle (pPuzzle, iValue+1, 1);
                                if (nRetValue > 0)
                                {
                                    (*pPuzzle)[i][j] = -1;
                                }
                                else break;
                                
                            }
                            else
                            {
                                //DumpPuzzle(pPuzzle);
                                return -1;
                            }
                        }
                        
                    }
                    if (nRetValue < 0) break;
                }
            }
            if (bFailed)
            {
                nRetValue = 1;
            }
        }
    }
 
    return nRetValue;
}


//
// main
//
int main (int argc, char * argv [])
{
    if (argc != 2)
    {
        cout << "Usage : " << argv [0] << " [INPUT_FILE]" << endl;
    }
    else
    {
        int nOrgPuzzle [9][9];
        int (*pOrgPuzzle)[9][9] = &nOrgPuzzle;
        
        // Read in the puzzle file
        ReadPuzzle (argv [1], pOrgPuzzle);
        
        int nSolPuzzle [9][9];
        int (*pSolPuzzle)[9][9] = &nSolPuzzle;
        CopyPuzzle (pOrgPuzzle, pSolPuzzle);
        
        // Solve puzzle
        SolvePuzzle (pSolPuzzle);
        
        // Write out puzzle   
        WriteOutPuzzleTxT (argv [1], pOrgPuzzle, pSolPuzzle);
        WriteOutPuzzlePS (argv [1], pOrgPuzzle, pSolPuzzle);
    }
    
    return 0;
}




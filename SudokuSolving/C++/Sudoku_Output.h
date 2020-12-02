#include <iostream>
#include <fstream>

using namespace std;


#ifndef __SUDUKO_OUTPUT_H__
#define __SUDUKO_OUTPUT_H__


bool WriteOutPuzzleTxT (char * sFilename, int (*pOrgPuzzle)[9][9], int (*pSolPuzzle)[9][9]);
bool WriteOutPuzzlePS (char * sFilename, int (*pOrgPuzzle)[9][9], int (*pSolPuzzle)[9][9]);
bool WriteOutPuzzlePS_Header (ofstream * pOutputFile);
bool WriteOutPuzzlePS_Footer (ofstream * pOutputFile);
bool WriteOutPuzzlePS_PuzzleStart (ofstream * pOutputFile, float iXOffset, float iYOffset, string iPuzzleName);
bool WriteOutPuzzlePS_PuzzleEnd (ofstream * pOutputFile);
bool WriteOutPuzzlePS_Number (ofstream * pOutputFile, int iColumn, int iRow, int iValue);


//
// WriteOutPuzzleTxT
//
bool WriteOutPuzzleTxT (char * sFilename, int (*pOrgPuzzle)[9][9], int (*pSolPuzzle)[9][9])
{
    bool bRetVal = false;

    if (pOrgPuzzle && pSolPuzzle)
    {
        string txtFilename = string (sFilename) + string ("_Solution.txt");
        
        ofstream outputFile (txtFilename);
        
        if (outputFile.is_open())
        {
            outputFile << "       Problem                   Solution\n\n";

            for (int j = 0; j < 9; j++)
            {
                for (int i = 0; i < 9; i++)
                {
                    if ((*pOrgPuzzle)[i][j] < 0)
                        outputFile << "_";
                    else
                        outputFile << (*pOrgPuzzle)[i][j];
                    
                    if (i == 2 || i == 5)
                        outputFile << " |";
                    
                    outputFile << " ";
                }

                outputFile << "    ";
                
                for (int i = 0; i < 9; i++)
                {
                    if ((*pSolPuzzle)[i][j] < 0)
                        outputFile << "_";
                    else
                        outputFile << (*pSolPuzzle)[i][j];
                    
                    if (i == 2 || i == 5)
                        outputFile << " |";
                    
                    outputFile << " ";
                }

                outputFile << "\n";
                
                if (j == 2 || j == 5)
                    outputFile << "------+-------+------     ------+-------+------\n";
            }

            bRetVal = true;
        }
    }

    return bRetVal;
}


//
// WriteOutPuzzlePS
//
bool WriteOutPuzzlePS (char * sFilename, int (*pOrgPuzzle)[9][9], int (*pSolPuzzle)[9][9])
{
    bool bRetVal = false;

    if (pOrgPuzzle && pSolPuzzle)
    {
        string txtFilename = string (sFilename) + string ("_Solution.ps");
        
        ofstream outputFile (txtFilename);
        
        if (outputFile.is_open())
        {
            WriteOutPuzzlePS_Header (&outputFile);

            WriteOutPuzzlePS_PuzzleStart (&outputFile, 2.75, 6.5, "Problem");
            for (int j = 0; j < 9; j++)
            {
                for (int i = 0; i < 9; i++)
                {
                    if ((*pOrgPuzzle)[i][j] > 0)
                        WriteOutPuzzlePS_Number (&outputFile, i, j, (*pOrgPuzzle)[i][j]);
                }
            }            
            WriteOutPuzzlePS_PuzzleEnd (&outputFile);


            WriteOutPuzzlePS_PuzzleStart (&outputFile, 2.75, 1.0, "Solution");
            for (int j = 0; j < 9; j++)
            {
                for (int i = 0; i < 9; i++)
                {
                    if ((*pSolPuzzle)[i][j] > 0)
                        WriteOutPuzzlePS_Number (&outputFile, i, j, (*pSolPuzzle)[i][j]);
                }
            }            
            WriteOutPuzzlePS_PuzzleEnd (&outputFile);

            WriteOutPuzzlePS_Footer (&outputFile);

            bRetVal = true;
        }
    }

    return bRetVal;
}


//
// WriteOutPuzzlePS_Header
//
bool WriteOutPuzzlePS_Header (ofstream * pOutputFile)
{
    bool bRetVal = false;

    if (pOutputFile)
    {
        // Postscript header
        (*pOutputFile) << "%!PS"                 << endl;
        (*pOutputFile)                           << endl;

        // Generic variables
        (*pOutputFile) << "0 setgray"            << endl;
        (*pOutputFile) << "1 setlinewidth"       << endl;
        (*pOutputFile) << "0 setlinecap"         << endl;
        (*pOutputFile) << "/Outline 0 def"       << endl;
        (*pOutputFile)                           << endl;

        // Convert to inches
        (*pOutputFile) << "/inch { 72 mul } def" << endl;
        (*pOutputFile)                           << endl;

        // Function to display center text
        (*pOutputFile) << "/centerShow"          << endl;
        (*pOutputFile) << "{"                    << endl;
        (*pOutputFile) << "   dup"               << endl; 
        (*pOutputFile) << "   gsave"             << endl;
        (*pOutputFile) << "      dup stringwidth pop 2 div neg" << endl;
        (*pOutputFile) << "   grestore"          << endl;
        (*pOutputFile) << "   gsave"             << endl;
        (*pOutputFile) << "      exch true charpath pathbbox exch" << endl;
        (*pOutputFile) << "      pop sub 2 div exch pop" << endl;
        (*pOutputFile) << "   grestore"          << endl;
        (*pOutputFile) << "   rmoveto"           << endl;
        (*pOutputFile) << "   Outline 1 eq"      << endl;
        (*pOutputFile) << "     { true charpath gsave 0.75 setgray fill grestore 0.5 setlinewidth stroke }" << endl;
        (*pOutputFile) << "     { show } ifelse" << endl;
        (*pOutputFile) << "} def"                << endl;
        (*pOutputFile)                           << endl;

        (*pOutputFile) << "/SuBox"               << endl;
        (*pOutputFile) << "{"                    << endl;
        (*pOutputFile) << "    gsave"            << endl;
        (*pOutputFile) << "    0.5 setlinewidth" << endl;
        (*pOutputFile) << "    2 setlinecap"     << endl;
        (*pOutputFile) << "    0 1 9 { gsave 3 div inch 0 moveto 0 3 inch rlineto stroke grestore } for" << endl;
        (*pOutputFile) << "    0 1 9 { gsave 0 exch 3 div inch moveto 3 inch 0 rlineto stroke grestore } for" << endl;
        (*pOutputFile) << "    2 setlinewidth"   << endl; 
        (*pOutputFile) << "    0 1 3 { gsave inch 0 moveto 0 3 inch rlineto stroke grestore } for" << endl;
        (*pOutputFile) << "    0 1 3 { gsave 0 exch inch moveto 3 inch 0 rlineto stroke grestore } for" << endl;
        (*pOutputFile) << "    grestore"         << endl;
        (*pOutputFile) << "} def"                << endl;
        (*pOutputFile)                           << endl;

        (*pOutputFile) << "/SuMoveto"            << endl;
        (*pOutputFile) << "{"                    << endl;
        (*pOutputFile) << "    exch 2 mul -1 add 6 div inch  exch 2 mul -1 add 6 div -1 mul 3 add inch moveto" << endl;
        (*pOutputFile) << "} def"                << endl;
        (*pOutputFile)                           << endl;

        bRetVal = true;
    }

    return bRetVal;
}


//
// WriteOutPuzzlePS_Footer
//
bool WriteOutPuzzlePS_Footer (ofstream * pOutputFile)
{
    bool bRetVal = false;

    if (pOutputFile)
    {
        (*pOutputFile) << "showpage" << endl;

        bRetVal = true;
    }

    return bRetVal;
}


//
// WriteOutPuzzlePS_PuzzleStart
//
bool WriteOutPuzzlePS_PuzzleStart (ofstream * pOutputFile, float iXOffset, float iYOffset, string iPuzzleName)
{
    bool bRetVal = false;

    if (pOutputFile)
    {
        (*pOutputFile) << "gsave"              << endl;
        (*pOutputFile) << "   " << iXOffset << " inch " << iYOffset << " inch translate" << endl;
        (*pOutputFile) << "   SuBox"              << endl;
        (*pOutputFile) << "   /Helvetica-Bold findfont 15 scalefont setfont" << endl;
        (*pOutputFile) << "   0 3.15 inch moveto" << endl;
        (*pOutputFile) << "(" << iPuzzleName << ") show" << endl;
        (*pOutputFile) << "0 0 moveto"         << endl;

        bRetVal = true;
    }

    return bRetVal;
}


//
// WriteOutPuzzlePS_PuzzleEnd
//
bool WriteOutPuzzlePS_PuzzleEnd (ofstream * pOutputFile)
{
    bool bRetVal = false;

    if (pOutputFile)
    {
        (*pOutputFile) << "grestore"           << endl;

        bRetVal = true;
    }

    return bRetVal;
}


//
// WriteOutPuzzlePS_Number
//
bool WriteOutPuzzlePS_Number (ofstream * pOutputFile, int iColumn, int iRow, int iValue)
{
    bool bRetVal = false;

    if (pOutputFile)
    {
        (*pOutputFile) << iColumn+1 << " " << iRow+1 << " SuMoveto" << endl;
        (*pOutputFile) << " (" << iValue << ") centerShow" << endl;

        bRetVal = true;
    }

    return bRetVal;
}


#endif //__SUDUKO_OUTPUT_H__




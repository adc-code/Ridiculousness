#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>


using namespace std;


float  FOOT   = 12.0;

float  LENGTH = 12 / FOOT;
float  WIDTH  =  1.5 / FOOT;


struct Point
{
    float x, y;
};


struct Element
{
    Point corners [4];   
};


void  MakeElement (float xOffset, float yOffset, int type, Element & newElement)
{
    if (type == 1)
    {
        newElement.corners[0].x = xOffset;
        newElement.corners[0].y = yOffset;

        newElement.corners[1].x = -WIDTH * M_SQRT1_2;
        newElement.corners[1].y =  WIDTH * M_SQRT1_2;

        newElement.corners[2].x = LENGTH * M_SQRT1_2;
        newElement.corners[2].y = LENGTH * M_SQRT1_2;

        newElement.corners[3].x =  WIDTH * M_SQRT1_2;
        newElement.corners[3].y = -WIDTH * M_SQRT1_2;
    }
    else if (type == 2)
    {
        newElement.corners[0].x = xOffset;
        newElement.corners[0].y = yOffset;

        newElement.corners[1].x =  WIDTH * M_SQRT1_2;
        newElement.corners[1].y =  WIDTH * M_SQRT1_2;

        newElement.corners[2].x =  LENGTH * M_SQRT1_2;
        newElement.corners[2].y = -LENGTH * M_SQRT1_2;

        newElement.corners[3].x = -WIDTH * M_SQRT1_2;
        newElement.corners[3].y = -WIDTH * M_SQRT1_2;
    }
}


void WriteOutElem (ofstream & oStr, Element & elem)
{
    oStr << "gsave"               << endl;
    oStr << "0 setlinewidth"      << endl;
    oStr << elem.corners[0].x << " inch " << elem.corners[0].y << " inch  moveto" << endl;
    oStr << elem.corners[1].x << " inch " << elem.corners[1].y << " inch rlineto" << endl;
    oStr << elem.corners[2].x << " inch " << elem.corners[2].y << " inch rlineto" << endl;
    oStr << elem.corners[3].x << " inch " << elem.corners[3].y << " inch rlineto" << endl;
    oStr << "closepath"           << endl;
    oStr << "stroke"              << endl;
    oStr << "grestore"            << endl;
}


int main (int argc, char * argv [])
{
    ofstream  outfile;
    outfile.open ("design.ps");

    outfile << "%!PS "    << endl; 
    outfile <<               endl;

    outfile << "/inch { 72 mul } def" << endl;

    outfile << "3 inch 2.5 inch translate" << endl;
    outfile << "gsave"               << endl;
    outfile << "0 0 moveto"          << endl;
    outfile << "2 setlinewidth"      << endl;
    outfile << "1 0 0 setrgbcolor"   << endl;
    outfile << "2.5 inch 0 rlineto"  << endl;
    outfile << "0 6 inch rlineto"    << endl;
    outfile << "-2.5 inch 0 rlineto" << endl;
    outfile << "closepath"           << endl;
    outfile << "stroke"              << endl;
    outfile << "1.25 inch -0.25 inch moveto"  << endl;
    outfile << "1 setlinewidth"      << endl;
    outfile << "0 6.5 inch rlineto"  << endl;
    outfile << "stroke"              << endl;
    outfile << "grestore"            << endl;


    float xOffset = -WIDTH;
    float yOffset = 0;
    for (int i = -5; i < 34; i++)
    {
        Element newElem;

        //MakeElement (xOffset - LENGTH*M_SQRT1_2 - WIDTH*M_SQRT1_2, 
        //             yOffset + LENGTH*M_SQRT1_2 + WIDTH*M_SQRT1_2 + i*WIDTH*M_SQRT2, 2, newElem);
        //WriteOutElem (outfile, newElem);   

        MakeElement (xOffset, 
                     yOffset + i*WIDTH*M_SQRT2, 1, newElem);
        WriteOutElem (outfile, newElem);   

        MakeElement (xOffset + LENGTH*M_SQRT1_2 - WIDTH*M_SQRT1_2, 
                     yOffset + LENGTH*M_SQRT1_2 + WIDTH*M_SQRT1_2 + i*WIDTH*M_SQRT2, 2, newElem);
        WriteOutElem (outfile, newElem);   

        MakeElement (xOffset + LENGTH*M_SQRT2, 
                     yOffset + i*WIDTH*M_SQRT2, 1, newElem);
        WriteOutElem (outfile, newElem);   

        MakeElement (xOffset + LENGTH*M_SQRT2 + LENGTH*M_SQRT1_2 - WIDTH*M_SQRT1_2, 
                     yOffset + LENGTH*M_SQRT1_2 + WIDTH*M_SQRT1_2 + i*WIDTH*M_SQRT2, 2, newElem);
        WriteOutElem (outfile, newElem);   

    }


    outfile << "showpage" << endl; 
   
    outfile.close ();

    return 0;
}



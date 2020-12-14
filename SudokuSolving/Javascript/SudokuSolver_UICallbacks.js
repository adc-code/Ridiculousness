//
// OnMouseEnter: when mouse enters a cell
//
function OnMouseEnter (event)
{
    if (event.target != currSelCell && event.target.getAttribute ('CellState') != 'error')
    {
        event.target.style.backgroundColor = preselectedColour;
    }
}


//
// OnMouseLeave: when mouse leaves a cell
//            
function OnMouseLeave (event)
{
    if (event.target != currSelCell && event.target.getAttribute ('CellState') != 'error')
    {
        event.target.style.backgroundColor = event.target.getAttribute ('OriginalBGColour');
    }
}
      

//
// OnClick: when user clicks on a cell
//
function OnClick (event)
{
    if (currSelCell == null)
    {
        currSelCell = event.target;
        event.target.style.backgroundColor = selectedColour;
        event.target.style.color = givenColour;
    }
    else
    {
        if (event.target == currSelCell)
        {
            if (currSelCell.getAttribute ('CellState') == 'error')
                event.target.style.backgroundColor = currSelCell.getAttribute ('ErrorBGColour');
            else
                event.target.style.backgroundColor = currSelCell.getAttribute ('OriginalBGColour');

            currSelCell = null;
        }
        else
        {
            if (currSelCell.getAttribute ('CellState') == 'error')
                currSelCell.style.backgroundColor = currSelCell.getAttribute ('ErrorBGColour');
            else
                currSelCell.style.backgroundColor = currSelCell.getAttribute ('OriginalBGColour');

            event.target.style.backgroundColor = selectedColour;
            currSelCell = event.target;
        }  
    }
}


//
// OnSolveButton: when the solve button is clicked
//
function OnSolveButton (event)
{
    if (errorsExist)
    {
        var originalMsg = document.getElementById ('Info').innerHTML;
        document.getElementById ('Info').innerHTML = 'Cannot solve since errors exist!!!' 
                                                     + '<br><br>'         
                                                     + originalMsg;
        return;
    }

    var puzzle = [];

    // read in puzzle...
    for (var i = 1; i <= 9; i++)
    {
        var row = [];
        for (var j = 1; j <= 9; j++)
        {
            var value = document.getElementById ('b' + i + j).innerText;
            if (value == '' || value == ' ')
                row.push (0);
            else
                row.push (+value);
        }
        puzzle.push (row);
    }

    const t0 = performance.now();
    SolvePuzzle (puzzle); 
    const t1 = performance.now();

    for (var i = 0; i < 9; i++)
    {
        for (var j = 0; j < 9; j++)
        {
            var cell = document.getElementById ('b' + (i+1) + (j+1));
            cell.innerText = puzzle[i][j];
            if (cell.getAttribute ('CellState') == 'given')
                cell.style.color = givenColour;
            else
                cell.style.color = solvedColour;
        }
    }

    document.getElementById ('Info').innerHTML = 'Time to Solve: <br>' + 
                                                 (t1 - t0).toFixed(3) + ' milliseconds' +
                                                 '<br><br>' +
                                                 'Number of Iterations: <br>' +
                                                 FunctionCallCount;
}


//
// OnResetButton... deal with the reset button
//
function OnResetButton (event)
{
    var puzzle = [];
    FunctionCallCount = 0;
    document.getElementById ('Info').innerHTML = '';
    errorsExist = false;

    for (var i = 1; i <= 9; i++)
    {
        for (var j = 1; j <= 9; j++)
        {
            var cell = document.getElementById ('b' + i + j);

            cell.innerText = '';
            cell.style.backgroundColor = cell.getAttribute ('OriginalBGColour'); 
            cell.setAttribute ('CellState', 'normal');
        }
    } 

    currSelCell = null; 
}


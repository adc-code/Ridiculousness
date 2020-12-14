//
// checkErrors
//
function checkErrors (value)
{
    var errorMessage = '';

    if (checkErrorsRow (value))
        errorMessage = 'Error: Same values in row ' + currSelCell.id [1];

    if (checkErrorsCol (value))
    {
        if (errorMessage.length > 0)
            errorMessage += '<br><br>';

        errorMessage += 'Error: Same values in column ' + currSelCell.id [2];
    }

    if (checkErrorsZone (value))
    {
        if (errorMessage.length > 0)
            errorMessage += '<br><br>';

        errorMessage += 'Error: Same values in zone ' + currSelCell.getAttribute ('zone');
    }

    document.getElementById ('Info').innerHTML = errorMessage;

    if (errorMessage.length == 0)
    {
        errorsExist = false;
        return true;
    }
    else
    {
        errorsExist = true;
        return false;
    }
}


//
// checkErrorsRow... check for errors within a row
//
function checkErrorsRow (value)
{
    var error = false;

    var currRow = currSelCell.id [1];
    var currCol = currSelCell.id [2];

    // check row
    var isSame = false;
    var sameVal = -1; 
    for (var i = 0; i < 9; i++)
    {
        if ( (i+1) == currCol )
            continue;

        if (document.getElementById ('b' + currRow + (i+1)).innerText == value)
        {
            isSame = true;
            sameVal = i;
            break;
        }
    }

    if (isSame)
    {
        for (var i = 0; i < 9; i++)
        {
            var errorColour = sameBgColour;
            if ( i == sameVal || (i+1) == currCol )
                errorColour = sameValueColour;
                        
            document.getElementById ('b' + currRow + (i+1)).style.backgroundColor = errorColour;
            document.getElementById ('b' + currRow + (i+1)).setAttribute ('ErrorBGColour', errorColour);
            document.getElementById ('b' + currRow + (i+1)).setAttribute ('CellState', 'error');
        }

        currSelCell.style.backgroundColor = selectedColour; 
        error = true;
    }

    return error;
}


//
// checkErrorsCol... check errors by column
//
function checkErrorsCol (value)
{
    var error = false;

    var currRow = currSelCell.id [1];
    var currCol = currSelCell.id [2];

    // check col
    var isSame  = false;
    var sameVal = -1; 
    for (var i = 0; i < 9; i++)
    {
        if ( (i+1) == currRow )
            continue;

        if (document.getElementById ('b' + (i+1) + currCol).innerText == value)
        {
            isSame = true;
            sameVal = i;
            break;
        }
    }

    if (isSame)
    {
        for (var i = 0; i < 9; i++)
        {
            var errorColour = sameBgColour;
            if ( i == sameVal || (i+1) == currRow )
                errorColour = sameValueColour;
                        
            document.getElementById ('b' + (i+1) + currCol).style.backgroundColor = errorColour;
            document.getElementById ('b' + (i+1) + currCol).setAttribute ('ErrorBGColour', errorColour);
            document.getElementById ('b' + (i+1) + currCol).setAttribute ('CellState', 'error');
        }
        currSelCell.style.backgroundColor = selectedColour; 

        error = true;
    }

    return error;
}


//
// checkErrorsZone... check errors within a zone/region
//
function checkErrorsZone (value)
{
    var error = false;

    var currRow  = currSelCell.id [1];
    var currCol  = currSelCell.id [2];
    var currZone = currSelCell.getAttribute ('zone');

    var isSame  = false;
    var sameValI = -1;
    var sameValJ = -1;
    var allCells = document.getElementsByClassName ('cell');
    for (var i = 0; i < allCells.length; i++)
    {
        var zone = allCells[i].getAttribute ('zone');
        if (zone == currZone)
        {
            if (allCells[i].id[1] == currRow && allCells[i].id[2] == currCol)
                continue;

            if (allCells[i].innerText == value)
            {
                isSame = true;
                sameValI = allCells[i].id[1];
                sameValJ = allCells[i].id[2];
                break;
            }
        }
    }

    if (isSame)
    {
        for (var i = 0; i < allCells.length; i++)
        {
            var zone = allCells[i].getAttribute ('zone');
            if (zone == currZone)
            {
                var errorColour = sameBgColour;
                if ( (allCells[i].id[1] == currRow  && allCells[i].id[2] == currCol) ||
                     (allCells[i].id[1] == sameValI && allCells[i].id[2] == sameValJ) )
                {
                    errorColour = sameValueColour;
                }
                            
                allCells[i].style.backgroundColor = errorColour;
                allCells[i].setAttribute ('ErrorBGColour', errorColour);
                allCells[i].setAttribute ('CellState', 'error');
            }
        }
        currSelCell.style.backgroundColor = selectedColour; 

        error = true;
    } 

    return error;
}



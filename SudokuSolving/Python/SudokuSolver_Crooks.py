# 
# SudokuSolver_Crooks.py... sudoku solver that uses 'Crooks' algorithm.  Original taken from 
# github and has been modified to have a similar command line interface as the other implementations.
# Also it was modified so that inputs and outputs are similar to other programs.
#
# Usage: > python SudokuSolver_Crooks.py  <TestFile>  [TestStats]
#
# Where: <TestFile>: the file containing the puzzle
#        [TestStats]: optional parameter to output stats; note if not present only solution is printed
#          -> FULL_SOL: output solution with timing and iteration values
#          -> JUST_STATS: output only timing and iteration values
#          -> ONLY_TIME: output only timing value
#


# Copyright (C) 2019 Daniel Opdahl (dopdahl16@gmail.com) Some Rights Reserved. 
# Permission to copy and modify is granted under the GNU General Public License v3.0 license
# Last revised 10/7/2019

# TODO: Use f-string for output
# TODO: Implement solving for puzzles that require random choice. Essentially, finish the project!
# TODO: Tell someone you love that you love them today :) 

import copy
import sys
import time


class Cell:
    def __init__(self, cell_row, cell_col, cell_box, cell_val):
        self.row = cell_row
        self.col = cell_col
        self.box = cell_box
        self.val = cell_val
    def getRow(self):
        return self.row
    def getCol(self):
        return self.col
    def getBox(self):
        return self.box
    def getVal(self):
        return self.val
    def setRow(self, new_row):
        self.row = new_row
    def setCol(self, new_col):
        self.col = new_col
    def setBox(self, new_box):
        self.box = new_box
    def setVal(self, new_val):
        self.val = new_val
    def __str__(self):
        cors_val = [self.row, self.col, self.box, self.val]
        return_str = str(cors_val)
        return return_str
    def __repr__(self):
        cors_val = [self.row, self.col, self.box, self.val]
        return_str = str(cors_val)
        return return_str

# Since I have the coordinates baked into each Cell oject, maybe I should subclass Matrix as a set... Faster lookups? The order that the list provides doesn't really matter... Do I ever have to iterate through a matrix object?
class Matrix(list):
    
    # For the methods resolveValue, preemptiveSolve, reduceMarkup, forceCells, rewrite. Each group goes through the same steps... so just generalize those steps!!!!!
    
    def __init__(self, cells_list=[]):
        self.cells = cells_list
        
    def setCells(self, cells_list):
        
        # The commented code below type checks the inputted cells_list, but I've opted not to employ it. It feels more "Pythonic" 
        # to use duck typing here. (see: https://en.wikipedia.org/wiki/Duck_typing)
        '''
        if not isinstance(cells_list, list):
            raise TypeError("Matrix objects only accept lists of Cell objects for method setCells")
        for cell in cells_list:
            if not isinstance(cell, Cell):
                raise TypeError("Matrix objects only accept lists of Cell objects for method setCells")
        '''
        
        self.cells = cells_list
        
    def getCells(self):
        return self.cells
    
    def getColumnGroup(self, column_number):
        column_group = []
        for cell in self.getCells():
            if cell.getCol() == column_number:
                column_group.append(cell)
        if len(column_group) != 9:
            raise BaseException("Something broke. Contact a developer ASAP!")
        return column_group
    
    def getRowGroup(self, row_number):
        row_group = []
        for cell in self.getCells():
            if cell.getRow() == row_number:
                row_group.append(cell)
        if len(row_group) != 9:
            raise BaseException("Something broke. Contact a developer ASAP!")
        return row_group
    
    def getBoxGroup(self, box_number):
        box_group = []
        for cell in self.getCells():
            if cell.getBox() == box_number:
                box_group.append(cell)
        if len(box_group) != 9:
            raise BaseException("Something broke. Contact a developer ASAP!")
        return box_group
    
    def markup(self):
        for cell in self.getCells():
            #if cell.getVal() == 'x':
            if cell.getVal() == '_':
                cell.setVal(set([1, 2, 3, 4, 5, 6, 7, 8, 9]))
                

    # There are too many for loops in reduceMarkup, but is there a way to reduce how many we have to use?  
    # Can we scan for numbers to be removed in a group while simultaneously remove the numbes that need to 
    # be removed from the markedup sets? I'm doubtful.  I believe the way I have my for loops set up is 
    # optimized for more difficult puzzles.  If we are dealing with puzzles that give us more numbers to 
    # start out with (easier puzzles), then I think the more optimal way would be to scan each group (row, 
    # column, box), only make a list of the numbers that need to be removed from that group, then go through 
    # again and remove the numbers that need to be removed from the markedup cells.  I think the way I do it 
    # below is faster for harder puzzles because we have to iterate through fewer total things, even if we 
    # have to create an extra list
    def reduceMarkup (self):
        change_made = True
        while change_made == True:
            change_made = False
            for row_number in range(1,10,1):
                numbers_to_remove_from_marked_up_cells = set()
                marked_up_cells = []
                for cell in self.getRowGroup(row_number):
                    if isinstance(cell.getVal(), str):
                        numbers_to_remove_from_marked_up_cells.add(int(cell.getVal()))
                    elif isinstance(cell.getVal(), set):
                        if len(cell.getVal()) == 1:
                            cell.setVal(str(cell.getVal().pop()))
                        else:
                            marked_up_cells.append(cell)
                    else:
                        raise BaseException("Something broke. Contact a developer ASAP!")
                for cell in marked_up_cells:
                    if len(cell.getVal().difference(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))) != 0:
                        cell.setVal(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))
                        change_made = True
            for column_number in range(1,10,1):
                numbers_to_remove_from_marked_up_cells = set()
                marked_up_cells = []
                for cell in self.getColumnGroup(column_number):
                    if isinstance(cell.getVal(), str):
                        numbers_to_remove_from_marked_up_cells.add(int(cell.getVal()))
                    elif isinstance(cell.getVal(), set):
                        if len(cell.getVal()) == 1:
                            cell.setVal(str(cell.getVal().pop()))
                        else:
                            marked_up_cells.append(cell)
                    else:
                        raise BaseException("Something broke. Contact a developer ASAP!")
                for cell in marked_up_cells:
                    if len(cell.getVal().difference(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))) != 0:
                        cell.setVal(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))
                        change_made = True
            for box_number in range(1,10,1):
                numbers_to_remove_from_marked_up_cells = set()
                marked_up_cells = []
                for cell in self.getBoxGroup(box_number):
                    if isinstance(cell.getVal(), str):
                        numbers_to_remove_from_marked_up_cells.add(int(cell.getVal()))
                    elif isinstance(cell.getVal(), set):
                        if len(cell.getVal()) == 1:
                            cell.setVal(str(cell.getVal().pop()))
                        else:
                            marked_up_cells.append(cell)
                    else:
                        raise BaseException("Something broke. Contact a developer ASAP!")
                for cell in marked_up_cells:
                    if len(cell.getVal().difference(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))) != 0:
                        cell.setVal(cell.getVal().difference(numbers_to_remove_from_marked_up_cells))
                        change_made = True
        self.checkSolved()
        
    # This step follows from the instructions on page 463 of Crook's paper, reading, "The method proceeds by 
    # finding a box that is missing this high-frequency number and determining whether there is one and only 
    # one cell into which this number can be entered." If reduceMarkup is called before this, then this method 
    # will accomplish what Crook describes here.
    # It is worth noting that this step is, regrettably, for loop intensive
    def forceCells(self):
        change_made = True
        while change_made == True:
            change_made = False        
            for row_number in range(1,10,1):
                for reference_cell in self.getRowGroup(row_number):
                    if not isinstance(reference_cell.getVal(), str):
                        reference_cell_value = reference_cell.getVal()
                        number_appearance_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
                        for comparison_cell in self.getRowGroup(row_number):
                            if isinstance(comparison_cell.getVal(), str):
                                comparison_cell_value = set([int(comparison_cell.getVal())])
                            else:
                                comparison_cell_value = comparison_cell.getVal()
                            difference_set = reference_cell_value.difference(comparison_cell_value)
                            for value in difference_set:
                                number_appearance_dict[int(value)] = number_appearance_dict[int(value)] + 1
                                if number_appearance_dict[int(value)] == 8:
                                    self.resolveValue(reference_cell, value)
                                    change_made = True
            for column_number in range(1,10,1):
                for reference_cell in self.getColumnGroup(column_number):
                    if not isinstance(reference_cell.getVal(), str):
                        reference_cell_value = reference_cell.getVal()
                        number_appearance_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
                        for comparison_cell in self.getColumnGroup(column_number):
                            if isinstance(comparison_cell.getVal(), str):
                                comparison_cell_value = set([int(comparison_cell.getVal())])
                            else:
                                comparison_cell_value = comparison_cell.getVal()
                            difference_set = reference_cell_value.difference(comparison_cell_value)
                            for value in difference_set:
                                number_appearance_dict[int(value)] = number_appearance_dict[int(value)] + 1
                                if number_appearance_dict[int(value)] == 8:
                                    self.resolveValue(reference_cell, value)
                                    change_made = True
            for box_number in range(1,10,1):
                for reference_cell in self.getBoxGroup(box_number):
                    if not isinstance(reference_cell.getVal(), str):
                        reference_cell_value = reference_cell.getVal()
                        number_appearance_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
                        for comparison_cell in self.getBoxGroup(box_number):
                            if isinstance(comparison_cell.getVal(), str):
                                comparison_cell_value = set([int(comparison_cell.getVal())])
                            else:
                                comparison_cell_value = comparison_cell.getVal()
                            difference_set = reference_cell_value.difference(comparison_cell_value)
                            for value in difference_set:
                                number_appearance_dict[int(value)] = number_appearance_dict[int(value)] + 1
                                if number_appearance_dict[int(value)] == 8:
                                    self.resolveValue(reference_cell, value)
                                    change_made = True
        self.checkSolved()
        
    # The below is my implmentation of Crook's algorithm described under the heading "An Algorithm for Solving Sudoku Puzzles" on pages 463 & 464
    def preemptiveSolve(self):
        change_made = True
        while change_made == True:
            change_made = False
            for row_number in range(1,10,1):
                unresolved_cells_row_group = []
                master_list_of_all_unions = []
                for cell in self.getRowGroup(row_number):
                    if not isinstance(cell.getVal(), str):
                        unresolved_cells_row_group.append(cell)
                master_list_of_all_unions = findNLevelUnions(unresolved_cells_row_group, master_list_of_all_unions)
                if master_list_of_all_unions == None:
                    master_list_of_all_unions = []                        
                for union in master_list_of_all_unions:
                    if not len(union) == len(unresolved_cells_row_group):
                        list_of_cells_that_are_subsets_of_union = []
                        for cell in unresolved_cells_row_group:
                            if cell.getVal().issubset(union) or cell.getVal() == union:
                                list_of_cells_that_are_subsets_of_union.append(cell)
                        list_of_cells_that_are_NOT_subsets_of_union = list(set(unresolved_cells_row_group).difference(set(list_of_cells_that_are_subsets_of_union)))
                        if len(union) == len(list_of_cells_that_are_subsets_of_union):
                            for number in union:
                                for cell in self.getRowGroup(row_number):
                                    if isinstance(cell.getVal(), set):
                                        if cell in list_of_cells_that_are_NOT_subsets_of_union:
                                            if number in cell.getVal():
                                                cell.getVal().remove(number)
                                                if len(cell.getVal()) == 1:
                                                    self.resolveValue(cell, cell.getVal().pop())
                                                    cells_to_be_removed = []
                                                    for unresolved_cell in unresolved_cells_row_group:
                                                        if len(unresolved_cell.getVal()) == 1:                                                       
                                                            cells_to_be_removed.append(unresolved_cell)
                                                    for cell_to_be_removed in cells_to_be_removed:
                                                        if cell_to_be_removed in unresolved_cells_row_group:
                                                            unresolved_cells_row_group.remove(cell_to_be_removed)                                                    
                                                change_made = True
            for column_number in range(1,10,1):
                unresolved_cells_col_group = []
                master_list_of_all_unions = []
                for cell in self.getColumnGroup(column_number):
                    if not isinstance(cell.getVal(), str):
                        unresolved_cells_col_group.append(cell)
                master_list_of_all_unions = findNLevelUnions(unresolved_cells_col_group, master_list_of_all_unions)
                if master_list_of_all_unions == None:
                    master_list_of_all_unions = []
                for union in master_list_of_all_unions:
                    if not len(union) == len(unresolved_cells_col_group):
                        list_of_cells_that_are_subsets_of_union = []
                        for cell in unresolved_cells_col_group:
                            if cell.getVal().issubset(union) or cell.getVal() == union:
                                list_of_cells_that_are_subsets_of_union.append(cell)
                        list_of_cells_that_are_NOT_subsets_of_union = list(set(unresolved_cells_col_group).difference(set(list_of_cells_that_are_subsets_of_union)))
                        if len(union) == len(list_of_cells_that_are_subsets_of_union):
                            for number in union:
                                for cell in self.getColumnGroup(column_number):
                                    if isinstance(cell.getVal(), set):
                                        if cell in list_of_cells_that_are_NOT_subsets_of_union:
                                            if number in cell.getVal():
                                                cell.getVal().remove(number)                                             
                                                if len(cell.getVal()) == 1:
                                                    self.resolveValue(cell, cell.getVal().pop())
                                                    cells_to_be_removed = []
                                                    for unresolved_cell in unresolved_cells_col_group:
                                                        if len(unresolved_cell.getVal()) == 1:                                                       
                                                            cells_to_be_removed.append(unresolved_cell)
                                                    for cell_to_be_removed in cells_to_be_removed:
                                                        if cell_to_be_removed in unresolved_cells_col_group:
                                                            unresolved_cells_col_group.remove(cell_to_be_removed)
                                                change_made = True
                                                
            for box_number in range(1,10,1):
                unresolved_cells_box_group = []
                master_list_of_all_unions = []
                for cell in self.getBoxGroup(box_number):
                    if not isinstance(cell.getVal(), str):
                        unresolved_cells_box_group.append(cell)
                master_list_of_all_unions = findNLevelUnions(unresolved_cells_box_group, master_list_of_all_unions)
                if master_list_of_all_unions == None:
                    master_list_of_all_unions = []                        
                for union in master_list_of_all_unions:
                    if not len(union) == len(unresolved_cells_box_group):
                        list_of_cells_that_are_subsets_of_union = []
                        for cell in unresolved_cells_box_group:
                            if cell.getVal().issubset(union) or cell.getVal() == union:
                                list_of_cells_that_are_subsets_of_union.append(cell)
                        list_of_cells_that_are_NOT_subsets_of_union = list(set(unresolved_cells_box_group).difference(set(list_of_cells_that_are_subsets_of_union)))
                        if len(union) == len(list_of_cells_that_are_subsets_of_union):
                            for number in union:
                                for cell in self.getBoxGroup(box_number):
                                    if isinstance(cell.getVal(), set):
                                        if cell in list_of_cells_that_are_NOT_subsets_of_union:
                                            if number in cell.getVal():
                                                cell.getVal().remove(number)
                                                if len(cell.getVal()) == 1:
                                                    self.resolveValue(cell, cell.getVal().pop())
                                                    cells_to_be_removed = []
                                                    for unresolved_cell in unresolved_cells_box_group:
                                                        if len(unresolved_cell.getVal()) == 1:                                                       
                                                            cells_to_be_removed.append(unresolved_cell)
                                                    for cell_to_be_removed in cells_to_be_removed:
                                                        if cell_to_be_removed in unresolved_cells_box_group:
                                                            unresolved_cells_box_group.remove(cell_to_be_removed)
                                                change_made = True
        self.checkSolved()            
        
    # When a value of a cell is determined, that value should be removed from the column, row, and box 
    # that the cell belongs to. For example, if I determine that a 5 belongs in the cell at [7, 2, 7], I 
    # must set the value of that cell to '5', but I must also remove 5 from the options for all the other 
    # cells in the 7th row, the 2nd column, and the 7th block.
    def resolveValue(self, cell_to_be_value_updated, cell_value):
        cell_to_be_value_updated.setVal(str(cell_value))
        for cell in self.getRowGroup(cell_to_be_value_updated.getRow()):
            if isinstance(cell.getVal(), set):
                if cell_value in cell.getVal():
                    cell.getVal().remove(cell_value) # probably should use setVal for this... and make it so that you can't modify cells value through a getVal call
                if len(cell.getVal()) == 1:
                    self.resolveValue(cell, cell.getVal().pop())
        for cell in self.getColumnGroup(cell_to_be_value_updated.getCol()):
            if isinstance(cell.getVal(), set):
                if cell_value in cell.getVal():
                    cell.getVal().remove(cell_value)
                if len(cell.getVal()) == 1:
                    self.resolveValue(cell, cell.getVal().pop())
        for cell in self.getBoxGroup(cell_to_be_value_updated.getBox()):
            if isinstance(cell.getVal(), set):
                if cell_value in cell.getVal():
                    cell.getVal().remove(cell_value)
                if len(cell.getVal()) == 1:
                    self.resolveValue(cell, cell.getVal().pop())
                    
    def checkSolved (self):
        for cell in self.getCells():
            if isinstance(cell.getVal(), set):
                return
        # print("SOLVED")
        # print (self)
        # quit()
            
            
    # Write a method to check validity of puzzle inputted
    
        
    def __str__(self):
        return_str = '' #"-----------------\n"
        for cell in self.getCells():
            
            ### Pretty output:
            if not isinstance(cell.getVal(), str):
                return_str = return_str + "_" + " "
            else:
                return_str = return_str + str(cell.getVal()) + " "

            if cell.getCol() == 3 or cell.getCol() == 6:
                return_str += '| '
            
            ### Functional output:
            #return_str = return_str + str(cell.getVal()) + " "
            
            if cell.getCol() == 9:
                return_str = return_str + '\n'
              
                if cell.getRow() == 3 or cell.getRow() == 6:
                    return_str += '------+-------+-------\n'

        # return_str = return_str + "-----------------"
        return return_str

    def __repr__(self):
        return_str = ""
        for cell in self.getCells():
            return_str = return_str + cell.getVal() + " "
            if cell.getCol() == 9:
                return_str = return_str + '\n'
        return return_str    
            
            
def constructCellList (puzzle):

    ordered_cell_list = []
    cell_count = 0
    for cell_starting_val in puzzle:
        row = (cell_count // 9) + 1
        column = (cell_count % 9) + 1
        box = (((column - 1) // 3) + 1) + (((row - 1) // 3) * 3)
        ordered_cell_list.append(Cell(row, column, box, cell_starting_val))
        cell_count += 1

    return ordered_cell_list

        
def openPuzzle (iFileName):
    matrix = []
    ask_for_input = True
    #while ask_for_input:
    #    user_input = input("Please enter the path to a Sudoku puzzle file: ")
    #    try:
    #        file = open(user_input, "r")
    #        ask_for_input = False
    #    except IOError:
    #        print("No such file name. Please input a valid path and filename.")

    try:
        file = open (iFileName, 'r')
    except IOError:
        print ('No such file name. Please input a valid path and filename.')

    matrix = file.read ()

    #print("Solving this puzzle \n-----------------")
    #print(matrix)
    #print("-----------------") 

    matrix = matrix.split ()

    return matrix


def CountNonZeroValues (iPuzzleValues):

    nCount = 0
    for value in iPuzzleValues:
        if value != '_':
            nCount += 1

    return nCount


def findNLevelUnions(my_list_of_unresolved_group_cells, master_list_of_all_unions):
    running_union = set()
    for cell in my_list_of_unresolved_group_cells:
        running_union = running_union.union(cell.getVal())
    # This is a hackey way to avoid having to search through the list in a for loop, but I just learned that .index() is O(n) complexity, the same as a loop. Essentially, O(n) searches through the list iteratively, which I could do with a for loop. I should probably change this, but I'm a little salty at myself right now
    val_is_in_list = True
    try:
        master_list_of_all_unions.index(running_union)
    except:
        val_is_in_list = False
    if not val_is_in_list:
        master_list_of_all_unions.append(running_union)
    for unresolved_cell in my_list_of_unresolved_group_cells:
        insertion_index = my_list_of_unresolved_group_cells.index(unresolved_cell)
        my_list_of_unresolved_group_cells.remove(unresolved_cell)
        working_list = copy.copy(my_list_of_unresolved_group_cells)
        if len(working_list) == 1:
            return
        findNLevelUnions(working_list, master_list_of_all_unions)
        my_list_of_unresolved_group_cells.insert(insertion_index, unresolved_cell)
    return master_list_of_all_unions


if __name__ == "__main__":
    
    if len(sys.argv) < 2 or len(sys.argv) > 3:

        print ('Error: incorrect number of parameters!')
        print ('Usage: ' + sys.argv[0] + ' <TestFile>  [TestStats]')
        print ()
        print ('<TestFile>: the file containing the puzzle')
        print ('[TestStats]: optional parameter to output stats; note if not present only solution is printed')
        print ('   -> FULL_SOL: output solution with timing and iteration values')
        print ('   -> JUST_STATS: output only timing and iteration values')
        print ('   -> ONLY_TIME: output only timing value')
        sys.exit ();

    # Output stats...
    outputStatMode = 0
    if len(sys.argv) == 3:
        if sys.argv[2] == 'FULL_SOL':
            outputStatMode = 1
        elif sys.argv[2] == 'JUST_STATS':
            outputStatMode = 2
        elif sys.argv[2] == 'ONLY_TIME':
            outputStatMode = 3


    puzzle = openPuzzle (sys.argv[1])
    #print (puzzle)
    numGivenValues = CountNonZeroValues (puzzle)

    ordered_cell_list = constructCellList (puzzle)
    my_matrix = Matrix()
    tic = time.perf_counter_ns()
    my_matrix.setCells (ordered_cell_list)
    my_matrix.markup ()
    my_matrix.reduceMarkup ()
    my_matrix.forceCells ()
    my_matrix.preemptiveSolve ()
    toc = time.perf_counter_ns()
    timeElapsed = (toc - tic) / 1000

    if outputStatMode == 0 or outputStatMode == 1:
        print (my_matrix)

    if outputStatMode == 1: 
        print (f'Solved in: {timeElapsed:0.4f} microsec')
        print (f'Number Givens: {numGivenValues}')
    elif outputStatMode == 2:
        print (f'{timeElapsed:0.4f} -1 {numGivenValues}')
    elif outputStatMode == 3:
        print (f'{timeElapsed:0.4f}')



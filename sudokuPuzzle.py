import numpy as np
from random import shuffle, sample, randint
from copy import deepcopy

class SudokuPuzzle(object):
    def __init__(self, data=None, original_entries=None):
        """
        data - input puzzle as one array, all rows concatenated.
        (default - incomplete puzzle)   
        
        original_entries - for inheritance of the original entries of one
        sudoku puzzle's original, immutable entries we don't 
        allow to change between random steps.                       
        """
        if data is None:
            self.data = np.array([0,0,5,7,0,0,0,1,2,
                                  0,3,9,0,0,0,0,0,0,
                                  6,0,0,0,5,4,0,9,0,
                                  0,0,1,0,4,0,0,0,6,
                                  0,0,0,2,0,0,8,0,0,
                                  0,9,7,3,0,0,0,5,0,
                                  4,0,0,1,0,6,0,0,0,
                                  0,0,0,0,0,3,0,8,7,
                                  0,2,0,0,0,7,0,0,1])
            print(self.data)
        else:
            self.data = data
    
        if original_entries is None:
            self.original_entries = np.arange(81)[self.data > 0]
        else:
            self.original_entries = original_entries
            
    def randomize_on_zeroes(self):
        """
        Go through entries, replace incomplete entries (zeroes) 
        with random numbers.
        """
        for num in range(9):
            block_indices = self.get_block_indices(num)
            block = self.data[block_indices]
            zero_indices = [ind for i,ind in enumerate(block_indices) if block[i] == 0]
            to_fill = [i for i in range(1,10) if i not in block]
            shuffle(to_fill)
            for ind, value in zip(zero_indices, to_fill):
                self.data[ind] = value
            
    def get_block_indices(self, k, ignore_originals=False):
        """
         Get data indices for kth block of puzzle.
        """
        row_offset = (k // 3) * 3
        col_offset = (k % 3)  * 3
        indices = [col_offset + (j%3) + 9*(row_offset + (j//3)) for j in range(9)]
        if ignore_originals:
            indices = list(filter(lambda x:x not in self.original_entries, indices))
        return indices
        
    def get_column_indices(self, i, type="data index"):
        """
        Get all indices for the column of ith index
        or for the ith column (depending on type)
        """
        if type=="data index":
            column = i % 9
        elif type=="column index":
            column = i
        indices = [column + 9 * j for j in range(9)]
        return indices
        
    def get_row_indices(self, i, type="data index"):
        """
        Get all indices for the row of ith index
        or for the ith row (depending on type)
        """
        if type=="data index":
            row = i // 9
        elif type=="row index":
            row = i
        indices = [j + 9*row for j in range(9)]
        return indices
        
    def view_results(self):
        """
        Visualize results as a 9 by 9 grid 
        (given as a two-dimensional numpy array)
        """ 
        results = np.array([self.data[self.get_row_indices(j, type="row index")] for j in range(9)])
        out_s = "{\n\"sudoku\": [\n"
        for i, row in enumerate(results):
            # if i%3==0: 
                # out_s += "="*25+'\n'
            out_s += "  [" + ", ".join([",".join(str(s) for s in list(row)[3*(k-1):3*k]) for k in range(1,4)]) + "]\n"
        out_s += '  ]\n}\n'
        print(out_s)
        return out_s    

    def score_board(self):
        """
        Score board by viewing every row and column and giving 
        -1 points for each unique entry.
        """
        score = 0
        for row in range(9):
            score -= len(set(self.data[self.get_row_indices(row, type="row index")]))
        for col in range(9):
            score -= len(set(self.data[self.get_column_indices(col,type="column index")]))
        return score
        
    def make_candidate_data(self):
        """
        Generates "neighbor" board by randomly picking
        a square, then swapping two small squares within.
        """
        new_data = deepcopy(self.data)
        block = randint(0,8)
        num_in_block = len(self.get_block_indices(block, ignore_originals=True))
        random_squares = sample(range(num_in_block),2)
        square1, square2 = [self.get_block_indices(block, ignore_originals=True)[ind] for ind in random_squares]
        new_data[square1], new_data[square2] = new_data[square2], new_data[square1]
        return new_data
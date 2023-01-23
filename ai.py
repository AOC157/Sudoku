import json
import numpy as np
import time
from sudokuPuzzle import SudokuPuzzle
from copy import deepcopy
from math import exp
from random import random


# *** you can change everything except the name of the class, the act function and the problem_data ***


class AI:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        pass

    # the solve function takes a json string as input
    # and outputs the solved version as json
    def solve(self, problem):
        # ^^^ DO NOT change the solve function above ***

        problem_data = json.loads(problem)
        # ^^^ DO NOT change the problem_data above ***

        # TODO implement your code here
        input_puzzle = np.array(problem_data["sudoku"]).ravel()
        start_time = time.time()
        finished = self.sudoku_solver_using_simulated_annealing(input_data=input_puzzle)
        duration_time = time.time() - start_time
        print(f'Elapsed time: { duration_time:.4f} s')

        # finished is the solved version
        return finished

    def sudoku_solver_using_simulated_annealing(self, input_data=None):
        """
        Uses a simulated annealing technique to solve a Sudoku puzzle.
        
        Randomly fills out the sub-squares to be consistent sub-solutions.
        
        Scores a puzzle by giving a -1 for every unique element
        in each row or each column. Best solution has a score of -162.
        (This is our stopping rule.)
        
        Candidate for new puzzle is created by randomly selecting
        sub-square, then randomly flipping two of its entries, evaluating
        the new score. The delta_S is the difference between the scores.
        
        Let T be the global temperature of our system, with a geometric
        schedule for decreasing (perhaps by T <- .999 T).
        
        If U is drawn uniformly from [0,1], and exp((delta_S/T)) > U,
        then we accept the candidate solution as our new state.
        """
        
        SP = SudokuPuzzle(input_data)
        print ("Original Puzzle:")
        SP.view_results()
        SP.randomize_on_zeroes()
        best_SP = deepcopy(SP)
        current_score = SP.score_board()
        best_score = current_score
        T = .5
        count = 0
        
        while (count < 400000):
            try:
                if (count % 1000 == 0): 
                    print ("Iteration %s,    \tT = %.5f, \tbest_score = %s, \tcurrent_score = %s"%(count, T, 
                                                                best_score, current_score))
                candidate_data = SP.make_candidate_data()
                SP_candidate = SudokuPuzzle(candidate_data, SP.original_entries)
                candidate_score = SP_candidate.score_board()
                delta_S = float(current_score - candidate_score)
                
                if (exp((delta_S/T)) - random() > 0):
                    SP = SP_candidate
                    current_score = candidate_score 
            
                if (current_score < best_score):
                    best_SP = deepcopy(SP)
                    best_score = best_SP.score_board()
            
                if candidate_score == -162:
                    SP = SP_candidate
                    break
        
                T = .99999*T
                count += 1
            except:
                print ("Random algorithm")      
        if best_score == -162:
            print ("\nSOLVED THE PUZZLE.")
        else:
            print ("\nDIDN'T SOLVE.")
        print ("\nFinal Puzzle:")
        return SP.view_results()
"""
This file defines a function to find a solution to the N Queen problem using the Min-Conflicts Heuristic algorithm.
It can be used from the command line.
"""

# import libraries
import argparse
import random
import os
import sys
sys.path.insert(0,'..')
#
from time import time
from utils import create_board, num_attacks, set_board, show_results

def find_solution(n: int):
    """
    This is the main function of MinConflictsHeuristic, representing the process of the environment.

    Parameters:
    n (int): The desired number of queens (dimension of the board) as an integer.

    Returns:
    solution (list): The solution to the N queen problem as a list.
    """
    assert type(n) == int, "n is not an integer!"

    state = []
    for i in range(n):
        conflicts = []
        for j in range(n):
            conflicts.append(num_conflicts(state, i, j, i))
        minConflicts = min(conflicts)
        matches = []
        for j in range(n):
            if conflicts[j] == minConflicts:
                matches.append(j)
        
        state.append(random.choice(matches))
        
    prev = 9999999999999
    laterals = 0
    maxIter = 1000
    
    while True:
        maxIter -= 1
        if maxIter == 0:
            
            return state
        nAttacks = num_attacks(state)

        if nAttacks == 0:
            return state
        
        if nAttacks == prev:
            laterals += 1
            if laterals > 100:
                return state
        else:
            laterals = 0
            
        prev = nAttacks
        
        order = [i for i in range(n)]
        random.shuffle(order)
        for i in order:

            if num_conflicts(state, i, state[i], n) == 0:
                continue
        
            conflicts = [999999999 for j in range(n)]
            
            for j in range(n):
                if j == state[i]:
                    continue
                conflicts[j] = num_conflicts(state, i, j, n)
                
            minConflicts = min(conflicts)
            matches = []
            for k in range(n):
                if minConflicts == conflicts[k]:
                    matches.append(k)
            j = random.choice(matches)
            state[i] = j

            if num_attacks(state) == 0:
                return state

def num_conflicts(state: list, i: int, pretend: int, n: int):
    """
    This function returns the number of conflicts.

    Parameters:
    state (list): The state of the proposed solution as a list.
    i (int): The index of the state.
    pretend (int): An alternative index of the state.
    n (int): The index of the state.

    Returns:
    conflicts (int): The number of conflicts as an integer.
    """
    assert type(state) == list, "state is not a list!"
    assert type(i) == int, "i is not an integer!"
    assert type(pretend) == int, "pretend is not an integer!"
    assert type(n) == int, "n is not an integer!"

    conflicts = 0
    for j in range(n):
        if j == i:
            continue

        if state[j] == pretend:
            conflicts += 1
            continue

        if state[j]+j == pretend+i:
            conflicts += 1
            continue

        if state[j]-j == pretend-i:
            conflicts += 1
            continue

    return conflicts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process N Queen MinConflictsHeuristic Solver parameters.')
    parser.add_argument('-n', '--dimension', type=int,
                        help='The desired number of queens (dimension of the board).')
    args = parser.parse_args()
    if args.dimension:
        assert args.dimension >= 4, "Dimension should be an integer >=4!"
        assert type(args.dimension)==int, "Dimension should be an integer >=4!"

    # entering the input from the command line
    if not args.dimension:
        while True:
            dimension = input("Enter board dimension (the desired number of queens): ")
            try:
                dimension = int(dimension)
                if dimension < 4:
                    print("Error: Dimension should be an integer n>=4, try again!")
                else:
                    break
            except ValueError:
                print("ValueError: Dimension must be an integer n>=4, try again!")
    else:
        dimension = args.dimension

    # Solving N Queen problem with MinConflictsHeuristic solver
    print(f'\nSolving N={dimension} Queen problem with MinConflictsHeuristic Solver...')
    start = time()
    while True:
        solution = find_solution(dimension)
        if num_attacks(solution) == 0:
            break
    end = time()

    # create the board for N dimension, and output the solution
    board = create_board(dimension)
    set_board(board, solution, dimension)
    print("\nSolution:")
    solution = [x+1 for x in solution]
    print(solution)
    duration = f'Time (ss): {round(end - start,2)}'
    print()
    print(duration)
    show_results(solution, duration, dimension, os.path.basename(__file__).split(".")[0])

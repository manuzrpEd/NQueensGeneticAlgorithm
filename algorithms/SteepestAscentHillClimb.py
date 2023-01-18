"""
This file defines a function to find a solution to the N Queen problem usng the Steepest Ascent Hill Climb algorithm.
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
from utils import create_board, find_neighbours, num_attacks, set_board, show_results

def find_solution(n: int):
    """
    This is the main function of SimulatedAnnealing, representing the process of the environment.

    Parameters:
    n (int): The desired number of queens (dimension of the board) as an integer.

    Returns:
    solution (list): The solution to the N queen problem as a list.
    """
    assert type(n) == int, "n is not an integer!"

    state = []
    for i in range(n):
        state.append(random.randint(0, n-1))
    state = State(state)

    laterals = 0
    while True:
        prev = state.fitness

        neighbours = find_neighbours(state.state)
        for i in range(len(neighbours)):
            neighbours[i] = State(neighbours[i])
        neighbours.append(state)

        neighbours.sort(key=(lambda key: key.fitness))

        state = neighbours[0]

        if state.fitness == 0:
            return state.state

        if state.fitness == prev:
            laterals += 1
            if laterals > 20:
                return state.state
        else:
            laterals = 0

class State:
    """
    This class contains information about the State for the SteepestAscentHillClimb algorithm.

    Attributes:
        state (list): The state of the proposed solution as a list.
    """
    def __init__(self, state: list):
        assert type(state) == list, "state is not a list!"
        self.state = state
        self.fitness = num_attacks(state)
        self.peaked = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process N Queen SteepestAscentHillClimb Solver parameters.')
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

    # Solving N Queen problem with SteepestAscentHillClimb solver
    print(f'\nSolving N={dimension} Queen problem with SteepestAscentHillClimb Solver...')
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


"""
This file defines a function to find a solution to the N Queen problem using the Line Beam Search algorithm.
It can be used from the command line.
"""

# import libraries
import argparse
import random
import os
#
from time import time
from utils import create_board, find_neighbours, num_attacks, set_board, show_results

class State:
    """
    This class contains information about the State for the LineBeamSearch algorithm.

    Attributes:
    state (list): The state of the proposed solution as a list.
    """
    def __init__(self, state: list):
        assert type(state) == list, "state is not a list!"
        self.state = state
        self.fitness = num_attacks(state)
        self.peaked = False

def find_solution(n: int):
    """
    This is the main function of LineBeamSearch, representing the process of the environment.

    Parameters:
    n (int): The desired number of queens (dimension of the board) as an integer.

    Returns:
    solution (list): The solution to the N queen problem as a list.
    """
    assert type(n) == int, "n is not an integer!"

    k = 30

    states = []
    for i in range(k):
        state = []
        for i in range(n):
            state.append(random.randint(0, n-1))
        states.append(State(state))

    laterals = 0
    while True:
        prev = max(states, key=(lambda key: key.fitness)).fitness
        
        neighbours = states.copy()
        for s in states:
            neighbours += get_neighbours(s)
        neighbours.sort(key=(lambda key: key.fitness))

        states = neighbours[:k]
        if states[0].fitness == 0:
            return states[0].state

        if states[0].fitness == prev:
            laterals += 1
            if laterals > 20:
                return states[0].state
        else:
            laterals = 0
        

def get_neighbours(state: State):
    """
    This function returns the state of the neighbours.

    Parameters:
    state (list): The state of the proposed solution as a list.

    Returns:
    neighbours (list): The state of the neighbours as a list.
    """
    assert isinstance(state, State), "state is not an instance of the State class!"

    neighbours = find_neighbours(state.state)
    for i in range(len(neighbours)):
        neighbours[i] = State(neighbours[i])

    return neighbours

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process N Queen LineBeamSearch Solver parameters.')
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

    # Solving N Queen problem with LineBeamSearch solver
    print(f'\nSolving N={dimension} Queen problem with LineBeamSearch Solver...')
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

"""
This file has functions used throughout the repository.
"""

# import libraries
import os
#
import matplotlib.pyplot as plt

def printBoard(state):
    print("")
    for s in state:
        print(' '.join(['-' if i != s else 'Q' for i in range(len(state))]))

def num_attacks(state):
    count = 0
    count += len(state) - len(set(state))

    diag_state1 = [state[i] - i for i in range(len(state))]
    diag_state2 = [state[i] + i for i in range(len(state))]
    count += len(diag_state1) - len(set(diag_state1))
    count += len(diag_state2) - len(set(diag_state2))
    
    return count

def find_neighbours(state):
    neighbours = []
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i] == j:
                continue

            new_state = state.copy()
            new_state[i] = j
            neighbours.append(new_state)

    return neighbours

def create_board(n: int):
    """
    This function creates the board.

    Parameters:
    n (int): The desired number of queens.

    Returns:
    board (list): The board as a list of lists.
    """
    assert type(n) == int, "n is not an integer!"

    board = [[0 for i in range(n)] for j in range(n)]
    return board

def set_board(board: list, pos: list, n: int):
    """
    This function sets the board.

    Parameters:
    board (list): The board as a list of lists.
    pos (list): A chromosome, which is a list of genes.

    Returns:
    board (list): The board as a list of lists.
    """
    assert type(board) == list, "board is not a list!"
    assert type(pos) == list, "pos is not a list!"

    for i in range(n):
        board[pos[i]][i] = 1

def show_results(res: list, duration: str, n: int, algo: str):
    """
    This function plots and saves the solution on a board.

    Parameters:
    res (list): The results/solution as a list of positions.
    duration (str): The duration of the GA solver as a string.
    """
    assert type(res) == list, "res is not a list!"
    assert type(duration) == str, "duration is not a string!"
    assert type(n) == int, "n is not an integer!"
    assert type(algo) == str, "algo is not a string!"

    l = len(res) + 1
    if l >= 80:
        plt.figure(figsize=(11, 11))
        plt.scatter([x + 1 for x in range(l - 1)], res[:l - 1], s=2)
        for i in range(l):
            plt.plot([0.5, l - 0.5], [i + 0.5, i + 0.5], color="k", linewidth=0.25)
            plt.plot([i + 0.5, i + 0.5], [0.5, l - 0.5], color="k", linewidth=0.25)
    elif l >= 30:
        plt.figure(figsize=(9, 9))
        plt.scatter([x + 1 for x in range(l - 1)], res[:l - 1], s=3)
        for i in range(l):
            plt.plot([0.5, l - 0.5], [i + 0.5, i + 0.5], color="k", linewidth=0.5)
            plt.plot([i + 0.5, i + 0.5], [0.5, l - 0.5], color="k", linewidth=0.5)
    else:
        plt.figure(figsize=(6, 6))
        plt.scatter([x + 1 for x in range(l - 1)], res[:l - 1])
        for i in range(l):
            plt.plot([0.5, l - 0.5], [i + 0.5, i + 0.5], color="k")
            plt.plot([i + 0.5, i + 0.5], [0.5, l - 0.5], color="k")
    #         plt.xticks(np.arange(1,l,1))
    #         plt.yticks(np.arange(1,l,1))
    plt.title(f'{algo} Solution for N={n}, {duration}')
    plt.savefig(f'solutions/{algo}_SolutionBoard_N={n}.png')
    plt.show()

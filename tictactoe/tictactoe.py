"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                count += 1
    if board == initial_state:
        return X
    elif count % 2 == 0:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    legal_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                legal_actions.add((i,j))
    return legal_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Illegal action")

    table = copy.deepcopy(board)
    table[action[0]][action[1]] = player(board)
    return table

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    else:
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]
            elif board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]
            else:
                return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is None:
        count = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False
        return True

    else:
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    Max = float("-inf")
    Min = float("inf")

    if player(board) == "X":
        return Maximization(board, Max, Min)[1]
    elif player(board) == "O":
        return Minimization(board, Max, Min)[1]

def Maximization(board, Max, Min):
    opt_action = None
    if terminal(board):
        return[utility(board), None]

    value = Max
    for action in actions(board):
        test = Minimization(result(board, action), Max, Min)[0]
        Max = max(Max, test)
        if test > value:
            value = test
            opt_action = action
        if Max >= Min:
            break
    return [value, opt_action]

def Minimization(board, Max, Min):
    opt_action = None
    if terminal(board):
        return[utility(board), None]
    value = Min
    for action in actions(board):
        test = Maximization(result(board, action), Max, Min)[0]
        Min = min(Min, test)
        if test < value:
            value = test
            opt_action = action
        if Max >= Min:
            break
    return [value, opt_action]
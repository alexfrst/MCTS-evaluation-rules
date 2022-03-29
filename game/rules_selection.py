from random import *
from math import *
import math

eps = 1e-15


def UCB_selection(node, exploration_constant):
    # define best score & best moves
    best_score = float('-inf')
    best_moves = []

    # loop over child nodes
    for child_node in node.children.values():
        # define current player
        if child_node.board.player_2 == 'x':
            current_player = 1
        elif child_node.board.player_2 == 'o':
            current_player = -1

        # get move score using UCT formula
        move_score = current_player * child_node.score / child_node.visits + \
            exploration_constant * \
            math.sqrt(math.log(node.visits / child_node.visits))

        # better move has been found
        if move_score > best_score:
            best_score = move_score
            best_moves = [child_node]

        # found as good move as already available
        elif move_score == best_score:
            best_moves.append(child_node)

    # return one of the best moves randomly
    return choice(best_moves)


def klBern(x, y):
    """Kullback-Leibler divergence for Bernoulli distributions."""
    x = min(max(x, eps), 1-eps)
    y = min(max(y, eps), 1-eps)
    return x*log(x/y) + (1-x)*log((1-x)/(1-y))


def klGauss(x, y, sig2=1.):
    """Kullback-Leibler divergence for Gaussian distributions."""
    return (x-y)*(x-y)/(2*sig2)


def IMED_selection(node, kullback):
    best_score = float('inf')
    best_moves = []
    means = []
    for child_node in node.children.values():
        means.append((child_node.score)/child_node.visits)
        maxMeans = max(means)

        move_score = child_node.visits * kullback((child_node.score)/child_node.visits, maxMeans) + math.log(
            child_node.visits) if child_node.visits > 0 else -1

        # better move has been found
        if move_score < best_score:
            best_score = move_score
            best_moves = [child_node]

        # found as good move as already available
        elif move_score == best_score:
            best_moves.append(child_node)
    # return one of the best moves randomly
    return choice(best_moves)


def random_selection(node):
    moves = [child_node for child_node in node.children.values()]
    return choice(moves)

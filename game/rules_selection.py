from random import *
from math import *
import math

def UCB_selection(node, exploration_constant):
        # define best score & best moves
        best_score = float('-inf')
        best_moves = []

        # loop over child nodes
        for child_node in node.children.values():
            # define current player
            if child_node.board.player_2 == 'x': current_player = 1
            elif child_node.board.player_2 == 'o': current_player = -1

            # get move score using UCT formula
            move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))

            # better move has been found
            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]

            # found as good move as already available
            elif move_score == best_score:
                best_moves.append(child_node)
        
        # return one of the best moves randomly
        return choice(best_moves)


def klGauss(x, y, sig2 = 1.):
    """Kullback-Leibler divergence for Gaussian distributions."""
    return (x-y)*(x-y)/(2*sig2)


def IMED_selection(node, kullback):
        best_score = float('inf')
        best_moves = []
        means = []
        for child_node in node.children.values():
            # define current player
            if child_node.board.player_2 == 'x': 
                current_player = 1
            elif child_node.board.player_2 == 'o': 
                current_player = -1
                
            means.append((current_player*child_node.score)/child_node.visits)
            maxMeans = max(means)
            
            move_score = child_node.visits * kullback((current_player*child_node.score)/child_node.visits, maxMeans ) + math.log(child_node.visits) if child_node.visits > 0 else 0 # ou -np.Inf ?
            
            if move_score == float('inf') : 
                print('move_score is inf' )
            # better move has been found
            if move_score < best_score:
                best_score = move_score
                best_moves = [child_node]
                
            # found as good move as already available
            elif move_score == best_score:
                best_moves.append(child_node)
        # return one of the best moves randomly
        return choice(best_moves) 





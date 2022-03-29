import itertools
import random

import networkx as nx
import numpy as np
from copy import deepcopy
from itertools import product

class Color:
    BLACK = 'x'
    WHITE = "o"


class GoBoard():
    # create constructor (init board class instance)
    def __init__(self, board=None,size =9,rule_selection1 = 'UCB', rule_selection2 = 'IMED'):

        # define players
        self.player_1 = Color.BLACK
        self.player_2 = Color.WHITE
        self.height = size
        self.width = size
        self.size = size
        self.rule_selection = rule_selection1
        self.rule_selection2 = rule_selection2
        self.empty_square = '.'
        self.played_turns = 0
        self.prisoners_player_1 = 0
        self.prisoners_player_2 = 0
        self.stones_per_player = (size-1)**2 + (size/2)
        self.one_player_capitulated = False

        # define board position
        self.board = np.full((self.size, self.size), fill_value=".", dtype=str)

        # init (reset) board
        self.init_board()

        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)
            self.board = deepcopy(board.board)

    def has_no_liberties(self, group):
        """Check if a stone group has any liberties on a given board.
        Args:
            group (List[Tuple[int, int]]): list of (col,row) pairs defining a stone group
        Returns:
            [boolean]: True if group has any liberties, False otherwise
        """
        for x, y in group:
            if x > 0 and self.board[x - 1, y] == ".":
                return False
            if y > 0 and self.board[x, y - 1] == ".":
                return False
            if x < self.board.shape[0] - 1 and self.board[x + 1, y] == ".":
                return False
            if y < self.board.shape[0] - 1 and self.board[x, y + 1] == ".":
                return False
        return True

    def render(self):
        return self.board

    def get_player_group(self, board, color: Color):
        size = board.shape[0]
        xs, ys = np.where(board == color)
        graph = nx.grid_graph(dim=[size, size])
        stones = set(zip(xs, ys))
        all_spaces = set(product(range(size), range(size)))
        stones_to_remove = all_spaces - stones
        graph.remove_nodes_from(stones_to_remove)
        return nx.connected_components(graph)

    # init (reset) board
    def init_board(self):
        self.board = np.full((self.size, self.size),fill_value='.', dtype=str)

    def get_stone_groups(self,color):
        """Get stone groups of a given color on a given board
        Returns:
            List[List[Tuple[int, int]]]: list of list of (col, row) pairs, each defining a group
        """
        size = self.board.shape[0]
        color_code = color
        xs, ys = np.where(self.board == color_code)
        graph = nx.grid_graph(dim=[size, size])
        stones = set(zip(xs, ys))
        all_spaces = set(itertools.product(range(size), range(size)))
        stones_to_remove = all_spaces - stones
        graph.remove_nodes_from(stones_to_remove)
        return nx.connected_components(graph)

    # make move
    def make_move(self, row, col):
        # create new board instance that inherits from the current state
        board = GoBoard(self)

        # make move
        #print(board.player_1)
        board.board[row, col] = board.player_1

        if board.prisoners_player_1 < board.prisoners_player_2 and random.random() < 0:
            self.one_player_capitulated = True

        # handle captures
        capture_happened = False
        for group in list(board.get_stone_groups(board.player_2)):
            if board.has_no_liberties(group):
                for i, j in group:
                    board.board[i, j] = "."
                board.prisoners_player_1 += len(group)

        # swap players
        (board.player_1, board.player_2) = (board.player_2, board.player_1)
        (board.prisoners_player_1, board.prisoners_player_2) = (board.prisoners_player_2, board.prisoners_player_1)
        board.played_turns += 1

        return board

    # get whether the game is drawn
    def is_draw(self):
        # loop over board squares
        for row, col in product(range(self.size), range(self.size)):
            # empty square is available
            if self.board[row, col] == self.empty_square:
                # this is not a draw
                return False

        # by default we return a draw
        return True

    # get whether the game is won
    def is_win(self):
        if self.one_player_capitulated:
            print("Player capitulated")
            return True

        if self.played_turns < (2 * self.stones_per_player):
            return False

        return self.prisoners_player_1 >= self.prisoners_player_2

    # generate legal moves to play in the current position
    def generate_states(self):
        actions = []
        positions = []

        for row in range(self.height):
            for col in range(self.width):
                if self.is_valid_move(row, col):
                    positions.append((row, col))
                    actions.append(self.make_move(row, col))
        return actions

    def is_valid_move(self, row, col):
        if col < 0 or col >= self.board.shape[1]:
            return False
        if row < 0 or row >= self.board.shape[0]:
            return False
        return self.board[row, col] == "."

    def game_turn_player(self, pos):
        return self.make_move(*pos)

    def game_turn_IA(self, mcts, rule_selection):
        print("starting AI play")
        try:
            best_move = mcts.search(self, rule_selection)
            print(best_move.board)
            self = best_move.board
        except Exception as e:
            print(e)

        if self.is_win():
            print("AI won the game")

        # check if the game is drawn
        elif self.is_draw():
            print('Game is drawn!\n')
        print("Ended AI turn")
        print(f"{self.prisoners_player_1=} {self.prisoners_player_2=}")
        return self

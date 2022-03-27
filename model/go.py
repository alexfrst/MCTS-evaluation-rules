import itertools

import networkx as nx
import numpy as np
from copy import deepcopy
from itertools import product

BOARD_SIZE = 9
STONE_COUNTS = 90
GENERAL = 0


class Color:
    BLACK = 'o'
    WHITE = "x"


class Board():
    # create constructor (init board class instance)
    def __init__(self, board=None, rule_selection='UCB'):

        # define players
        self.player_1 = Color.BLACK
        self.player_2 = Color.WHITE
        self.height = BOARD_SIZE
        self.width = BOARD_SIZE
        self.rule_selection = rule_selection
        self.empty_square = 0
        self.played_turns = 0
        self.prisoners = {
            Color.BLACK: 0,
            Color.WHITE: 0
        }

        # define board position
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=str)

        # init (reset) board
        self.init_board()

        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)
            self.board = deepcopy(board.board)
            board.board[0, 0] -= 1
            assert board.board[0, 0] != self.board[0, 0]
            board.board[0, 0] += 1
            assert board.board[0, 0] == self.board[0, 0]

    def has_no_liberties(self, group):
        """Check if a stone group has any liberties on a given board.
        Args:
            group (List[Tuple[int, int]]): list of (col,row) pairs defining a stone group
        Returns:
            [boolean]: True if group has any liberties, False otherwise
        """
        for x, y in group:
            if x > 0 and self.board[x - 1, y] == 0:
                return False
            if y > 0 and self.board[x, y - 1] == 0:
                return False
            if x < self.board.shape[0] - 1 and self.board[x + 1, y] == 0:
                return False
            if y < self.board.shape[0] - 1 and self.board[x, y + 1] == 0:
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
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))

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
        board = Board(self)

        # make move
        board.board[row, col] = self.player_1
        board.played_turns[self.player_1] += 1

        # handle captures
        capture_happened = False
        for group in list(self.get_stone_groups(self.player_2)):
            if self.has_no_liberties(group):
                capture_happened = True
                for i, j in group:
                    self.board[i, j] = 0
                self.prisoners[self.player_1] += len(group)

        # handle special case of invalid stone placement
        # this must be done separately because we need to know if capture resulted
        if not capture_happened:
            group = None
            for group in self.get_stone_groups():
                if (col, row) in group:
                    break
            if self.has_no_liberties(group):
                self.board[col, row] = 0
                return

        # swap players
        (board.player_1, board.player_2) = (board.player_2, board.player_1)
        self.played_turns += 1

        return board

    # get whether the game is drawn
    def is_draw(self):
        # loop over board squares
        for row, col in product(range(BOARD_SIZE), range(BOARD_SIZE)):
            # empty square is available
            if self.board[row, col] == self.empty_square:
                # this is not a draw
                return False

        # by default we return a draw
        return True

    # get whether the game is won
    def is_win(self):
        if self.played_turns[self.player_1] <= STONE_COUNTS:
            return False

        return self.prisoners[self.player_1] >= self.prisoners[self.player_2]

    # generate legal moves to play in the current position
    def generate_states(self):
        actions = []
        positions = []

        for row in range(self.height):
            for col in range(self.width):
                if self.is_valid_move(col, row):
                    positions.append((row, col))
                    actions.append(self.make_move(row, col))
        return actions

    def is_valid_move(self, col, row):
        if col < 0 or col >= self.board.shape[1]:
            return False
        if row < 0 or row >= self.board.shape[0]:
            return False
        return self.board[row, col] == 0

    def game_turn_player(self, pos):
        return self.make_move(*pos)

    def game_turn_IA(self, mcts):
        print("starting AI play")
        try:
            best_move = mcts.search(self, self.rule_selection)
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
        return self

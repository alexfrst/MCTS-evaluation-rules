from copy import deepcopy
import sys


class TicTacToeBoard():
    # create constructor (init board class instance)
    def __init__(self, board=None, size=3, rule_selection1='UCB', rule_selection2='IMED', sequence_length=3):
        # define players
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.height = size
        self.width = size
        self.sequence_length = sequence_length
        self.empty_square = '.'
        self.rule_selection = rule_selection1
        self.rule_selection2 = rule_selection2

        # define board position
        self.position = {}

        # init (reset) board
        self.init_board()

        # create a copy of a previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def render(self):
        return self.position

    # init (reset) board
    def init_board(self):
        for row in range(self.height):
            for col in range(self.width):
                self.position[row, col] = self.empty_square

    # make move
    def make_move(self, row, col):
        # create new board instance that inherits from the current state
        board = TicTacToeBoard(self)

        board.position[row, col] = self.player_1

        (board.player_1, board.player_2) = (board.player_2, board.player_1)

        return board

    def is_draw(self):
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                return False

        return True

    # get whether the game is won
    def is_win(self):

        for col in range(self.width):
            winning_sequence = []

            for row in range(self.height):
                if self.position[row, col] == self.player_2:
                    winning_sequence.append((row, col))

                if len(winning_sequence) == self.sequence_length:
                    return True

        # loop over board columns
        for row in range(self.height):
            # define winning sequence list
            winning_sequence = []

            for col in range(self.width):
                if self.position[row, col] == self.player_2:
                    winning_sequence.append((row, col))

                if len(winning_sequence) == self.sequence_length:
                    return True

        winning_sequence = []

        for row in range(self.height):
            col = row

            if self.position[row, col] == self.player_2:
                winning_sequence.append((row, col))

            if len(winning_sequence) == self.sequence_length:
                return True

        winning_sequence = []

        for row in range(self.height):
            col = self.width - row - 1

            if self.position[row, col] == self.player_2:
                winning_sequence.append((row, col))

            if len(winning_sequence) == self.sequence_length:
                return True

        return False

    # generate legal moves to play in the current position
    def generate_states(self):
        actions = []

        for row in range(self.height):
            for col in range(self.width):
                if self.is_valid_move(row, col):
                    actions.append(self.make_move(row, col))

        return actions

    def is_valid_move(self, row, col):
        if row < 0 or row >= self.height:
            return False
        if col < 0 or col >= self.width:
            return False
        return self.position[row, col] == self.empty_square

    def game_turn_player(self, pos):
        return self.make_move(*pos)

    def game_turn_IA(self, mcts, rule_selection):
        try:
            best_move = mcts.search(self, rule_selection)
            self = best_move.board
        except Exception as e:
            print(sys.exc_info()[2])
            print(e)
            pass

        return self

from copy import deepcopy
from game.game_handler import MCTS


class TicTacToeBoard():
    # create constructor (init board class instance)
    #def __init__(self, board=None, rule_selection='UCB', size=3):
    def __init__(self, board=None, size=3, rule_selection1 = 'UCB', rule_selection2 = 'IMED'):
        # define players
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.height = size
        self.width = size
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
        # loop over board rows
        for row in range(self.height):
            # loop over board columns
            for col in range(self.width):
                # set every board square to empty square
                self.position[row, col] = self.empty_square

    # make move
    def make_move(self, row, col):
        # create new board instance that inherits from the current state
        board = TicTacToeBoard(self)

        # make move
        board.position[row, col] = self.player_1

        # swap players
        (board.player_1, board.player_2) = (board.player_2, board.player_1)

        # return new board state
        return board

    # get whether the game is drawn
    def is_draw(self):
        # loop over board squares
        for row, col in self.position:
            # empty square is available
            if self.position[row, col] == self.empty_square:
                # this is not a draw
                return False

        # by default we return a draw
        return True

    # get whether the game is won
    def is_win(self):
        ##################################
        # vertical sequence detection
        ##################################

        # loop over board columns
        for col in range(self.width):
            # define winning sequence list
            winning_sequence = []

            # loop over board rows
            for row in range(self.height):
                # if found same next element in the row
                if self.position[row, col] == self.player_2:
                    # update winning sequence
                    winning_sequence.append((row, col))

                # if we have 3 elements in the row
                if len(winning_sequence) == 3:
                    # return the game is won state
                    return True

        ##################################
        # horizontal sequence detection
        ##################################

        # loop over board columns
        for row in range(self.height):
            # define winning sequence list
            winning_sequence = []

            # loop over board rows
            for col in range(self.width):
                # if found same next element in the row
                if self.position[row, col] == self.player_2:
                    # update winning sequence
                    winning_sequence.append((row, col))

                # if we have 3 elements in the row
                if len(winning_sequence) == 3:
                    # return the game is won state
                    return True

        ##################################
        # 1st diagonal sequence detection
        ##################################

        # define winning sequence list
        winning_sequence = []

        # loop over board rows
        for row in range(self.height):
            # init column
            col = row

            # if found same next element in the row
            if self.position[row, col] == self.player_2:
                # update winning sequence
                winning_sequence.append((row, col))

            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                # return the game is won state
                return True
        winning_sequence = []

        # loop over board rows
        for row in range(self.height):
            # init column
            col = self.width - row - 1

            # if found same next element in the row
            if self.position[row, col] == self.player_2:
                # update winning sequence
                winning_sequence.append((row, col))

            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                # return the game is won state
                return True

        # by default return non winning state
        return False

    # generate legal moves to play in the current position
    def generate_states(self):
        # define states list (move list - list of available actions to consider)
        actions = []

        # loop over board rows
        for row in range(self.height):
            # loop over board columns
            for col in range(self.width):
                # make sure that current square is empty
                if self.position[row, col] == self.empty_square:
                    # append available action/board state to action list
                    actions.append(self.make_move(row, col))

        # return the list of available actions (board class instances)
        return actions

    # main game loop
    def game_turn_player(self, pos):
        return self.make_move(*pos)

    def game_turn_IA(self, mcts, rule_selection):
        try:
            best_move = mcts.search(self, rule_selection)
            self = best_move.board
        except Exception as e:
            print(e.with_traceback())
            print(e)
            pass

        if self.is_win():
            print("AI won the game")

        # check if the game is drawn
        elif self.is_draw():
            print('Game is drawn!\n')

        return self


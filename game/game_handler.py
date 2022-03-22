import random
from game.rules_selection import IMED_selection, UCB_selection, klGauss


# tree node class definition
class TreeNode():
    def __init__(self, board, parent):
        self.board = board

        if self.board.is_win() or self.board.is_draw():
            self.is_terminal = True
        else:
            self.is_terminal = False

        self.is_fully_expanded = self.is_terminal
        self.parent = parent

        self.visits = 0
        self.score = 0
        self.children = {}


class MCTS():
    # search for the best move in the current position
    def search(self, initial_state, rule_selection):

        # create root node
        self.root = TreeNode(initial_state, None)
        print(initial_state.board)

        for iteration in range(1000):
            node = self.select(self.root, rule_selection, exploration_constant=2)
            score = self.rollout(node.board)
            self.backpropagate(node, score)

        try:
            return self.get_best_move(self.root, rule_selection, exploration_constant=2)

        except Exception as e:
            print(e)

    # select most promising node
    def select(self, node, rule_selection, exploration_constant=2):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(
                    node, rule_selection, exploration_constant, klGauss)

            else:
                return self.expand(node)

        return node

    # expand node
    def expand(self, node):
        states = node.board.generate_states()
        for state in states:
            # make sure that current state (move) is not present in child nodes
            if str(state.render()) not in node.children:
                new_node = TreeNode(state, node)
                node.children[str(state.render())] = new_node

                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                return new_node

        print('Should not get here!!!')

    # simulate the game via making random moves until reach end of the game
    def rollout(self, board):
        while not board.is_win():
            try:
                board = random.choice(board.generate_states())
            except:
                return 0

        if board.player_2 == 1:
            return 1
        elif board.player_2 == 2:
            return -1

    # backpropagate the number of visits and score up to the root node
    def backpropagate(self, node, score):
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    # select the best node
    def get_best_move(self, node, rule_selection, exploration_constant, kullback=klGauss):
        if rule_selection == 'UCB':
            next_move = UCB_selection(node, exploration_constant)
        else:
            next_move = IMED_selection(node, kullback)

        return (next_move)

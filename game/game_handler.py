import random
from game.rules_selection import IMED_selection, UCB_selection, klBern, random_selection


# tree node class definition
class TreeNode():
    # class constructor (create tree node class instance)
    def __init__(self, board, parent):
        # init associated board state
        self.board = board

    # init is node terminal flag
        if self.board.is_win() or self.board.is_draw():
            self.is_terminal = True
        else:
            self.is_terminal = False

        self.is_fully_expanded = self.is_terminal
        self.parent = parent

        # init the number of node visits
        self.visits = 0

        # init the total score of the node
        self.score = 0

        # init current node's children
        self.children = {}

# MCTS class definition


class MCTS():
    # search for the best move in the current position
    def search(self, initial_state, rule_selection):
        # create root node
        self.root = TreeNode(initial_state, None)

        # walk through 1000 iterations
        for iteration in range(1000):
            # select a node (selection phase)
            node = self.select(self.root, rule_selection,
                               exploration_constant=2)

            # scrore current node (simulation phase)
            score = self.rollout(node.board)

            # backpropagate results
            self.backpropagate(node, score)

        # pick up the best move in the current position
        try:
            return self.get_best_move(self.root, rule_selection, exploration_constant=2)

        except:
            pass

    # select most promising node
    def select(self, node, rule_selection, exploration_constant=2):
        # make sure that we're dealing with non-terminal nodes
        while not node.is_terminal:
            # case where the node is fully expanded
            if node.is_fully_expanded:
                node = self.get_best_move(
                    node, rule_selection, exploration_constant, klBern)

            # case where the node is not fully expanded
            else:
                # otherwise expand the node
                return self.expand(node)

        # return node
        return node

    # expand node
    def expand(self, node):
        # generate legal states (moves) for the given node
        states = node.board.generate_states()

        # loop over generated states (moves)
        for state in states:
            # make sure that current state (move) is not present in child nodes
            if str(state.position) not in node.children:
                # create a new node
                new_node = TreeNode(state, node)

                # add child node to parent's node children list (dict)
                node.children[str(state.position)] = new_node

                # case when node is fully expanded
                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                # return newly created node
                return new_node

        # debugging
        print('Should not get here!!!')

    # simulate the game via making random moves until reach end of the game
    def rollout(self, board):
        # make random moves for both sides until terminal state of the game is reached
        while not board.is_win():
            # try to make a move
            try:
                # make the on board
                board = random.choice(board.generate_states())

            # no moves available
            except:
                # return a draw score
                return 0

        # return score from the player "x" perspective
        if board.player_2 == 'x':
            return 1
        elif board.player_2 == 'o':
            return -1

    # backpropagate the number of visits and score up to the root node
    def backpropagate(self, node, score):
        # update nodes's up to root node
        while node is not None:
            # update node's visits
            node.visits += 1

            # update node's score
            node.score += score

            # set node to parent
            node = node.parent

    # select the best node
    def get_best_move(self, node, rule_selection, exploration_constant, kullback=klBern):
        if rule_selection == 'UCB':
            next_move = UCB_selection(node, exploration_constant)

        elif rule_selection == 'IMED':
            next_move = IMED_selection(node, kullback)

        elif rule_selection == 'random':
            next_move = random_selection(node)

        return(next_move)

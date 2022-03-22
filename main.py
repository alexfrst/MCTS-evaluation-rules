from view.game_window import GameWindow
from model.tictactoe import Board

# choose between 'IMED' 'UCB' 'random'
rule_selection = 'random'
game = GameWindow(Board(rule_selection=rule_selection))
game.mainloop()

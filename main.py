from view.game_window import GameWindow
from model.tictactoe import Board

rule_selection = 'UCB'
game = GameWindow(Board(rule_selection=rule_selection))
game.mainloop()

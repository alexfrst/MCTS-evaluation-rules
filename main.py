from view.game_window import GameWindow
from view.start_window import StartWindow
from model.tictactoe import Board

"""
rule_selection = 'UCB'
game = GameWindow(Board(rule_selection=rule_selection))
game.mainloop()
"""

game = StartWindow()
game.mainloop()

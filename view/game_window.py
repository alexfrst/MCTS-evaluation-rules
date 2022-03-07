from tkinter import Tk

from game.game_handler import MCTS
from view.grid import GameGrid
from model.tictactoe import Board
#from model.tictactoe import MCTS


class GameWindow(Tk):
    def __init__(self, model:Board):
        super().__init__()
        self.configure(bg="#333333", padx=10, pady=10)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{screen_width//2}x{screen_height//2}')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.model = model
        self.mcts = MCTS()
        self.grid = GameGrid(self,model.height,model.width)

    def play(self, pos):
        self.model = self.model.game_turn_player(pos)
        self.grid.render(self.model.position)
        self.update()
        self.model = self.model.game_turn_IA(self.mcts)
        self.grid.render(self.model.position)
        self.update()



class MyModel:
    def __init__(self):
        self.height = 8
        self.width = 8

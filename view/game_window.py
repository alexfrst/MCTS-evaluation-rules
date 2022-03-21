from tkinter import Tk, Label
import tkinter.font as tkFont
from game.game_handler import MCTS
from view.grid import GameGrid
from model.tictactoe import TicTacToeBoard
#from model.tictactoe import MCTS


class GameWindow(Tk):
    def __init__(self, model):
        super().__init__()
        self.title("MCTS Project")
        """
        self.configure(bg="#333333", padx=10, pady=10)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{screen_width//2}x{screen_height//2}')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        """
        self.configure(padx=10, pady=10)
  
        normal_font = tkFont.Font(family="Helvetica", size=16)
        self.option_add("*TCombobox*Listbox*Font", normal_font)
        self.title("MCTS Project")

        label1 = Label(self, text="Bienvenue dans notre simulateur !", font=("Helvetica", 20, 'bold'))
        label2 = Label(self, text="Vous jouez actuellement à : ", font=normal_font)
        label1.grid(column=0, row=0, padx=50)
        label2.grid(column=0, row=1, padx=50, pady=10)

        self.model = model
        self.mcts = MCTS()
        self.grid = GameGrid(self, model.height, model.width)

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

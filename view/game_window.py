from tkinter import Label, Button, Toplevel, DISABLED
import tkinter.font as tkFont

from itertools import product
from game.game_handler import MCTS
# from view.start_window import StartWindow A MODIF = on ajoute en paramètre la start window dans gamewindow
from view.grid import GameGrid
#from model.tictactoe import MCTS


class GameWindow(Toplevel):
    def __init__(self, model, startwindow):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
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
        self.startwindow = startwindow
        self.game = startwindow.game_choices[startwindow.gameChoice.get()]

        self.model = model
        self.mcts = MCTS()
        self.grid = GameGrid(self, model.height, model.width, self.game)
        self.rule_selection1 = self.model.rule_selection
        self.rule_selection2 = self.model.rule_selection2

        text_label2 = f"Grille de taille : {self.model.height}x{self.model.width}"
        player1_piece = "X" if self.game == 'tictactoe' else "BLACK"
        player2_piece = "O" if self.game == 'tictactoe' else "WHITE"

        if (self.game == 'tictactoe'):
            text_label2 += f"\nPions à aligner pour gagner : {self.startwindow.slider2.get()}"
        
        if (self.rule_selection1 == "Human"):
            text_label2 += f"\nJoueur 1 : Vous ({player1_piece})\nJoueur 2 : {self.rule_selection2} ({player2_piece})"
        elif (self.rule_selection2 == "Human"):
            text_label2 += f"\nJoueur 1 : {self.rule_selection1} ({player1_piece})\nJoueur 2 : Vous ({player2_piece})"
        else:
            text_label2 += f"\nJoueur 1 : {self.rule_selection1} ({player1_piece})\nJoueur 2 : {self.rule_selection2} ({player2_piece})"

        self.normal_font = tkFont.Font(family="Helvetica", size=16)
        self.option_add("*TCombobox*Listbox*Font", self.normal_font)
        self.title("MCTS Project")

        game = "du jeu de Go !" if self.game == 'go' else "de jeu du Morpion !"
        label1 = Label(self, text=f"Bienvenue dans notre simulateur {game}",
                       font=("Helvetica", 20, 'bold'))
        label2 = Label(
            self, text=text_label2, font=self.normal_font)
        label1.grid(column=0, row=0, padx=50)
        label2.grid(column=0, row=1, padx=50, pady=10)

        restart_button = Button(self, text="Rejouer",
                                font=self.normal_font, command=self.restart)
        restart_button.grid(column=0, row=1+self.model.height, pady=10)

        self.label3 = Label(self, text="", font=self.normal_font)
        self.label3.grid(column=0, row=2+self.model.height)
        self.update()

        #Si l'IA doit commencer
        if self.rule_selection1 != "Human":
            if self.rule_selection2 != "Human":
                print("------IA vs IA------")
                turn = 0
                while not self.model.is_win() and not self.model.is_draw():
                    if (turn%2==0):
                        self.model = self.model.game_turn_IA(self.mcts, self.rule_selection1)
                        self.grid.render(self.model.render())
                        self.update()
                    else:
                        self.model = self.model.game_turn_IA(self.mcts, self.rule_selection2)
                        self.grid.render(self.model.render())
                        self.update()
            else: #
                print("------IA vs Human------")
                self.model = self.model.game_turn_IA(self.mcts, self.rule_selection1)
                self.grid.render(self.model.render())
                self.update()

        

    def play(self, pos):

        if not self.model.is_valid_move(*pos):
            print("Invalid move")
            return

        if (not self.model.is_win() and not self.model.is_draw()):

            print("un gagnant :", self.model.is_win())
            print("match nul :", self.model.is_draw())

            if (self.rule_selection1!= "Human" and self.rule_selection2 == "Human"):
                print("1) IA contre Humain")
                self.model = self.model.game_turn_player(pos)
                self.grid.render(self.model.render())
                self.update()
                self.model = self.model.game_turn_IA(self.mcts, self.rule_selection1)
                self.grid.render(self.model.render())
                self.update()

            elif (self.rule_selection1 == "Human" and self.rule_selection2 != "Human"):
                print("2) Humain contre IA")
                self.model = self.model.game_turn_player(pos)
                self.grid.render(self.model.render())
                self.update()
                self.model = self.model.game_turn_IA(self.mcts, self.rule_selection2)
                self.grid.render(self.model.render())
                self.update()

            else :  #(self.rule_selection1 == "Human" and self.rule_selection2 == "Human"):
                print("3) Humain contre Humain")
                self.model = self.model.game_turn_player(pos)
                self.grid.render(self.model.render())
                self.update()

            if (self.model.is_win() or self.model.is_draw()):
                self.changeText("La partie est terminée")
                for i,j in product(range(self.model.height, self.model.width)):
                    self.cases[i][j]["state"] = DISABLED
                self.update()

    def changeText(self, message):
        self.label3['text'] = message  # A MODIFIER : Rajouter qui a gagné

    def restart(self):
        self.destroy()
        self.startwindow.deiconify()

    def on_closing(self):
        self.destroy()
        self.startwindow.destroy()


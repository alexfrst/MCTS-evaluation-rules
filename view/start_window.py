from view.game_window import GameWindow
from model.tictactoe import TicTacToeBoard
from model.go import GoBoard

from tkinter import Tk, Label, Frame, Button, Scale
import tkinter.ttk as ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk


class StartWindow(Tk):

    def __init__(self):
        super().__init__()

        normal_font = tkFont.Font(family="Helvetica", size=16)
        self.option_add("*TCombobox*Listbox*Font", normal_font)
        self.title("MCTS Project")
        self.img = ImageTk.PhotoImage(Image.open("./images/games.png").resize((330, 130)))
        self.game_choices = {"Tic Tac Toe (Morpion)" : "tictactoe", "Jeu de Go" : "go"}
        self.selection_rule_choices = {"MCTS - UCB Rule" : "UCB", "MCTS - IMED Rule" : "IMED", "Jeu aléatoire" : "random", "Un humain" : "Human"}

        #Different elements of our GUI
        label1 = Label(self, text="Bienvenue dans notre simulateur !", font=("Helvetica", 20, 'bold'))
        label2 = Label(self, text="Vous devez dans un premier temps sélectionner un jeu parmis ceux proposés, \nainsi que sélectionner les joueurs qui s'affronteront.\nCela peut être une IA jouant grâce à l'algorithme MCTS (plusieurs règles de sélection possible), \nou bien des humains.", font=normal_font)
        label1.pack(padx=50)
        label2.pack(padx=50, pady=10)

        panel = Label(self, image = self.img)
        panel.pack()

        frame1 = Frame(self)
        frame1.pack(padx=50, pady=10)
        Label(frame1, text="Choisissez un jeu : ", font=normal_font).pack(side='left')
        self.gameChoice = ttk.Combobox(frame1, values=list(self.game_choices.keys()), font=normal_font,  width=22)
        self.gameChoice.pack(side='left')
        self.gameChoice.current(0)

        self.slider = Scale(self, orient='horizontal', from_=3, to=19, tickinterval=2, length=350, label='Choisissez la taille de la grille (t x t) : ', font = normal_font, troughcolor="#e88032", activebackground = "#a15017")
        self.slider.pack()

        frame2 = Frame(self)
        frame2.pack(padx=50, pady=10)
        Label(frame2, text="Joueur 1 : ", font=normal_font).pack(side='left')
        self.player1 = ttk.Combobox(frame2, values=list(self.selection_rule_choices.keys()), font=normal_font)
        self.player1.pack(side='left')
        self.player1.current(0)

        frame3 = Frame(self)
        frame3.pack(padx=50, pady=10)
        Label(frame3, text="Joueur 2 : ", font=normal_font).pack(side='left')
        self.player2 = ttk.Combobox(frame3, values=list(self.selection_rule_choices.keys()), font=normal_font)
        self.player2.pack(side='left')
        self.player2.current(3)

        start_button = Button(self, text ="Commencer", font=normal_font, command = self.startGame)
        start_button.pack(pady=10)


    def startGame(self):

        selected_game = self.game_choices[self.gameChoice.get()]
        size = int(self.slider.get())
        player1 = self.selection_rule_choices[self.player1.get()]
        player2 = self.selection_rule_choices[self.player2.get()]

        game_args = {"size" : size, "rule_selection1" : player1, "rule_selection2" : player2}

        print("Nous pouvons commencer à jouer !")
        print(f"Jeu choisi : {selected_game}\nTaille de la grille : {size}\nJoueur 1 : {player1}\nJoueur 2 : {player2}")
        
        # Hide the main window
        self.withdraw()

        if (selected_game == "tictactoe"):
            game = GameWindow(TicTacToeBoard(**game_args), self)
            game.mainloop()

        else: #go
            game = GameWindow(GoBoard(**game_args), self)
            game.mainloop()


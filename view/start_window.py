from view.game_window import GameWindow
from model.tictactoe import Board

from tkinter import Tk, Label, Frame, Button
import tkinter.ttk as ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk


class StartWindow(Tk):

    def __init__(self):
        super().__init__()

        normal_font = tkFont.Font(family="Helvetica", size=16)
        self.option_add("*TCombobox*Listbox*Font", normal_font)
        self.title("MCTS Project")

        label1 = Label(self, text="Bienvenue dans notre simulateur !", font=("Helvetica", 20, 'bold'))
        label2 = Label(self, text="Vous devez dans un premier temps sélectionner un jeu parmis ceux proposés, \nainsi que sélectionner les joueurs qui s'affronteront.\nCela peut être une IA jouant grâce à l'algorithme MCTS (plusieurs règles de sélection possible), \nou bien des humains.", font=normal_font)
        label1.pack(padx=50)
        label2.pack(padx=50, pady=10)

        self.img = ImageTk.PhotoImage(Image.open("./images/games.png").resize((330, 130)))
        panel = Label(self, image = self.img)
        panel.pack()

        frame1 = Frame(self)
        frame1.pack(padx=50, pady=10)
        Label(frame1, text="Choisissez un jeu : ", font=normal_font).pack(side='left')
        self.gameChoice = ttk.Combobox(frame1, values=["Tic Tac Toe (Morpion)", "Jeu de Go"], font=normal_font)
        self.gameChoice.pack(side='left')
        self.gameChoice.current(0)

        frame2 = Frame(self)
        frame2.pack(padx=50, pady=10)
        Label(frame2, text="Joueur 1 : ", font=normal_font).pack(side='left')
        self.player1 = ttk.Combobox(frame2, values=["MCTS - UCB Rule", "MCTS - IMED Rule", "Un humain"], font=normal_font)
        self.player1.pack(side='left')
        self.player1.current(0)

        frame3 = Frame(self)
        frame3.pack(padx=50, pady=10)
        Label(frame3, text="Joueur 2 : ", font=normal_font).pack(side='left')
        self.player2 = ttk.Combobox(frame3, values=["MCTS - UCB Rule", "MCTS - IMED Rule", "Un humain"], font=normal_font)
        self.player2.pack(side='left')
        self.player2.current(2)

        start_button = Button(self, text ="Commencer", font=normal_font, command = self.startGame)
        start_button.pack(pady=10)

    def startGame(self):
        print("Nous pouvons commencer à jouer !")
        print("Le jeu choisi est :", self.gameChoice.get())
        print("Joueur 1 :", self.player1.get())
        print("Joueur 2 :", self.player2.get())
        #Destroy main window
        self.destroy()

        #A CHANGER : appeler BoardGo ou BoardTictacToe et leur donner les 2 joueurs en argument
        rule_selection = 'UCB'
        game = GameWindow(Board(rule_selection=rule_selection))
        game.mainloop()


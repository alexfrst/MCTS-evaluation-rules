from tkinter import Tk, Label, Button, StringVar
import tkinter.font as tkFont
from game.game_handler import MCTS
#from view.start_window import StartWindow A MODIF = on ajoute en paramètre la start window dans gamewindow
from view.grid import GameGrid
#from model.tictactoe import MCTS


class GameWindow(Tk):
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
  
        self.normal_font = tkFont.Font(family="Helvetica", size=16)
        self.option_add("*TCombobox*Listbox*Font", self.normal_font)
        self.title("MCTS Project")

        label1 = Label(self, text="Bienvenue dans notre simulateur !", font=("Helvetica", 20, 'bold'))
        label2 = Label(self, text="Vous jouez actuellement à : A MODIFIER", font=self.normal_font) 
        label1.grid(column=0, row=0, padx=50)
        label2.grid(column=0, row=1, padx=50, pady=10)

        self.model = model
        self.mcts = MCTS()
        self.grid = GameGrid(self, model.height, model.width)

        restart_button = Button(self, text ="Rejouer", font=self.normal_font, command = self.restart)
        restart_button.grid(column=0, row=1+self.model.height, pady=10)

        self.label3 = Label(self, text="", font=self.normal_font) 
        self.label3.grid(column=0, row=2+self.model.height)
        self.update()

        if self.model.rule_selection != "Human":
             self.model = self.model.game_turn_IA(self.mcts, self.model.rule_selection)
             self.grid.render(self.model.position)
             self.update()


        

    def play(self, pos):

        rule_selection1 = self.model.rule_selection
        rule_selection2 = self.model.rule_selection2

        if rule_selection1== "Human" or rule_selection2== "Human": #Humain VS IA

            if rule_selection1== "Human":
                self.model = self.model.game_turn_player(pos)
                self.grid.render(self.model.position)
                self.update()
                self.model = self.model.game_turn_IA(self.mcts, rule_selection2)
                self.grid.render(self.model.position)
                self.update()
                self.changeText()
            else:
                self.model = self.model.game_turn_IA(self.mcts, rule_selection1)
                self.grid.render(self.model.position)
                self.update()
                self.model = self.model.game_turn_player(pos)
                self.grid.render(self.model.position)
                self.update()
                self.changeText()

        else:
            print("Dans le else")
            self.model = self.model.game_turn_IA(self.mcts, rule_selection1)
            self.grid.render(self.model.position)
            self.update()
            self.model = self.model.game_turn_IA(self.mcts, rule_selection2)
            self.grid.render(self.model.position)
            self.update()
            self.changeText()


    def changeText(self):
        self.label3['text'] = "update" #A MODIFIER : Rajouter qui a gagné

    def restart(self):
        self.destroy()
        self.startwindow.deiconify()

    def on_closing(self):
        self.destroy()
        self.startwindow.destroy()

class MyModel:
    def __init__(self):
        self.height = 8
        self.width = 8

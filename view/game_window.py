from tkinter import Label, Button, StringVar, Toplevel
import tkinter.font as tkFont
from game.game_handler import MCTS
#from view.start_window import StartWindow A MODIF = on ajoute en paramètre la start window dans gamewindow
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
  
        self.normal_font = tkFont.Font(family="Helvetica", size=16)
        self.option_add("*TCombobox*Listbox*Font", self.normal_font)
        self.title("MCTS Project")

        label1 = Label(self, text="Bienvenue dans notre simulateur !", font=("Helvetica", 20, 'bold'))
        label2 = Label(self, text="Vous jouez actuellement à : A MODIFIER", font=self.normal_font) 
        label1.grid(column=0, row=0, padx=50)
        label2.grid(column=0, row=1, padx=50, pady=10)

        self.model = model
        self.mcts = MCTS()
        self.grid = GameGrid(self, model.height, model.width, self.game)

        restart_button = Button(self, text ="Rejouer", font=self.normal_font, command = self.restart)
        restart_button.grid(column=0, row=1+self.model.height, pady=10)

        self.label3 = Label(self, text="", font=self.normal_font) 
        self.label3.grid(column=0, row=2+self.model.height)
        self.update()

        self.rule_selection1 = self.model.rule_selection
        self.rule_selection2 = self.model.rule_selection2

        #Si l'IA doit commencer
        if self.rule_selection1 != "Human":
            if self.rule_selection2 != "Human":
                print("------IA vs IA------")
                turn = 0
                while not self.model.is_win() and not self.model.is_draw():
                    if (turn%2==0):
                        self.model = self.model.game_turn_IA(self.mcts, self.rule_selection1)
                        self.grid.render(self.model.position)
                        self.update()
                    else:
                        self.model = self.model.game_turn_IA(self.mcts, self.rule_selection2)
                        self.grid.render(self.model.position)
                        self.update()
            else: #
                print("------IA vs Human------")
                self.model = self.model.game_turn_IA(self.mcts, self.rule_selection1)
                self.grid.render(self.model.position)
                self.update()

        

    def play(self, pos):

        if (self.rule_selection1!= "Human" and self.rule_selection2 == "Human"):
            print("1) IA contre Humain")
            self.model = self.model.game_turn_player(pos)
            self.grid.render(self.model.position)
            self.update()
            self.model = self.model.game_turn_IA(self.mcts, self.rule_selection1)
            self.grid.render(self.model.position)
            self.update()

        elif (self.rule_selection1 == "Human" and self.rule_selection2 != "Human"):
            print("2) Humain contre IA")
            self.model = self.model.game_turn_player(pos)
            self.grid.render(self.model.position)
            self.update()
            self.model = self.model.game_turn_IA(self.mcts, self.rule_selection2)
            self.grid.render(self.model.position)
            self.update()

        else :  #(self.rule_selection1 == "Human" and self.rule_selection2 == "Human"):
            print("3) Humain contre Humain")
            self.model = self.model.game_turn_player(pos)
            self.grid.render(self.model.position)
            self.update()


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

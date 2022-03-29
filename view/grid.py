from tkinter import Button, Frame, DISABLED, NORMAL, Canvas, Label
from functools import partial

from PIL import Image, ImageTk

class GameGrid:
    def __init__(self, window, height, width, game):
        # On appelle le constructeur parent
        super().__init__()
        self.game = game
        self.gridFrame = Frame(window)
        self.gridFrame.grid(column=0, row=2)#, sticky="nswe")
        self.cases = []
        self.frame_width = int(500/width)
        self.frame_height = int(500/height)

        # Images de fond pour le jeu de Go
        self.background_img = ImageTk.PhotoImage(Image.open("./images/go.png").resize((self.frame_width, self.frame_height)))
        self.player_white = ImageTk.PhotoImage(Image.open("./images/go_white.png").resize((self.frame_width, self.frame_height)))
        self.player_black = ImageTk.PhotoImage(Image.open("./images/go_black.png").resize((self.frame_width, self.frame_height)))

        for i in range(height):
            self.cases.append([])
            for j in range(width):

                frame = Frame(self.gridFrame, width=self.frame_width, height=self.frame_height)

                if (self.game == "tictactoe"):
                    button = Button(frame, bg= "#595959", borderwidth=5, font= ("Arial", 20, "bold") if width>9 else ("Arial", 50, "bold"), command=partial(window.play,(i,j)))
                    padx = 10 if width<7 else 3
                    pady = 10 if width<7 else 3
                
                else : #go
                    button = Button(frame, borderwidth=0, image=self.background_img, command=partial(window.play,(i,j)))
                    padx = 0
                    pady = 0

                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                self.cases[i].append(button)
                frame.grid(row=i, column=j, sticky= "nswe", padx= padx, pady= pady) #put frame where the button should be
                button.grid(sticky="wens")



    def disable_button(self, button):
        i,j = button
        self.cases[i][j]["state"] = DISABLED

    def enable_button(self, button):
        i,j = button
        self.cases[i][j]["state"] = NORMAL

    def update_button_content(self, button , color, label):
        i,j = button
        self.cases[i][j]["text"] = label
        self.cases[i][j]["bg"] = color

    def update_button_content_go(self, button, player):
        i,j = button
        if player == ".":
            self.cases[i][j]["image"] = self.background_img
        elif player == "white":
            self.cases[i][j]["image"] = self.player_white
        else: #black
            self.cases[i][j]["image"] = self.player_black


    def render(self,positions):
        print(positions)
        if isinstance(positions, dict):
            for pos in positions:
                if positions[pos] == "x":
                    self.update_button_content(pos ,"#FF0000", "X")
                    self.disable_button(pos)

                if positions[pos] == "o":
                    self.update_button_content(pos ,"#0000FF", "O")
                    self.disable_button(pos)
        else:
            for row in range(len(positions)):
                for col in range(len(positions[0])):
                    pos = row,col
                    if positions[pos] == ".":
                        self.update_button_content_go(pos, ".")
                    if positions[pos] == "x":
                        self.update_button_content_go(pos, "black")
                    if positions[pos] == "o":
                        self.update_button_content_go(pos, "white")





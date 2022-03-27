from tkinter import Button, Frame, DISABLED, NORMAL
from functools import partial


class GameGrid:
    def __init__(self, window, height, width):
        # On appelle le constructeur parent
        super().__init__()
        self.gridFrame = Frame(window)
        self.gridFrame.grid(column=0, row=2)#, sticky="nswe")
        self.cases = []
        self.frame_width = 500/width
        self.frame_height = 500/height

        for i in range(height):
            self.cases.append([])
            for j in range(width):
                
                frame = Frame(self.gridFrame, width=self.frame_width, height=self.frame_height)
                button = Button(frame, bg= "#595959", borderwidth=5, font= ("Arial", 20, "bold") if width>9 else ("Arial", 50, "bold"), command=partial(window.play,(i,j)))
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                self.cases[i].append(button)
                frame.grid(row=i, column=j, sticky= "nswe", padx= 10 if width<7 else 3, pady= 10 if width<7 else 3) #put frame where the button should be
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


    def render(self,positions):
        if isinstance(positions, dict):
            for pos in positions:
                if positions[pos] == "x":
                    self.update_button_content(pos ,"#FF0000", "X")
                    self.disable_button(pos)
                if positions[pos] == "o":
                    self.update_button_content(pos ,"#0000FF", "O")
                    self.disable_button(pos)
        else:
            print("A modifier avec le jeu de GO")
            for row in range(len(positions)):
                for col in range(len(positions[0])):
                    pos = row,col
                    if positions[pos] == 0:
                        self.enable_button(pos)
                    if positions[pos] == 1:
                        self.update_button_content(pos, "#555555", "X")
                        self.disable_button(pos)
                    if positions[pos] == 2:
                        self.update_button_content(pos, "#FFFFFF", "O")
                        self.disable_button(pos)





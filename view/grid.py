from tkinter import Button, Frame, DISABLED, NORMAL
from functools import partial

default_button_style = {
    "bg": "#595959", "fg": "white", "highlightthickness": 0,
    "font": ("Arial", 25, "bold"),
    "borderwidth":10,
    "width": 5,
    "height": 2
}
grid_dict = {"sticky": "nswe", "padx": 10, "pady": 10}


class GameGrid:
    def __init__(self, window, height, width):
        # On appelle le constructeur parent
        super().__init__()
        self.gridFrame = Frame(window)
        self.gridFrame.grid(column=0, row=2)#, sticky="nswe")
        self.cases = []

        for i in range(height):
            self.cases.append([])
            for j in range(width):
                button = Button(self.gridFrame, **default_button_style, command=partial(window.play,(i,j)))
                self.cases[i].append(button)
                button.grid(row=i, column=j, **grid_dict)

    def disable_button(self, button):
        i,j = button
        self.cases[i][j]["state"] = DISABLED
        self.cases[i][j]["bg"] = "#898989"

    def enable_button(self, button):
        i,j = button
        self.cases[i][j]["state"] = NORMAL
        self.cases[i][j]["bg"] = "#898989"

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





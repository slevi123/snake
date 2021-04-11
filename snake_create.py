from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import Label as OLabel
from ttkwidgets.color import ColorPicker, ColorSquare, askcolor
from tkinter.colorchooser import askcolor

class ColorDisplayBox(OLabel):
    def __init__(self, parent, color):
        super().__init__(parent, bg=color, relief="groove", text='        ')
        self.bind("<Button-1>", self.color_choosing)
    
    def color_choosing(self, event=None):
        if t := askcolor()[1]:
            self.config(bg=t)

class SnakeCreate(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ColorDisplayBox(self, 'red').grid()
        Entry(self, text='kigyo neve').grid(column=1, row=0)
        Button(self, text = 'Add Snake').grid(row=1, columnspan=2)

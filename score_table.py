from tkinter.ttk import Label
from tkinter import StringVar

class ScoreTable(Label):
    def __init__(self, parent):
        self.score = StringVar()
        super().__init__(parent, textvariable=self.score)
        self.score.set('0')
from tkinter.ttk import Frame, Button


class GameControl(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.game = None

        self.start_button = Button(self, text="START")
        self.start_button.pack()


    def load_game(self, game):
        self.game=game
        self.start_button.config(command=self.game.start)
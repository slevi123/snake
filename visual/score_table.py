from tkinter import Label
from tkinter import StringVar, Frame
from program_config import main_game_frame
from snake import Snake

font_type = "sans-sheriff"


class SnakeStat(Frame):
    def __init__(self, parent, snake, visibility=True):
        super().__init__(parent, width=90, height=9)
        self.snake = snake

        if visibility:
            Label(self, text=snake.name, fg=snake.color, font=(font_type, 14)).pack()
        else:
            Label(self, text="      ", bg=snake.color, font=(font_type, 14)).pack()

        self.score = StringVar()
        Label(self, textvariable=self.score, fg=snake.color).pack()
        self.score.set('0')

    def update_score(self):
        self.score.set(str(self.snake.score))


class ScoreTable(Frame):
    def __init__(self, parent):
        sizes = main_game_frame.SCOREBOARD_SIZE
        super().__init__(parent, height=sizes.y, width=sizes.x)
        self.pack_propagate(0)

        Label(self, text="").pack()
        self.winfo_toplevel().bind("<<GameStarted>>", self.draw)

    def draw(self, event=None):
        visibility = len(Snake.snakes_alive) <= 6
        for child in self.winfo_children():
            child.pack_forget()
            child.destroy()
        for snake in Snake.snakes_alive:
            SnakeStat(self, snake, visibility).pack(side="left", padx=4)

    def update_scores(self, event=None):
        for child in self.winfo_children():
            if child.snake.alive:
                child.update_score()


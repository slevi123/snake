from tkinter.ttk import LabelFrame

from logic.game import Game
from visual.scrollable_frame import ScrollableFrame
from tkinter import Label, Frame, Button
import program_config as consts

font_type = "sans-sheriff"


class SnakeListItem(Frame):
    def __init__(self, parent, snake, del_command):
        self.snake = snake
        super().__init__(parent, width=consts.SNAKE_HANDLERS_WIDTH, height=consts.LISTITEM_HEIGHT,
                         bg=snake.color, border=2, relief="groove")
        self.grid_propagate(0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        Label(self, text=snake.name, bg=snake.color, font=(font_type, "12")).grid(column=0)
        Label(self, text=snake.button_string, bg=snake.color, font=(font_type, "10")).grid(column=0, row=1)
        self.del_button = Button(self, text="X", command=lambda: del_command(self), bg=snake.color,
                                 relief="solid", border=1, height=consts.LISTITEM_HEIGHT, width=6)
        self.del_button.grid(column=1, row=0, sticky="e", rowspan=2)

    def disable_delete(self):
        self.del_button.config(state="disable", border=0)

    def enable_delete(self):
        self.del_button.config(state="normal", border=2)


class SnakeLister(LabelFrame):
    def __init__(self, parent, game, starting_handler):
        super().__init__(parent, text="Snakes in game:")
        self.scrollable_frame = ScrollableFrame(self, width=consts.SNAKE_HANDLERS_WIDTH,
                                                height=consts.SNAKELISTERS_HEIGHT)

        self.starting_handler = starting_handler
        self.game = game
        self.winfo_toplevel().bind("<<SnakeModelsChanged>>", self.update_list, add=True)
        # TODO: solve unbindind if needed
        self.winfo_toplevel().bind("<<GameStarted>>", self.disable_deleting, add=True)
        self.winfo_toplevel().bind("<<GameEnded>>", self.enable_deleting, add=True)
        self.scrollable_frame.pack()

    def update_list(self, event=None):
        for listitem in self.scrollable_frame.interior.winfo_children():
            listitem.pack_forget()
            listitem.destroy()
        for snake in self.starting_handler.snakes:
            SnakeListItem(self.scrollable_frame.interior, snake, self.delete_item).pack()

    def delete_item(self, listitem):
        self.starting_handler.snakes.remove(listitem.snake)
        listitem.pack_forget()
        listitem.destroy()

    def disable_deleting(self, event=None):
        for listitem in self.scrollable_frame.interior.winfo_children():
            listitem.disable_delete()

    def enable_deleting(self, event=None):
        for listitem in self.scrollable_frame.interior.winfo_children():
            listitem.enable_delete()

from tkinter.ttk import Frame, Button

from logic.services import add_image2tk_widget
from program_config import main_game_frame, START_DELAY
from functools import wraps

button_size = main_game_frame.GM_CONTROL_BSIZE


def event_blocker(function):
    """Long keypresses could result in multiple game loops.
    This decorator fixes this type of behavior.

    Meant to be used on methods, within a class with block() method,
    which automatically deblocks after a certain time."""
    @wraps(function)  # making sure function knows her identity and documentation.
    def new_function(self, *args, **kwargs):
        if not self.event_block:
            function(self, *args, **kwargs)
            self.block()
    return new_function


class GameControl(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.game = None
        self.event_block = False

        self.start_button = Button(self, text="START/PAUSE", command=self.start_game)
        self.stop_button = Button(self, text="STOP", command=self.stop_game, state="disable")
        add_image2tk_widget(self.start_button, "res/png/start.png", resize=button_size.tuple)
        add_image2tk_widget(self.stop_button, "res/png/stop.png", resize=button_size.tuple)

        self.start_button.pack(side="left", padx=6)
        self.stop_button.pack(side="left", padx=6)

        self.winfo_toplevel().bind("<<GameEnded>>", self.reactivate_starting)
        self.winfo_toplevel().bind("<space>", self.start_game)

    def deblock(self):
        self.event_block = False

    def block(self):
        """Long button presses caused multiple loops running simultanously."""
        self.event_block = True

        self.winfo_toplevel().after(500, self.deblock)

    def load_game(self, game):
        self.game = game

    @event_blocker
    def start_game(self, event=None):
        if self.game.start():
            self.start_button.config(command=self.pause_game)
            add_image2tk_widget(self.start_button, "res/png/pause.png", resize=button_size.tuple)
            self.winfo_toplevel().bind("<space>", self.pause_game)

            self.stop_button.config(state="normal")
            self.winfo_toplevel().bind("<Escape>", self.stop_game)

            self.game.map_canvas.delete_message()

    @event_blocker
    def reactivate_starting(self, event=None):
        add_image2tk_widget(self.start_button, "res/png/start.png", resize=button_size.tuple)
        self.start_button.config(command=self.start_game)
        self.winfo_toplevel().bind("<space>", self.start_game)
        self.stop_button.config(state="disable")
        self.winfo_toplevel().unbind("<Escape>")

    @event_blocker
    def stop_game(self, event=None):
        self.game.map_canvas.message("Game Stopped")
        self.game.in_game = False
        self.game.paused = False
        self.game.loop()

    @event_blocker
    def pause_game(self, event=None):
        self.game.paused = True
        self.game.map_canvas.message("Game Paused")
        add_image2tk_widget(self.start_button, "res/png/start.png", resize=button_size.tuple)
        self.start_button.config(command=self.pause_continue)
        self.winfo_toplevel().bind("<space>", self.pause_continue)

    @event_blocker
    def pause_continue(self, event=None):
        add_image2tk_widget(self.start_button, "res/png/pause.png", resize=button_size.tuple)
        self.start_button.config(command=self.pause_game)
        self.winfo_toplevel().bind("<space>", self.pause_game)

        self.game.map_canvas.delete_message()

        self.game.paused = False
        self.game.unpause()
        self.winfo_toplevel().after(START_DELAY, self.game.loop)


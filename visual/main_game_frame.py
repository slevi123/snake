from tkinter import Frame, Button

from logic.game import Game
from logic.starting_handler import StartingHandler
from visual.game_control_menu import GameControl
from visual.info_frame import InfoFrame
from visual.map_canvas import MapCanvas
from visual.score_table import ScoreTable
from visual.snake_creator_frame import SnakeCreate
from visual.snake_lister_frame import SnakeLister
from program_config import main_game_frame


class MainGameFrame(Frame):
    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.grid_components()

    def grid_components(self):
        start_handler = StartingHandler()

        sc = ScoreTable(self)
        map_sizes = main_game_frame.MAP_SIZE
        mc = MapCanvas(self, width=map_sizes.x, height=map_sizes.y)
        mc.grid(row=1, rowspan=3, padx=0, pady=0, sticky='sw')
        game = Game(self, mc, sc, start_handler)
        gc = GameControl(self)
        SnakeLister(self, game, start_handler).grid(row=1, column=1, padx=0, pady=8, sticky="nw")
        SnakeCreate(self, start_handler).grid(row=2, column=1, sticky="nw", pady=8)
        InfoFrame(self).grid(row=3, column=1, sticky="e", pady=8)

        sc.grid(row=0, column=0)
        gc.grid(row=0, column=1)
        gc.load_game(game)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

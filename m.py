from random import seed
from game import Game
from snake import Snake

import tkinter as tk
from map_canvas import MapCanvas
from score_table import ScoreTable
from snake_create import SnakeCreate
from game_control_menu import GameControl


seed()
root = tk.Tk()
root.title('Snake')
# Snake.head_icon = PhotoImage(Snake.head_icon_image)

ScoreTable(root).grid(row=0)
mc = MapCanvas(root)
mc.grid(row=1)
SnakeCreate(root).grid(row=1, column=1)

game = Game(root, mc)
gc = GameControl(root)

gc.grid(row=0, column=2)

gc.load_game(game)

root.mainloop()

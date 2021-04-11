import tkinter as tk
from map import Map
from random import seed

from score_table import ScoreTable
from snake_create import SnakeCreate


seed()
root = tk.Tk()
root.title('Snake')

ScoreTable(root).grid(row=0)
Map(root).grid(row=1)
SnakeCreate(root).grid(row=1, column=1)

root.mainloop()

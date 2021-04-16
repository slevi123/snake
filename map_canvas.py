from tkinter import Canvas
import gconsts as consts
from snake import Snake

class MapCanvas(Canvas):
    def __init__(self, root):
        super().__init__(root, bd=8, relief='sunken',
        bg=consts.MAP_BG, height=consts.MAP_HEIGHT,width=consts.MAP_WIDTH)

        self.map = None

    def load_map(self, map_):
        self.map = map_
        map_.canvas = self
        self.map._init_map_()

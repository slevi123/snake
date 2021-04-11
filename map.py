from tkinter import Canvas
import gconsts as consts
from barrier import SquareBarrier
from snake import Snake

class Map(Canvas):
    def __init__(self, root):
        super().__init__(root, bd=8, relief='sunken',
        bg=consts.MAP_BG, height=consts.MAP_HEIGHT,width=consts.MAP_WIDTH)

        self.barriers = [ SquareBarrier(50, 100,'black', 100) ]
        self.barriers[0].draw(self)

        Snake(self, 'red')
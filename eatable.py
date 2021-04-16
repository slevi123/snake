import gconsts as consts

from random import randrange


class Eatable:
    r = 10
    def __init__(self, map_, x = None, y = None):
        self.map = map_

        if x:
            self.x = x
        else:
            self.x = randrange(consts.START_MARGIN[0], consts.MAP_WIDTH - consts.START_MARGIN[0])

        if y:
            self.y = y
        self.y = randrange(consts.START_MARGIN[1], consts.MAP_HEIGHT- consts.START_MARGIN[1])

    def plot(self):
        self.map.canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)

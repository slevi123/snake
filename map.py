from barrier import SquareBarrier


class Map:
    def __init__(self):
        self.barriers = [ SquareBarrier(50, 100,'black', 100) ]
        self.canvas = None

    def _init_map_(self):
        self.barriers[0].draw(self)

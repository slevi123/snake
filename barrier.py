class Barrier():
    def __init__(self, x,y, color, size=None):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

        self.draw_id = None

    def draw(self, map):
        pass

    def delete(self, map):
        pass

class SquareBarrier(Barrier):

    def draw(self, map_, level=""):
        self.draw_id = map_.canvas.create_rectangle(self.x, self.y, self.x+self.size, self.y+self.size, 
        fill=self.color, tag="barrier")

    def delete(self, map_):
        map_.canvas.delete(self.draw_id)
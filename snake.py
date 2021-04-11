import gconsts as consts
from random import randrange

class Snake:
    size = 60

    def __init__(self, map_, color):
        self.map = map_
        self.shape = None

        self.wallwalker = False
        self.color = color
        self.speed = 10 #consts.BASE_SPEED
        self.x = randrange(0, consts.MAP_WIDTH)
        self.y = randrange(0, consts.MAP_HEIGHT)

        self.move_bind_table = {
            'up' : 'w',
            'down' : 's',
            'left' : 'd',
            'right' : 'a'
        }

        self.bind_ids = []

        self.coords = (self.x, self.y, self.x+self.size, self.y+self.size)

        self.draw()
        self.bind_events()

    def bind_events(self):
        self.bind_ids = [
            self.map.winfo_toplevel().bind(self.move_bind_table['up'], self.move_up),
            self.map.winfo_toplevel().bind(self.move_bind_table['down'], self.move_down),
            self.map.winfo_toplevel().bind(self.move_bind_table['left'], self.move_left),
            self.map.winfo_toplevel().bind(self.move_bind_table['right'], self.move_right),
        ]

    def draw(self):
        self.shape = self.map.create_rectangle(*self.coords,
        fill = self.color)

    def move_up(self, event=None):
        if self.y - self.speed >= 0:
            self.y -= self.speed
            self.map.move(self.shape, 0, - self.speed)
        elif self.wallwalker:
            temp_y = consts.MAP_HEIGHT-self.size
            self.map.move(self.shape, 0, temp_y-self.y)
            self.y = temp_y
        else:
            self.map.move(self.shape, 0, -self.y)
            self.y = 0
            self.kill()

        if self.is_there_barrier():
            self.kill()

    def move_down(self, event=None):
        if self.y + self.speed <= consts.MAP_HEIGHT - self.size:
            self.y += self.speed
            self.map.move(self.shape, 0, self.speed)
        elif self.wallwalker:
            self.map.move(self.shape, 0, -self.y)
            self.y = 0
        else:
            temp_y = consts.MAP_HEIGHT-self.size
            self.map.move(self.shape, 0, temp_y-self.y)
            self.y = temp_y
            self.kill()

        if self.is_there_barrier():
            self.kill()

    def move_right(self, event=None):
        self.x -= self.speed
        self.map.move(self.shape, - self.speed, 0)

    def move_left(self, event=None):
        self.x += self.speed
        self.map.move(self.shape, self.speed, 0)

    def kill(self):
        print('kill')
        self.unbind_events()

    def unbind_events(self):
        print('events unbnd')
        for bind_id in self.bind_ids:
            print(bind_id)
            self.map.winfo_toplevel().unbind("",bind_id)

    def is_there_barrier(self):
        bbox = self.map.bbox(self.shape)
        overlappers = self.map.find_overlapping(*bbox)

        if overlappers:
            barrier_ids = self.map.find_withtag('barrier')
            for item in overlappers:
                if item in barrier_ids:
                    return True
        return False


    # def overlapping(self):
    #     bbox = self.map.bbox(self.shape)
    #     overlappers = self.map.find_overlapping(*bbox)
    #     return [x for x in overlappers if x!=self.shape]
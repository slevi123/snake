import gconsts as consts
from random import randrange, choice
from collections import deque

class Snake:
    size = 20
    snakes_alive = []

    def __init__(self, map_, color):
        self.map = map_
        self.head = None

        self.wallwalker = False
        self.color = color
        self.speed = consts.BASE_SPEED
        self.x = randrange(consts.START_MARGIN[0], consts.MAP_WIDTH - consts.START_MARGIN[0])
        self.y = randrange(consts.START_MARGIN[1], consts.MAP_HEIGHT- consts.START_MARGIN[1])

        self.safety = True
        self.alive = True
        self.direction = choice(('L', 'R', 'U', 'D'))
        self.shape_queue = deque([], consts.MAX_SNAKE_SIZE)
        self.pre_overlap = []

        # self.last_x = self.x
        # self.last_y = self.y

        self.move_bind_table = {
            'up' : 'w',
            'down' : 's',
            'left' : 'd',
            'right' : 'a'
        }


        self.snakes_alive.append(self)

        self.map.winfo_toplevel().after(3000, self.turn_off_safety)
        self.draw()
        self.bind_events()

    def turn_off_safety(self):
        self.safety = False

    @property
    def coords(self):
        return (self.x, self.y, self.x+self.size, self.y+self.size)

    def change_direction(self, new_dir):
        self.direction = new_dir
        # self.map.create_rectangle(self.last_x, self.last_y, self.x + self.size, self.y+self.size)

    def bind_events(self):
        self.bind_ids = [
            self.map.winfo_toplevel().bind(self.move_bind_table['up'], lambda e: self.change_direction('U')),
            self.map.winfo_toplevel().bind(self.move_bind_table['down'], lambda e: self.change_direction('D')),
            self.map.winfo_toplevel().bind(self.move_bind_table['left'], lambda e: self.change_direction('L')),
            self.map.winfo_toplevel().bind(self.move_bind_table['right'], lambda e: self.change_direction('R')),
        ]

    def draw(self):
        print('draw')
        self.head = self.map.create_rectangle(*self.coords,
        fill = self.color, tags = 'snake_body')

        if len(self.shape_queue) >= consts.MAX_SNAKE_SIZE:
            self.map.delete(self.shape_queue.popleft())
        self.shape_queue.append(self.head)
        self.pre_overlap.append(self.head)


    def move_up(self, event=None):
        if self.y - self.speed >= 0:
            self.y -= self.speed
            # self.map.move(self.head, 0, - self.speed)
        elif self.wallwalker:
            temp_y = consts.MAP_HEIGHT-self.size
            # self.map.move(self.head, 0, temp_y-self.y)
            self.y = temp_y
        else:
            # self.map.move(self.head, 0, -self.y)
            self.y = 0
            self.kill()
            return False
        return True

    def move_down(self, event=None):
        if self.y + self.speed <= consts.MAP_HEIGHT - self.size:
            self.y += self.speed
            # self.map.move(self.head, 0, self.speed)
        elif self.wallwalker:
            # self.map.move(self.head, 0, -self.y)
            self.y = 0
        else:
            temp_y = consts.MAP_HEIGHT-self.size
            # self.map.move(self.head, 0, temp_y-self.y)
            self.y = temp_y
            self.kill()
            return False
        return True

    def move_right(self, event=None):
        self.x -= self.speed
        # self.map.move(self.head, - self.speed, 0)
        return True

    def move_left(self, event=None):
        self.x += self.speed
        # self.map.move(self.head, self.speed, 0)
        return True

    def kill(self):
        self.alive = False
        self.snakes_alive.remove(self)
        self.unbind_events()
        

    def unbind_events(self):
        print('events unbnd')
        for bind_id in self.bind_ids:
            print(bind_id)
            self.map.winfo_toplevel().unbind("",bind_id)

    def is_there_barrier(self):
        bbox = self.map.bbox(self.head)
        overlappers = self.map.find_overlapping(*bbox)

        new_pre_overlappers = []
        for item in self.pre_overlap:
            if item in overlappers:
                new_pre_overlappers.append(item)
        self.pre_overlap = new_pre_overlappers

        if overlappers:
            barrier_ids = self.map.find_withtag('barrier')
            snake_bodies_ids = self.map.find_withtag('snake_body')
            for item in overlappers:
                if (item in barrier_ids) or (item in snake_bodies_ids):
                    if item not in self.pre_overlap:
                        return True

        return False

    def move(self):

        if self.direction == "U":
            self.move_up()
        elif self.direction == "D":
            self.move_down()
        elif self.direction == "R":
            self.move_right()
        elif self.direction == "L":
            self.move_left()

        if (not self.safety) and self.is_there_barrier():
            self.kill()

        self.draw()


    # def overlapping(self):
    #     bbox = self.map.bbox(self.head)
    #     overlappers = self.map.find_overlapping(*bbox)
    #     return [x for x in overlappers if x!=self.head]
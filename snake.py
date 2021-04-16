import gconsts as consts
from random import randrange, choice
from collections import deque

from PIL import Image
from PIL.ImageTk import PhotoImage
from services import complementary_color, rgb2hex


class Snake:
    size = 20
    snakes_alive = []

    head_icon_image = Image.open('./res/png/smil.png').resize((size, size), Image.ANTIALIAS)
    head_icon = None
    # head_icon = PhotoImage(head_icon_image)

    def __init__(self, game, color, move_bind_table=None):
        self.game = game
        self.head = None

        self.wallwalker = True
        self.color_rgb = color
        self.speed = consts.BASE_SPEED
        self.x = randrange(consts.START_MARGIN[0], consts.MAP_WIDTH - consts.START_MARGIN[0])
        self.y = randrange(consts.START_MARGIN[1], consts.MAP_HEIGHT- consts.START_MARGIN[1])

        self.safety = True
        self.alive = True
        self.direction = choice(('L', 'R', 'U', 'D'))
        self.shape_queue = deque([], consts.MAX_SNAKE_SIZE)
        self.pre_overlap = []

        self.last_x = self.x
        self.last_y = self.y

        if move_bind_table:
            self.move_bind_table = move_bind_table
        else:
            self.move_bind_table = {
                'up' : 'w',
                'down' : 's',
                'left' : 'a',
                'right' : 'd'
            }

        # self.head_icon = self.recolor_head_icon()
        self.head_visual = self.game.map.canvas.create_image(self.x, self.y, image=self.head_icon, anchor='nw')

        self.snakes_alive.append(self)

        self.game.map.canvas.winfo_toplevel().after(3000, self.turn_off_safety)
        self.draw()
        self.bind_events()

        # self.gif1 = PhotoImage(file='./res/gif/stickman.gif')

    @property
    def color(self):
        return rgb2hex(*self.color_rgb)  

    def recolor_head_icon(self, color=None):
        pass
    #     #get the color
    #     complementary = complementary_color(*self.color)

    #     #recolor the pic
    #     image = self.head_icon_image.copy()
    #     pixels = image.load()
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             pixels[i, j] = (*complementary, pixels[i, j][3])
    #     return PhotoImage(image)

    def turn_off_safety(self):
        self.safety = False

    @property
    def coords(self):
        return (self.x, self.y, self.x+self.size, self.y+self.size)

    # @property
    # def direction(self):
    #     return self.directions.

    def change_direction(self, new_dir):
        self.direction = new_dir
        self.last_x = self.x
        self.last_y = self.y

    def bind_events(self):
        self.bind_ids = [
            self.game.map.canvas.winfo_toplevel().bind(self.move_bind_table['up'], lambda e: self.change_direction('U')),
            self.game.map.canvas.winfo_toplevel().bind(self.move_bind_table['down'], lambda e: self.change_direction('D')),
            self.game.map.canvas.winfo_toplevel().bind(self.move_bind_table['left'], lambda e: self.change_direction('L')),
            self.game.map.canvas.winfo_toplevel().bind(self.move_bind_table['right'], lambda e: self.change_direction('R')),
            # self.game.map.canvas.winfo_toplevel().bind(self.move_bind_table['left'], lambda e: self.change_direction('L')),
            # self.game.map.canvas.winfo_toplevel().bind(self.move_bind_table['right'], lambda e: self.change_direction('R')),
        ]

    def draw(self):
        self.head = self.game.map.canvas.create_rectangle(*self.coords,
        fill = self.color, 
        width=0, tags = 'snake_body')

        if len(self.shape_queue) >= consts.MAX_SNAKE_SIZE:
            self.game.map.canvas.delete(self.shape_queue.popleft())
        self.shape_queue.append(self.head)
        self.pre_overlap.append(self.head)

        vc = self.game.map.canvas.coords(self.head_visual)
        self.game.map.canvas.move(self.head_visual, self.x-vc[0], self.y-vc[1])
        self.game.map.canvas.tag_raise(self.head_visual)

        # self.game.map.creatSAde_rectangle(self.last_x, self.last_y, self.x + self.size, self.y+self.size)

    def delete(self):
        while len(self.shape_queue):
            self.game.map.canvas.delete(self.shape_queue.popleft())

    def move_up(self, event=None):
        if self.y - self.speed >= 0:
            self.y -= self.speed
            # self.game.map.move(self.head, 0, - self.speed)
        elif self.wallwalker:
            # self.game.map.move(self.head, 0, temp_y-self.y)
            self.y = consts.MAP_HEIGHT-self.size
        else:
            # self.game.map.move(self.head, 0, -self.y)
            self.y = 0
            self.kill()

    def move_down(self, event=None):
        if self.y + self.speed <= consts.MAP_HEIGHT - self.size:
            self.y += self.speed
            # self.game.map.move(self.head, 0, self.speed)
        elif self.wallwalker:
            # self.game.map.move(self.head, 0, -self.y)
            self.y = 0
        else:
            # self.game.map.move(self.head, 0, temp_y-self.y)
            self.y = consts.MAP_HEIGHT-self.size
            self.kill()

    def move_left(self, event=None):
        if self.x - self.speed >= 0:
            self.x -= self.speed
        elif self.wallwalker:
            self.x = consts.MAP_WIDTH-self.size
        else:
            self.x = 0
            self.kill()

    def move_right(self, event=None):
        if self.x + self.speed <= consts.MAP_WIDTH - self.size:
            self.x += self.speed
            # self.game.map.move(self.head, 0, self.speed)
        elif self.wallwalker:
            # self.game.map.move(self.head, 0, -self.y)
            self.x = 0
        else:
            # self.game.map.move(self.head, 0, temp_y-self.y)
            self.x = consts.MAP_WIDTH-self.size
            self.kill()

    def kill(self):
        self.alive = False
        self.snakes_alive.remove(self)
        self.unbind_events()
        

    def unbind_events(self):
        print('events unbnd')
        for bind_id in self.bind_ids:
            print(bind_id)
            self.game.map.canvas.winfo_toplevel().unbind("",bind_id)

    def is_there_barrier(self):
        bbox = self.game.map.canvas.bbox(self.head)
        overlappers = self.game.map.canvas.find_overlapping(*bbox)

        new_pre_overlappers = []
        for item in self.pre_overlap:
            if item in overlappers:
                new_pre_overlappers.append(item)
        self.pre_overlap = new_pre_overlappers

        if overlappers:
            barrier_ids = self.game.map.canvas.find_withtag('barrier')
            snake_bodies_ids = self.game.map.canvas.find_withtag('snake_body')
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
    #     bbox = self.game.map.bbox(self.head)
    #     overlappers = self.game.map.find_overlapping(*bbox)
    #     return [x for x in overlappers if x!=self.head]
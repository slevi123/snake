from program_config import main_game_frame
import program_config as consts
from random import randrange
from collections import deque

from PIL import Image
from logic.services import rgb2hex
from logic.circular_list import DirectionCircle
from program_config import snake as snake_config

map_border = main_game_frame.MAP_BORDER


class Snake:
    size = 20
    snakes_alive = []

    # head_icon_image = Image.open('./res/png/smil.png').resize((size, size), Image.ANTIALIAS)
    # head_icon = None

    # head_icon = PhotoImage(head_icon_image)

    def __init__(self, game, snake_model):
        self.game = game
        self.head = None

        self.name = snake_model.name

        self.wallwalker = False
        self.color = snake_model.color
        self.speed = consts.BASE_SPEED  # TODO: refactor
        map_size = main_game_frame.MAP_SIZE
        # Indulhatnak egymasrol, mert van safety.
        blocked_size = main_game_frame.MAP_BLOCKEDSIZE
        self.x = self.gen_start_block(snake_config.START_GEN_MARGIN_BLOCKS.x, blocked_size.x, self.size)
        self.y = self.gen_start_block(snake_config.START_GEN_MARGIN_BLOCKS.y, blocked_size.y, self.size)

        self.score = 0

        self.slowing = False
        self.safety = True
        self.alive = True
        # self.direction = choice(('L', 'R', 'U', 'D'))
        self.shape_queue = deque([], consts.MAX_SNAKE_SIZE)  # TODO: create a new snake_visual class and bind it to snake
        self.pre_overlap = []

        self.last_x = self.x
        self.last_y = self.y

        # self.bind_ids = []
        self.eatable_timing_table = dict()

        self.move_bind_table = snake_model.move_bind_table

        self.direction_circle = DirectionCircle.random_direction()

        # self.head_icon = self.recolor_head_icon()
        # self.head_visual = self.game.map.canvas.create_image(self.x, self.y, image=self.head_icon, anchor='nw')

        self.snakes_alive.append(self)

        self.game.map.canvas.winfo_toplevel().after(3000, self.turn_off_safety)
        self.draw()
        # self.bind_events()

        # self.gif1 = PhotoImage(file='./res/gif/stickman.gif')

    @staticmethod
    def gen_start_block(margin_blocks, high, blocksize):
        return map_border + randrange(margin_blocks, high - margin_blocks) * blocksize

    def turn_off_safety(self):
        self.safety = False

    @property
    def coords(self):
        return self.x + 1, self.y + 1, self.x + self.size - 1, self.y + self.size - 1

    @property
    def direction(self):
        return self.direction_circle.data

    def change_direction(self, new_dir):
        # self.direction = new_dir
        if new_dir == 'L':
            self.direction_circle = self.direction_circle.left
        else:
            self.direction_circle = self.direction_circle.right
        # self.last_x = self.x
        # self.last_y = self.y

    # def bind_events(self):
        # self.bind_ids = [
        #     self.game.map.canvas.winfo_toplevel().bind(self.move_bind_table['left'],
        #                                                lambda e: self.change_direction('L')),
        #     self.game.map.canvas.winfo_toplevel().bind(self.move_bind_table['right'],
        #                                                lambda e: self.change_direction('R')),
        # ]
    def check_event(self, key):
        if key == self.move_bind_table["left"]:
            self.change_direction('L')
        elif key == self.move_bind_table["right"]:
            self.change_direction('R')

    def eatable_timing(self):
        # FIXME?: now this is loop speed dependant, not constant time
        # TODO: redesign loop to fit normal ms-s
        to_del = []
        for name, (count, callback) in self.eatable_timing_table.items():
            if count:
                self.eatable_timing_table[name][0] -= 1
            else:
                callback()
                to_del.append(name)
        for non_key in to_del:
            self.eatable_timing_table.pop(non_key)

    def draw(self):
        width = int(self.wallwalker)
        self.head = self.game.map.canvas.create_rectangle(*self.coords, fill=self.color, tags='snake_body', width=width)
        # TODO: it is a deque, so create kigyofarok.
        if len(self.shape_queue) >= consts.MAX_SNAKE_SIZE:
            self.game.map.canvas.delete(self.shape_queue.popleft())

        self.shape_queue.append(self.head)
        self.pre_overlap.append(self.head)

        # vc = self.game.map.canvas.coords(self.head_visual)
        # self.game.map.canvas.move(self.head_visual, self.x - vc[0], self.y - vc[1])
        # self.game.map.canvas.tag_raise(self.head_visual)

        # self.game.map.creatSAde_rectangle(self.last_x, self.last_y, self.x + self.size, self.y+self.size)

    def erase_shape(self):
        while len(self.shape_queue):
            self.game.map.canvas.delete(self.shape_queue.popleft())

    def delete(self):
        self.kill()
        self.erase_shape()
        # self.head

    def move_up(self, event=None):
        if self.y - self.speed >= map_border:
            self.y -= self.speed
            # self.game.map.move(self.head, 0, - self.speed)
        elif self.wallwalker:
            # self.game.map.move(self.head, 0, temp_y-self.y)
            self.y = main_game_frame.MAP_SIZE.y - map_border
        else:
            # self.game.map.move(self.head, 0, -self.y)
            self.y = map_border
            self.kill()

    def move_down(self, event=None):
        if self.y + self.speed <= main_game_frame.MAP_SIZE.y - map_border:
            self.y += self.speed
            # self.game.map.move(self.head, 0, self.speed)
        elif self.wallwalker:
            # self.game.map.move(self.head, 0, -self.y)
            self.y = map_border
        else:
            # self.game.map.move(self.head, 0, temp_y-self.y)
            self.y = main_game_frame.MAP_SIZE.y - map_border
            self.kill()

    def move_left(self, event=None):
        if self.x - self.speed >= map_border:
            self.x -= self.speed
        elif self.wallwalker:
            self.x = main_game_frame.MAP_SIZE.x - map_border
        else:
            self.x = map_border
            self.kill()

    def move_right(self, event=None):
        if self.x + self.speed <= main_game_frame.MAP_SIZE.x - map_border:
            self.x += self.speed
            # self.game.map.move(self.head, 0, self.speed)
        elif self.wallwalker:
            # self.game.map.move(self.head, 0, -self.y)
            self.x = map_border
        else:
            # self.game.map.move(self.head, 0, temp_y-self.y)
            self.x = main_game_frame.MAP_SIZE.x - map_border
            self.kill()

    def kill(self):
        self.alive = False
        if self in self.snakes_alive:
            self.snakes_alive.remove(self)
        # self.unbind_events()

    # def unbind_events(self):
    #     for bind_id in self.bind_ids:
    #         self.game.map.canvas.winfo_toplevel().unbind("", bind_id)

    def is_there_barrier(self):
        bbox = self.game.map.canvas.bbox(self.head)
        if bbox:  # FIXME: this is a temporary patch
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

    def overlappers(self):
        # TODO: refactor, cause this method is similat to is_there_barrier
        bbox = self.game.map.canvas.bbox(self.head)
        if bbox:  # FIXME: this is a temporary patch
            overlappers = self.game.map.canvas.find_overlapping(*bbox)
            return (overlapper for overlapper in overlappers if overlapper != self.head)

        return []

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
        else:
            self.draw()

    # def overlapping(self):
    #     bbox = self.game.map.bbox(self.head)
    #     overlappers = self.game.map.find_overlapping(*bbox)
    #     return [x for x in overlappers if x!=self.head]

from random import randrange, choice

from PIL import Image
from PIL.ImageTk import PhotoImage

from logic.services import rgb2hex
from program_config import main_game_frame
from snake import Snake


class ReverseMixin:
    def action(self, snake, **kwargs):
        # TODO: resolve this jumbo
        temp = snake.eatable_timing_table.get(self.__class__.__name__.lower(), None)
        if not temp:
            redo_kwargs = self.effect(snake, **kwargs)
            temp = [self.time, lambda: self.reverse_effect(snake, **redo_kwargs)]
        else:
            temp[0] = self.time
        snake.eatable_timing_table[self.__class__.__name__.lower()] = temp

    @staticmethod
    def effect(snake, **kwargs):
        return {}

    @staticmethod
    def reverse_effect(snake, **kwargs):
        pass


class Eatable:
    r = 14
    planted = 0
    on_map = dict()

    score = 200

    possible_mods = ["all", "own", "others"]
    mod_colors = {
        "all": rgb2hex(117, 170, 255),
        "own": rgb2hex(245, 86, 104),
        "others": rgb2hex(233, 250, 85)
    }

    photo = None
    image_path = ""

    time = 200

    def __init__(self, map_):
        self.map = map_
        self.mod = choice(self.possible_mods)
        # fixme: check if there is a barrier or it is unreachable

        while True:
            self.x = randrange(main_game_frame.MAP_BORDER + self.r,
                               main_game_frame.MAP_SIZE.x - main_game_frame.MAP_BORDER - self.r)

            self.y = randrange(main_game_frame.MAP_BORDER + self.r,
                               main_game_frame.MAP_SIZE.y - main_game_frame.MAP_BORDER - self.r)
            if not self.map.canvas.find_overlapping(*self.bbox):
                break

        self.im_id, self.circ_id = None, None
        self.plot()

        self.on_map[self.circ_id] = self

    @property
    def bbox(self):
        # FIXME: rename func because this is overloaded
        return self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r

    def plot(self):
        canvas = self.map.canvas
        self.circ_id = canvas.create_oval(*self.bbox, fill=self.mod_colors[self.mod], outline="")

        if not self.photo:
            image = Image.open(self.image_path).resize((2 * self.r, 2 * self.r), Image.ANTIALIAS)
            self.photo = PhotoImage(image)
        self.im_id = canvas.create_image(self.x, self.y, image=self.photo)

    def unplot(self):
        self.map.canvas.delete(self.im_id)
        self.map.canvas.delete(self.circ_id)
        self.on_map.pop(self.circ_id)

    @classmethod
    def unplot_all(cls):
        for instance in cls.on_map.values():
            instance.map.canvas.delete(instance.im_id)
            instance.map.canvas.delete(instance.circ_id)
        cls.on_map = dict()

    def eat(self, snake, **kwargs):
        self.unplot()
        snake.score += self.score
        self.action(snake, **kwargs)

    def action(self, snake, **kwargs):
        temp = snake.eatable_timing_table.get(self.__class__.__name__.lower(), None)
        if not temp:
            self.effect(snake, **kwargs)
            temp = [self.time, lambda: self.effect(snake, **kwargs)]
        else:
            temp[0] = self.time
        snake.eatable_timing_table[self.__class__.__name__.lower()] = temp

    @staticmethod
    def effect(snake, **kwargs):
        pass


class Switch(Eatable):
    photo = None
    image_path = "res/png/eatables/switch.png"

    possible_mods = ["others"]

    @staticmethod
    def effect(snake, **kwargs):
        for snaki in kwargs["snakes"]:
            if snaki != snake:
                snaki.move_bind_table["left"], snaki.move_bind_table["right"] = \
                    snaki.move_bind_table["right"], snaki.move_bind_table["left"]


class Wallwalker(ReverseMixin, Eatable):
    photo = None
    image_path = "res/png/eatables/wallwalker.png"
    possible_mods = ["own"]

    @staticmethod
    def reverse_effect(snake, **kwargs):
        snake.wallwalker = False
        snake.safety = False

    @staticmethod
    def effect(snake, **kwargs):
        # FIXME: two wallwalkers consecutively picked up
        snake.wallwalker = True
        snake.safety = True
        return {}


class Clean(Eatable):
    photo = None
    image_path = "res/png/eatables/clean.png"

    possible_mods = ["all"]

    def action(self, snake, **kwargs):
        snakes = kwargs['snakes']
        for snake in snakes:
            snake.erase_shape()


class SlowDown(ReverseMixin, Eatable):
    photo = None
    image_path = "res/png/eatables/slow_down.png"

    possible_mods = ["own"]

    @staticmethod
    def reverse_effect(snake, **kwargs):
        if kwargs["do"]:
            snake.slowing = False

    def effect(self, snake, **kwargs):
        # temp = snake.eatable_timing_table.get(self.__class__.__name__.lower(), None)
        # if temp:
        #     temp[1]()
        #     snake.eatable_timing_table.pop(self.__class__.__name__.lower())
        #     return {"do": False}
        # else:
        snake.slowing = True
        return {"do": True}


class SpeedUp(ReverseMixin, Eatable):
    # TODO: If two speedup was picked up
    photo = None
    image_path = "res/png/eatables/speed_up.png"

    possible_mods = ["others"]

    @staticmethod
    def reverse_effect(snake, **kwargs):
        snakis = kwargs["snakis"]
        snakes_speeding = kwargs["snakes_speeding"]
        try:
            for snake in snakis:
                snakes_speeding.remove(snake)
        except ValueError:
            pass

    def effect(self, snake, **kwargs):
        snakes_speeding = kwargs["snakes_speeding"]
        snakes = kwargs["snakes"]
        snakis = (snaki for snaki in snakes if snaki != snake)
        snakes_speeding.update(snakis)
        return {"snakis": snakis, "snakes_speeding": snakes_speeding}


eatable_classes = [Switch, Wallwalker, Clean, SpeedUp, SlowDown]

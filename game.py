import gconsts as consts
from map import Map
from snake import Snake
from eatable import Eatable


class Game:

    def __init__(self, root, map_canvas):
        self.root = root
        self.map = Map()
        self.snakes = []
        self.ingame = False
        self.counter = 0
        self.delay = consts.START_LOOP_DELAY

        map_canvas.load_map(self.map)
        # self.start()
        
    def start(self):
        for snake in self.snakes:
                snake.delete()

        self.ingame=True
        self.counter = 0

        blue_move_bind_table  = {
                'up' : '<Up>',
                'down' : '<Down>',
                'left' : '<Left>',
                'right' : '<Right>'
            }

        self.snakes = {
            Snake(self,(242, 23, 7)),
            Snake(self, (5, 5, 232), blue_move_bind_table),
        }

        Eatable(self.map, ).plot()

        self.root.after(consts.START_DELAY, self.loop)

    def loop(self):
        if Snake.snakes_alive:
            for snake in Snake.snakes_alive:
                snake.move()

            self.counter += 1
            if not self.counter%consts.LOOP_DELAY_DECREASE_TIME:
                if self.delay > consts.MIN_LOOP_DELAY:
                    self.delay -= 1
            self.root.after(self.delay, self.loop)
        else:
            self.ingame = False
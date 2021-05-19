from random import choice

import program_config as consts
from logic.map import Map
from snake import Snake
import eatables


class Game:

    def __init__(self, root, map_canvas, score_table, starting_handle):
        self.root = root
        self.map = Map()
        self.snakes = []
        self.in_game = False
        self.paused = False
        self.counter = 0
        self.delay = consts.START_LOOP_DELAY
        self.max_eatable = 0
        self.snakes_speeding = []

        self.starting_handle = starting_handle

        map_canvas.load_map(self.map)
        self.map_canvas = map_canvas
        self.score_table = score_table
        # self.start()

    def start(self):
        if len(self.starting_handle.snakes) > 1:
            for snake in self.snakes:
                snake.delete()
            self.snakes = []
            self.in_game = True
            self.counter = 0
            self.delay = consts.START_LOOP_DELAY
            self.paused = False

            eatables.Eatable.unplot_all()
            self.snakes_speeding = set()
            self.snakes = [Snake(self, snake_model) for snake_model in self.starting_handle.snakes]
            self.max_eatable = 2*len(self.snakes)

            # Switch(self.map, )
            # Wallwalker(self.map, )
            # Clean(self.map, )
            # SpeedUp(self.map, )



            self.root.winfo_toplevel().bind("<KeyPress>", self.move_snakes)
            self.root.after(consts.START_DELAY, self.loop)

            self.map_canvas.winfo_toplevel().event_generate("<<GameStarted>>")
            return True
        else:
            self.map_canvas.message("Add more players!")
            return False

    def move_snakes(self, event):
        for snake in Snake.snakes_alive:
            snake.check_event(event.keysym)

    def check_eatables(self):
        for snake in Snake.snakes_alive:
            overlappers = snake.overlappers()
            for overlapper in overlappers:
                if eatabl := eatables.Eatable.on_map.get(overlapper, None):
                    eatabl.eat(snake, snakes=self.snakes, snakes_speeding=self.snakes_speeding)
                    break

    def speeding(self):
        if self.snakes_speeding:
            for snake in self.snakes_speeding:
                if snake.alive:
                    snake.move()
            self.check_eatables()  # TODO: if this gets longer, refactor it out of loop

    def pause(self):
        self.root.winfo_toplevel().unbind("<KeyPress>")

    def unpause(self):
        self.root.winfo_toplevel().bind("<KeyPress>", self.move_snakes)

    def loop(self):
        if not self.paused:
            if self.in_game and Snake.snakes_alive:
                for snake in Snake.snakes_alive:
                    if (not snake.slowing) or (not self.counter % 2):
                        snake.move()
                    snake.eatable_timing()
                    if not self.counter % 3:
                        snake.score += 1
                self.check_eatables()
                self.counter += 1
                if (not self.counter % consts.LOOP_DELAY_DECREASE_TIME) and self.delay > consts.MIN_LOOP_DELAY:
                    # TODO: what if overflow counter? Game cant be that long or counter needs reseting
                    self.delay -= 1

                if (not self.counter % 30) and (len(eatables.Eatable.on_map) < self.max_eatable):
                    eatable_class_to_plot = choice(eatables.eatable_classes)
                    eatable_class_to_plot(self.map)
                self.root.after(self.delay, self.loop)
                self.root.after(self.delay, self.speeding)

                if len(Snake.snakes_alive) == 1:
                    self.in_game = False
                    self.map_canvas.message(f"Game Ended!\nWinner: {self.winner()}")
                    self.map_canvas.winfo_toplevel().event_generate("<<GameEnded>>")
            else:
                self.in_game = False
                if not self.map_canvas.contains_message:
                    self.map_canvas.message(f"Game Ended!")
                self.map_canvas.winfo_toplevel().event_generate("<<GameEnded>>")

            self.score_table.update_scores()
        else:
            self.pause()

    def winner(self):
        if Snake.snakes_alive:
            winner = Snake.snakes_alive[0]
        else:
            winner = max(self.snakes, key=lambda snake: snake.score)
        return winner.name

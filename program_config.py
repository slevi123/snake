from logic.services import rgb2hex
from logic.structs import Coord, Margin, AttributeDict

# APP_HEIGHT = 1080
# APP_WIDTH = 1600

SNAKE_HANDLERS_WIDTH = 200
SNAKELISTERS_HEIGHT = 450

LISTITEM_HEIGHT = 70


# START_MARGIN = Margin(50, 50)

MAX_SNAKE_SIZE = 30

BASE_SPEED = 20  # TODO: move here snake size instead of speed

START_DELAY = 1000  # 600
START_LOOP_DELAY = 60
MIN_LOOP_DELAY = 8
LOOP_DELAY_DECREASE_TIME = 200


class NotConfiguredYet:
    pass


window = AttributeDict({
    "APP_WIDTH": NotConfiguredYet,
    "APP_HEIGHT": NotConfiguredYet
})

logo_frame = AttributeDict({
    "logo_size": Coord(50, 50)
})

control_frame = AttributeDict({
    # app
    "Y_MARGIN": Margin(5, 8),
    "X_MARGIN":  5,
    "BUTTON_SIZE":  Coord(25, 25)
})

control_frame.total_size = Coord(
            control_frame.X_MARGIN + control_frame.BUTTON_SIZE.x + control_frame.X_MARGIN,
            control_frame.Y_MARGIN.first + control_frame.BUTTON_SIZE.y + control_frame.Y_MARGIN.last
        )


main_game_frame = AttributeDict({
    "SIZE": NotConfiguredYet,  # Coord
    "SCOREBOARD_SIZE": Coord(NotConfiguredYet, 40),
    "MAP_SIZE": NotConfiguredYet,  # Coord
    "MAP_COLOR": rgb2hex(117, 245, 66),
    "MAP_BORDER": 8,
    "SNAKE_HANDLERS_WIDTH": 200,
    # "SNAKE_HANDLERS_MARGIN": 2,
    "GM_CONTROL_BSIZE": Coord(50, 50),
    "MAP_BLOCKEDSIZE": NotConfiguredYet  # Coord
})

snake = AttributeDict({
    "START_GEN_MARGIN_BLOCKS": Coord(5, 3),
})


def gridify(dim):
    return dim // BASE_SPEED


def configure(root):
    window.APP_WIDTH, window.APP_HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()  # 1200,800  #

    main_game_frame.SIZE = Coord(
            window.APP_WIDTH,
            window.APP_HEIGHT - max(logo_frame.logo_size.y, control_frame.total_size.y)
        )

    main_game_frame.SCOREBOARD_SIZE.x = window.APP_WIDTH

    main_game_frame.MAP_BLOCKEDSIZE = Coord(
        gridify(main_game_frame.SIZE.x - main_game_frame.SNAKE_HANDLERS_WIDTH - 40),
        gridify(main_game_frame.SIZE.y - max(main_game_frame.SCOREBOARD_SIZE.y, main_game_frame.GM_CONTROL_BSIZE.y)-45)
    )

    main_game_frame.MAP_SIZE = Coord(
        main_game_frame.MAP_BLOCKEDSIZE.x * BASE_SPEED + 2*main_game_frame.MAP_BORDER,
        main_game_frame.MAP_BLOCKEDSIZE.y * BASE_SPEED + 2 * main_game_frame.MAP_BORDER,
    )

    main_game_frame.SCOREBOARD_SIZE.x = main_game_frame.MAP_SIZE.x - SNAKE_HANDLERS_WIDTH

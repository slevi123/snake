from random import seed

# from memory_profiler import profile
from PIL import Image, ImageTk

from visual.app_control_frame import AppControlFrame
import tkinter as tk

from visual.logo_frame import LogoFrame
from visual.main_game_frame import MainGameFrame
import program_config as pc


# @profile
def main():
    seed()
    root = tk.Tk()
    root.title('Snake')

    ico = Image.open('res/png/snicon.png')
    photo = ImageTk.PhotoImage(ico)

    # root.wm_iconbitmap(photo)
    root.iconphoto(True, photo)  # FIXME

    # root.overrideredirect(True)
    # root.geometry(f"{consts.APP_WIDTH}x{consts.APP_HEIGHT}")
    root.attributes("-fullscreen", True)
    root.update_idletasks()
    # Snake.head_icon = PhotoImage(Snake.head_icon_image)

    pc.configure(root)

    LogoFrame(root).grid(column=0, row=0, sticky="w")
    AppControlFrame(root).grid(column=1, row=0, sticky="e", pady=pc.control_frame.Y_MARGIN.tuple)
    MainGameFrame(root).grid(row=1, columnspan=2)

    root.grid_columnconfigure(0, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()


# TODO: help/ about menu, maybe github link
# TODO: barriers, boosters
# TODO: scoreboard
# TODO: fontstyling
# TODO: seems, there are still bugs when snakes speed up cause of multiple after calls
# TODO: snakes need to grow?
# TODO: easter-eggs
# TODO: multi-snake mode
# TODO: learning-mode

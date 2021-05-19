from pathlib import Path
from tkinter import Frame, Label, Toplevel, Button
from tkinter.simpledialog import Dialog, askfloat

from PIL import Image
from PIL.ImageTk import PhotoImage

from logic.services import add_image2tk_widget


def ph_image(path):
    image = Image.open(path)
    return PhotoImage(image)


class InfoDialog(Dialog):

    def __init__(self, parent):
        self.images = [
            ph_image(image) for image in Path("res/png/how_to_play").iterdir() if image.is_file()
        ]

        self.current_step = 0

        self.label = None

        super().__init__(parent, "How To play?")

        # self.resizable(False, False)
        # self.wm_geometry("1000x1000+0+0")

    def body(self, master):
        self.label = Label(master, text="TUTORIAL PICTUREs label\n if u see this, the game is broken",
                           image=self.images[0])
        self.label.pack()

    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="Previous", command=self.previous)
        add_image2tk_widget(w, "res/png/how_to_play/navig_arrows/back.png", resize=(170, 40))
        w.pack(side="left", padx=5, pady=5)
        w = Button(box, text="Next", command=self.next, default="active")
        add_image2tk_widget(w, "res/png/how_to_play/navig_arrows/next.png", resize=(170, 40))
        w.pack(side="left", padx=5, pady=5, fill="both", expand=True)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)
        self.bind("<Left>", self.previous)
        self.bind("<Right>", self.next)

        box.pack()

    def update_image(self):
        self.label.config(image=self.images[self.current_step])

    def next(self, event=None):
        if self.current_step < len(self.images)-1:
            self.current_step += 1
            self.update_image()
        else:
            self.ok()

    def previous(self, event=None):
        if self.current_step:
            self.current_step -= 1
            self.update_image()


class InfoFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        how_to = Label(self, text="how-to-play", cursor="hand2", compound="right", padx=0)
        about = Label(self, text="about-program", cursor="hand2")
        add_image2tk_widget(how_to, "res/png/how_to_play.png", resize=(40, 40))
        # add_image2tk_widget(about, "res/png/about.png", resize=(40, 40))
        how_to.bind("<Button-1>", self.how_to_play_window)
        # about.bind("<Button-1>", self.how_to_play_window)
        how_to.pack(side="right")
        # about.pack(side="right")

    def how_to_play_window(self, event=None):
        # window = askfloat("gg", "ww")
        InfoDialog(self.winfo_toplevel())

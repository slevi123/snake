from pathlib import Path
from random import randrange

from PIL import Image
from PIL.ImageTk import PhotoImage


def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c


def complementary_color(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))


def rgb2hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

# def recolor_head_icon(self, color=None):
    # recolor_pic()

    #     #get the color
    #     complementary = complementary_color(*self.color)

    #     #recolor the pic
    #     image = self.head_icon_image.copy()
    #     pixels = image.load()
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             pixels[i, j] = (*complementary, pixels[i, j][3])
    #     return PhotoImage(image)


def random_color():
    r, g, b = randrange(256), randrange(256), randrange(256)
    return rgb2hex(r, g, b)


def add_image2tk_widget(widget, image, resize=None):
    if isinstance(image, (str, Path)):
        image = Image.open(image)
    if resize:
        image = image.resize(resize, Image.ANTIALIAS)
    photo = PhotoImage(image)
    widget.kep = photo
    widget.config(image=photo)

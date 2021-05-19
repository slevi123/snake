from tkinter import Label, Frame

from logic.services import add_image2tk_widget
from program_config import logo_frame


class LogoFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent,)
        slogo = Label(self, compound="center")
        add_image2tk_widget(slogo, "res/png/snicon.png", resize=logo_frame.logo_size.tuple)
        slogo.pack(side="left", pady=0)
        Label(self, text="Snake: Torpedo", font=("Arial Rounded MT Bold", 19)).pack(side="left")
        Label(self, text="(by Leswell)", font=("sans-sheriff", 8), fg='grey').pack(side="left", padx=8)

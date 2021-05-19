from tkinter import Frame, Button

from logic.services import add_image2tk_widget
import program_config as pc


class AppControlFrame(Frame):
    def __init__(self, root):
        super().__init__(root)

        self.iconify_but = Button(self, text="Iconify Game", command=root.iconify, relief="ridge")
        self.close_but = Button(self, text="Close Game", command=root.destroy, relief="ridge")
        self.pack_buttons()

    def pack_buttons(self):
        add_image2tk_widget(self.close_but, "res/png/x.png", resize=pc.control_frame.BUTTON_SIZE.tuple)
        add_image2tk_widget(self.iconify_but, "res/png/-.png", resize=pc.control_frame.BUTTON_SIZE.tuple)
        self.iconify_but.pack(side='left', padx=pc.control_frame.X_MARGIN)
        self.close_but.pack(side='left', padx=pc.control_frame.X_MARGIN)

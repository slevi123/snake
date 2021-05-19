from tkinter.ttk import LabelFrame, Label, Entry, Frame
from tkinter import Button
from tkinter import Label as OLabel, messagebox
# from ttkwidgets.color import ColorPicker, ColorSquare, askcolor
from tkinter.colorchooser import askcolor
# from ttkwidgets.color import askcolor

import program_config as consts
from logic.services import add_image2tk_widget, rgb2hex, random_color
from logic.snake import SnakeModel
from snake import Snake

font_type = "sans-sheriff"


class ColorDisplayBox(OLabel):
    def __init__(self, parent, color):
        super().__init__(parent, bg=color, relief="groove", text='        ')
        self._color = color
        self.enable()

    def enable(self):
        self.bind("<Button-1>", self.color_choosing)

    def disable(self):
        self.unbind("<Button-1>")

    def color_choosing(self, event=None):
        if t := askcolor()[1]:
            self.config(bg=t)
            self._color = t

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self.config(bg=value)
        self._color = value


class SnakeCreate(LabelFrame):
    def __init__(self, parent, start_handler):
        super().__init__(parent, text="Add a snake", width=consts.SNAKE_HANDLERS_WIDTH)
        self.color_picker = ColorDisplayBox(self, 'red')
        self.color_picker.grid(padx=(8, 3))
        self.name_entry = Entry(self)
        self.name_entry.grid(column=1, row=0, padx=(1, 8))
        Button(self, text='Add Snake', command=self.add_snake, font=(font_type, "12"),
               relief='groove', bg="#94bfff").grid(row=2, columnspan=2)
        self.start_handler = start_handler

        self.selected_selector = None

        self.dir_but_container = Frame(self)
        self.key_r_selector = OLabel(self.dir_but_container, text="", borderwidth=2, relief="groove",
                                     border=2, compound="center")
        self.key_l_selector = OLabel(self.dir_but_container, text="", borderwidth=2, relief="groove",
                                     border=2, compound="center")

        self.selectors = [self.key_r_selector, self.key_l_selector]

        self.key_r_selector.grid(sticky='e', padx=5, pady=3)
        self.key_l_selector.grid(column=1, row=0, sticky='w', padx=5, pady=3)
        self.dir_but_container.grid(row=1, columnspan=2)

        add_image2tk_widget(self.key_r_selector, "res/png/left_arrow.png", resize=(40, 40))
        add_image2tk_widget(self.key_l_selector, "res/png/right_arrow.png", resize=(40, 40))

        self.bind("<Button-1>", lambda e: self.focus_set())

        self.bind_events()
        self.clear()
        self.enable()

    def clear(self):
        self.name_entry.delete(0, 'end')
        self.name_entry.insert(0, 'AnonymousSnake')
        self.name_entry.selection_range(0, "end")

        self.color_picker.color = random_color()

        for selector in self.selectors:
            selector.config(text="")

    def bind_events(self):
        self.winfo_toplevel().bind("<<GameStarted>>", self.disable, add=True)  # TODO: solve unbinding if needed
        self.winfo_toplevel().bind("<<GameEnded>>", self.enable, add=True)  # TODO: solve unbinding if needed

    def change_selector(self, char):
        self.focus_set()
        for selector in self.selectors:
            selector.config(borderwidth=2)
        if char == "r":
            self.selected_selector = self.key_r_selector
            self.selected_selector.config(borderwidth=4)
        else:
            self.selected_selector = self.key_l_selector
            self.selected_selector.config(borderwidth=4)

    def button_input(self, event):
        no_select = True
        if self.selected_selector:
            self.selected_selector.config(text=event.keysym)
            for selector in self.selectors:
                if not selector.cget("text"):
                    self.selected_selector = selector
                    self.selected_selector.config(borderwidth=4)
                    no_select = False
                else:
                    selector.config(borderwidth=2)

        if no_select:
            self.selected_selector = None
        # print(event.keysym)
        # print((event.char ==""), (event.keysym ==""))

    def disable(self, event=None):  # FIXME: labels and the color picker disabling
        self.winfo_toplevel().unbind("<Return>")
        for child in self.winfo_children():
            if child == self.dir_but_container:
                for but in child.winfo_children():
                    but.config(borderwidth=2)  # , bg=rgb2hex(219, 219, 219))
                    but.unbind("<Button-1>")
                    but.configure(state='disable')
            elif isinstance(child, ColorDisplayBox):
                child.disable()
            elif isinstance(child, (Button, Entry)):
                child.configure(state='disable')

    def enable(self, event=None):
        self.key_r_selector.bind("<Button-1>", lambda e: self.change_selector('r'))
        self.key_l_selector.bind("<Button-1>", lambda e: self.change_selector('l'))
        self.winfo_toplevel().bind("<Return>", self.add_snake)
        # self.clear()
        for child in self.winfo_children():
            if child == self.dir_but_container:
                for but in child.winfo_children():
                    but.configure(state='normal')
            elif isinstance(child, ColorDisplayBox):
                child.enable()
            elif isinstance(child, (Button, Entry)):
                child.configure(state='normal')
        self.winfo_toplevel().bind("<KeyPress>", self.button_input)

    def add_snake(self, event=None):
        l = self.key_l_selector.cget("text")
        r = self.key_r_selector.cget("text")
        if len(self.start_handler.snakes) >=20:
            messagebox.showinfo(title="Adding new snake", message="Can not add snake, you have too many!\n"
                                                                  "Maximum number of snakes(20) is reached.")
        elif l and r:
            self.start_handler.snakes.append(SnakeModel(
                self.color_picker.color,
                move_bind_table={
                    "left": r,
                    "right": l,
                },
                name=self.name_entry.get()
            ))
            self.clear()
            self.winfo_toplevel().event_generate("<<SnakeModelsChanged>>")
        else:
            messagebox.showinfo(title="Adding new snake", message="You need to select control buttons first!")

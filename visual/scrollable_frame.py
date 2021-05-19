import tkinter as tk
from tkinter import ttk

from ttkwidgets import AutoHideScrollbar


class ScrollableFrame(ttk.Frame):
    """
    """
    def __init__(self, container, height=None, width=None, **kwargs):
        super().__init__(container, **kwargs)
        self.canvas = tk.Canvas(self, height=height, width=width, )
        scrollbar = AutoHideScrollbar(self, orient="vertical", command=self.canvas.yview)
        self.interior = ttk.Frame(self.canvas)

        self.interior.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind('<Enter>', self._bind_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbind_from_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")  # TODO: fix scorlling on linux

    def _bind_to_mousewheel(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # FIXME: scrolls on everymouse scroll

    def _unbind_from_mousewheel(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")

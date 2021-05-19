from tkinter import Canvas

from program_config import main_game_frame
import program_config as consts
from snake import Snake


class MapCanvas(Canvas):
    def __init__(self, root, **kw):
        super().__init__(root, bd=main_game_frame.MAP_BORDER, relief='sunken', bg=main_game_frame.MAP_COLOR, **kw)

        self.map = None
        self.message_ids = []
        self.contains_message = False
        self.message("Welcome")

    def load_map(self, map_):
        self.map = map_
        map_.canvas = self
        self.map.init_map()

    def message(self, text="Under developing", bg="white"):
        self.delete_message()
        textid = self.create_text(self.winfo_reqwidth() // 2, self.winfo_reqheight() // 2, text=text,
                                  font=("sans-sheriff", "24"))
        horizontal_offset, vertical_offset = 40, 40
        bbox = self.bbox(textid)
        new_bbox = (bbox[0] - horizontal_offset // 2, bbox[1] - vertical_offset // 2,
                    bbox[2] + horizontal_offset // 2, bbox[3] + vertical_offset // 2)

        rect_id = self.create_rectangle(*new_bbox, fill="white", width=4, outline="black")
        self.tag_raise(textid)

        self.message_ids = (rect_id, textid)
        self.contains_message = True

    def delete_message(self):
        for azonosito in self.message_ids:
            self.delete(azonosito)

        self.contains_message = False

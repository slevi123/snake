from dataclasses import dataclass


@dataclass
class SnakeModel:
    color: str
    move_bind_table: dict = {},
    name: str = "PlayerAnonymous"

    @property
    def button_string(self):
        return "   ".join((self.move_bind_table.get("left"),
                           self.move_bind_table.get("right"),
                           ))

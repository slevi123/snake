from dataclasses import dataclass


@dataclass
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return self.x, self.y

    def __getitem__(self, item):
        if item:
            return self.x
        else:
            return self.y

@dataclass
class Margin:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def tuple(self):
        return self.first, self.last

    def __getitem__(self, item):
        if item:
            return self.last
        else:
            return self.first


class AttributeDict(dict):
    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

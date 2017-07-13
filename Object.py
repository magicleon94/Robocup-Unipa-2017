import numpy as np


class Object(object):
    def __init__(self, name):
        self.type = None
        self.name = name
        if name == "green":
            self.min_color = [34, 50, 50]
            self.max_color = [80, 220, 200]
            self.frameColor = (0, 255, 0)

        elif name == "blue":
            self.min_color = [101, 165, 31]
            self.max_color = [233, 255, 123]
            self.frameColor = (255, 0, 0)

        elif name == "red":
            self.min_color = [0, 0, 0]
            self.max_color = [120, 22, 50]
            self.frameColor = (0, 0, 255)

        elif name == "yellow":
            self.min_color = [0, 116, 88]
            self.max_color = [36, 227, 208]
            self.frameColor = (0, 255, 255)

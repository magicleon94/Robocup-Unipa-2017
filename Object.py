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
            self.otherObjectColor = "yellow"

        elif name == "red":
            self.min_color = [0, 161, 36]
            self.max_color = [14, 255, 201]
            self.frameColor = (0, 0, 255)
            self.otherObjectColor = "blue"

        elif name == "yellow":
            self.min_color = [0, 230, 127]
            self.max_color = [95, 255, 214]
            self.frameColor = (0, 255, 255)
            self.otherObjectColor = "blue"

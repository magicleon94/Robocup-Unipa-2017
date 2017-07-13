import numpy as np


class Object(object):
    def __init__(self, name):
        self.type = None
        self.name = name
        if name == "green":
            self.min_bgr = [34, 50, 50]
            self.max_bgr = 80, 220, 200]
            self.frameColor= (0, 255, 0)

        elif name == "blue":
            self.min_bgr= [9, 0, 0]
            self.max_bgr= [245, 99, 68]
            self.frameColor= (255, 0, 0)

        elif name == "red":
            self.min_bgr= [0, 0, 0]
            self.max_bgr= [120, 22, 50]
            self.frameColor= (0, 0, 255)

        elif name == "yellow":
            self.min_bgr= [0, 116, 88]
            self.max_bgr= [36, 227, 208]
            self.frameColor= (0, 255, 255)

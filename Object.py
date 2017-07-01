import numpy as np

class Object(object):
    def __init__(self, name):
        self.type = None
        self.name = name
        if name == "green":
            self.min_hsv = np.array([34, 50, 50])
            self.max_hsv = np.array([80, 220, 200])
            self.frameColor = (0, 255, 0)
        elif name == "blue":
            self.min_hsv = np.array([92, 0, 0])
            self.max_hsv = np.array([124, 256, 256])
            self.frameColor = (255, 0, 0)
        elif name == "red":
            #self.min_hsv = np.array([0, 200, 0])
            #self.max_hsv = np.array([19, 255, 255])
            self.min_hsv = np.array([0, 159, 26])
            self.max_hsv = np.array([2, 255, 255])
            self.frameColor = (0, 0, 255)

        elif name == "yellow":
            self.min_hsv = np.array([20, 124, 123])
            self.max_hsv = np.array([30, 256, 256])
            self.frameColor = (0, 255, 255)
        elif name == "orange":
            self.min_hsv = np.array([1, 242, 55])
            self.max_hsv = np.array([24, 255, 204])
            self.frameColor = (0, 255, 255)
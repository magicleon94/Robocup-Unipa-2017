import cv2
import numpy as np
from Object import Object
import Thresholder


class Detector(object):
    def __init__(self, obj):
        self.obj = obj
        self.distance = None
        self.bounding_box = None

    def refresh(self):
        self.distance = None
        self.bounding_box = None

    def find_obj(self, frame):
        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = Thresholder.threshold(
            frame, self.obj.min_color, self.obj.max_color)
        cv2.imshow('mask', mask)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(cnts) > 0:
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0:2]
            # print "Bigger contours: ", len(cnts)
            for c in cnts:
                rect = cv2.minAreaRect(c)

                # se l'oggetto e' sufficientemente grande lo detecto (per evitare falsi positivi)
                larghezza = rect[1][0]
                altezza = rect[1][1]

                if altezza > 30:
                    #self.bounding_box = rect
                    #box = np.int0(cv2.boxPoints(rect))
                    self.bounding_box = rect
                    return rect
                    # cv2.drawContours(
                    #     frame, [box], -1, self.obj.frameColor, 8)
                    #text = self.obj.name + " " + self.obj.type
                    # print text
            return None

    def find_type(self, frame):
        other_color_detector = Detector(Object(self.obj.otherObjectColor))
        rect_other_color = other_color_detector.find_obj(frame)
        if rect_other_color is not None:  # se ha trovato l'altro colore allora e' un oggetto
            self.obj.type = "object"
        else:
            self.obj.type = "area"

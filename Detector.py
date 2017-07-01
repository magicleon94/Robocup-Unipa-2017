import cv2
import numpy as np
import Object

class Detector(object):
    def __init__(self, obj):
        self.obj = obj
        self.distance = None
        self.bounding_box = None

    #def calculate_distance(self): #TODO

    def refresh(self):
        self.distance = None
        self.bounding_box = None

    def find_obj(self, frame, type_obj="object"):
        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame, self.obj.min_hsv, self.obj.max_hsv)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow('mask', mask)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        while len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            cnts.remove(max(cnts)) # faccio il pop dell'elemento piu' grande
            rect = cv2.minAreaRect(c)

            if rect[1][0] > 10:  # se l'oggetto e' sufficientemente grande lo detecto (per evitare falsi positivi)
                #self.bounding_box = rect
                box = np.int0(cv2.boxPoints(rect))

                if rect[1][0] > 2 * rect[1][1]:
                    my_type = "area"
                else:
                    my_type = "object"
                if my_type == type_obj: # se ho trovato l'oggetto che stavo cercando salvo i valori
                    self.bounding_box = rect
                    self.obj.type = my_type
                    cv2.drawContours(frame, [box], -1, self.obj.frameColor, 8)
                    text = self.obj.name + " " + self.obj.type
                    print text
                    break
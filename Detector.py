import cv2
import numpy as np
import Object
import Thresholder


class Detector(object):
    def __init__(self, obj):
        self.obj = obj
        self.distance = None
        self.bounding_box = None

    # def calculate_distance(self): #TODO

    def refresh(self):
        self.distance = None
        self.bounding_box = None

    def find_obj(self, frame, type_obj="object"):
        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print self.obj.min_color
        print self.obj.max_color
        mask = Thresholder.threshold(
            frame, self.obj.min_color, self.obj.max_color)
        cv2.imshow('mask', mask)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0:2]
            for c in cnts:
                rect = cv2.minAreaRect(c)

                # se l'oggetto e' sufficientemente grande lo detecto (per evitare falsi positivi)
                larghezza = rect[1][0]
                altezza = rect[1][1]
                print "Larghezza: ", larghezza
                print "Altezza: ", altezza
                print "Rect: ", rect
                print "\n"*2

                if larghezza > 10:
                    #self.bounding_box = rect
                    box = np.int0(cv2.boxPoints(rect))
                    my_type = "object"

                    if larghezza >= 1.8 * altezza:
                        my_type = "area"

                    if my_type == type_obj:  # se ho trovato l'oggetto che stavo cercando salvo i valori
                        self.bounding_box = rect
                        self.obj.type = my_type
                        cv2.drawContours(
                            frame, [box], -1, self.obj.frameColor, 8)
                        text = self.obj.name + " " + self.obj.type
                        print text
                        break
                    else:
                        print "i don't want a ", my_type

        cv2.imshow('frame', frame)

        # while len(cnts) > 0:
        #     c = max(cnts, key=cv2.contourArea)
        # rect = cv2.minAreaRect(c)

        # # se l'oggetto e' sufficientemente grande lo detecto (per evitare falsi positivi)
        # if rect[1][0] > 10:
        #     #self.bounding_box = rect
        #     box = np.int0(cv2.boxPoints(rect))
        #     my_type = "object"

        #     if rect[1][0] > 2 * rect[1][1]:
        #         my_type = "area"

        #     if my_type == type_obj:  # se ho trovato l'oggetto che stavo cercando salvo i valori
        #         self.bounding_box = rect
        #         self.obj.type = my_type
        #         cv2.drawContours(frame, [box], -1, self.obj.frameColor, 8)
        #         text = self.obj.name + " " + self.obj.type
        #         print text
        #         break
        #     else:
        #         # faccio il pop dell'elemento piu' grande
        #         cnts.remove(max(cnts, key=cv2.contourArea))

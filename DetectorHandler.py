from Detector import Detector
from Object import Object
import constants
import cv2


class DetectorHandler(object):
    def __init__(self, detectors=None):
        if detectors is None:
            detectors = [Detector(Object("red")), Detector(Object("blue")), Detector(
                Object("yellow")), Detector(Object("green"))]
        self.detectors = detectors
        self.target = None
        self.frame = None
        # self.update()

    def find_target(self, frame, color=None, type_obj="object"):
        self.update(frame)
        if color is None:  # se non gli passo nessun colore da cercare, li cerco tutti
            for detector in self.detectors:
                rect = detector.find_obj(self.frame)
                if rect is not None:
                    detector.find_type(self.frame)
                if detector.bounding_box and detector.obj.type == type_obj:  # se ho rilevato qualcosa
                    self.target = detector
                    break
        else:  # altrimenti cerco solo quel colore
            detector = Detector(Object(color))
            rect = detector.find_obj(self.frame)
            if rect is not None:
                detector.find_type(self.frame)
            if detector.bounding_box and detector.obj.type == type_obj:  # se ho rilevato qualcosa
                self.target = detector
        if self.target:
            print "my target is " + self.target.obj.name + " " + self.target.obj.type

    def do_action(self):
        if not self.target:
            print "I need a target"
        else:
            text = "target: " + self.target.obj.name + " " + self.target.obj.type
            print text
            range_min = self.frame.shape[1] * 0.5 - self.frame.shape[1] / 4
            range_max = self.frame.shape[1] * 0.5 + self.frame.shape[1] / 4
            print self.frame.shape
            if range_min <= self.target.bounding_box[0][0] <= range_max:
                print "vai avanti"
                return constants.FORWARD
            elif self.target.bounding_box[0][0] < range_min:
                print "vai a sinistra"
                return constants.TURN_LEFT_MICRO
            else:
                print "vai a destra"
                return constants.TURN_RIGHT_MICRO

    def update(self, frame):  # aggiorna distanze e bounding box di tutti i detector
        self.target = None
        self.frame = frame
        for detector in self.detectors:
            detector.refresh()
        #    detector.find_obj(self.frame)

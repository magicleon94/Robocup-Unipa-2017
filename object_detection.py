import cv2
import numpy as np
import imutils

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
            self.min_hsv = np.array([146, 47, 0])
            self.max_hsv = np.array([194, 218, 255])
            self.frameColor = (0, 0, 255)

        elif name == "yellow":
            self.min_hsv = np.array([20, 124, 123])
            self.max_hsv = np.array([30, 256, 256])
            self.frameColor = (0, 255, 255)



class Detector(object):
    def __init__(self, obj):
        self.obj = obj
        self.distance = None
        self.bounding_box = None

    #def calculate_distance(self): #TODO

    def refresh(self):
        self.distance = None
        self.bounding_box = None

    def find_obj(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.obj.min_hsv, self.obj.max_hsv)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            rect = cv2.minAreaRect(c)

            if rect[1][0] > 130:  # se l'oggetto e' sufficientemente grande lo detecto (per evitare falsi positivi)
                self.bounding_box = rect
                box = np.int0(cv2.boxPoints(self.bounding_box))
                cv2.drawContours(frame, [box], -1, self.obj.frameColor, 8)
                if self.bounding_box[1][0] > 2 * self.bounding_box[1][1]:
                    self.obj.type = "area"
                else:
                    self.obj.type = "object"

                text = self.obj.name + " " + self.obj.type
                #print self.bounding_box[0][0] + 200, self.bounding_box[0][1]
                cv2.putText(frame, text,
                            (int(self.bounding_box[0][0]), int(self.bounding_box[0][1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, self.obj.frameColor, 6)


class DetectorHandler(object):
    def __init__(self, detectors):
        self.detectors = detectors
        self.target = None
        self.frame = None
        #self.update()

    def find_target(self):  #TODO
        for detector in self.detectors:
            if detector.bounding_box:
                self.target = detector
                break

    def do_action(self): #TODO
        if not self.target:
            print "I need a target"
        else:
            text = "target: " + self.target.obj.name + " " + self.target.obj.type
            cv2.putText(self.frame, text,
                        (self.frame.shape[1] - 2000, self.frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                        6.0, self.target.obj.frameColor, 6)

            range_min = self.frame.shape[1] * 0.5 - 300
            range_max = self.frame.shape[1] * 0.5 + 300

            if range_min <= self.target.bounding_box[0][0] <= range_max:
                print "vai avanti"
                return 0
            elif self.target.bounding_box[0][0] < range_min:
                print "vai a sinistra"
                return 4
            else:
                print "vai a destra"
                return 6
    def update(self, frame): #aggiorna distanze e bounding box di tutti i detector #TODO
        self.target = None
        self.frame = frame
        for detector in self.detectors:
            detector.refresh()
            detector.find_obj(frame)
            #detector.calculate_distance()






if __name__ == '__main__':
    #cap = cv2.VideoCapture('immagini/IMG_5110.MOV')
    #cap = cv2.VideoCapture('rtsp://@192.168.0.102/live/ch00_0', cv2.CAP_FFMPEG)
    cap = cv2.VideoCapture('rtsp://@192.168.1.21/live/ch00_0', cv2.CAP_FFMPEG)

    detectors = [
        Detector(Object("green")),
        Detector(Object("blue")),
        Detector(Object("red")),
        Detector(Object("yellow"))
    ]

    detector_handler = DetectorHandler(detectors)

    cv2.namedWindow('mask')
    cv2.namedWindow('img')


    while(True):
        ret, frame = cap.read()
        if not ret:
            break
        #frame = cv2.imread('immagini/all.jpg', 1)

        detector_handler.update(frame)
        detector_handler.find_target()
        if detector_handler.target:
            detector_handler.do_action()

        frame = imutils.resize(frame, width=600)
        cv2.imshow('img', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()








    # if len(cnts) > 0:
    #     # find the largest contour in the mask, then use
    #     # it to compute the minimum enclosing circle and
    #     # centroid
    #     c = max(cnts, key=cv2.contourArea)
    #     ((x, y), radius) = cv2.minEnclosingCircle(c)
    #     M = cv2.moments(c)
    #     center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    #
    #     # only proceed if the radius meets a minimum size
    #     if radius > 30:
    #         # draw the circle and centroid on the frame,
    #         # then update the list of tracked points
    #         cv2.circle(frame, (int(x), int(y)), int(radius), obj.frameColor, 2)
    #         cv2.circle(frame, center, 5, obj.frameColor, -1)
    #         return center



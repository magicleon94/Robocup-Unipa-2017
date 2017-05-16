import cv2
import numpy as np
import imutils


def find_obj(hsv, obj):
    mask = cv2.inRange(hsv, obj.min_hsv, obj.max_hsv)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 30:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), obj.frameColor, 2)
            cv2.circle(frame, center, 5, obj.frameColor, -1)

class Object(object):
    def __init__(self, name):
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

if __name__ == '__main__':
    cap = cv2.VideoCapture('immagini/IMG_5110.MOV')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    green_obj = Object("green")
    blue_obj = Object("blue")
    red_obj = Object("red")
    yellow_obj = Object("yellow")

    cv2.namedWindow('mask')
    cv2.namedWindow('img')

    first_time = True

    while(True):
        ret, frame = cap.read()
        if ret == False:
            break
        #frame = cv2.imread('immagini/all.jpg', 1)

        frame = imutils.resize(frame, width=600)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        find_obj(hsv, green_obj)
        find_obj(hsv, blue_obj)
        find_obj(hsv, red_obj)
        find_obj(hsv, yellow_obj)
        out.write(frame)
        cv2.imshow('img', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()






import threading
from DetectorHandler import DetectorHandler
import cv2
import numpy as np

running = True


def adjust_gamma(image, gamma=1.0):

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth


def update(x):
    hsv_green_lower[0] = cv2.getTrackbarPos('H_LOW', 'mask')
    hsv_green_lower[1] = cv2.getTrackbarPos('S_LOW', 'mask')
    hsv_green_lower[2] = cv2.getTrackbarPos('V_LOW', 'mask')
    hsv_green_upper[0] = cv2.getTrackbarPos('H_HIGH', 'mask')
    hsv_green_upper[1] = cv2.getTrackbarPos('S_HIGH', 'mask')
    hsv_green_upper[2] = cv2.getTrackbarPos('V_HIGH', 'mask')

    print hsv_green_lower, hsv_green_upper

    #mask = cv2.inRange(hsv, hsv_green_lower, hsv_green_upper)
    #mask = cv2.erode(mask, None, iterations=2)
    #mask = cv2.dilate(mask, None, iterations=2)

    #cv2.imshow('mask', mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


#img = adjust_gamma(img, gamma=0.6)

#cap = cv2.VideoCapture(0)


hsv_green_lower = np.array([0, 114, 34])
hsv_green_upper = np.array([17, 220, 235])


frame = None
ret = None
# hsv_green_lower = cv2.cvtColor(hsv_green_lower, cv2.COLOR_BGR2HSV)
# hsv_green_upper = cv2.cvtColor(hsv_green_upper, cv2.COLOR_BGR2HSV)
cap = cv2.VideoCapture('rtsp://@192.168.1.101/live/ch00_0', cv2.CAP_FFMPEG)
# cap = cv2.VideoCapture(0)


class AcquireFrames(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global cap
        global running
        global ret
        while running:
            ret = cap.grab()
        cap.release()


cv2.namedWindow('mask')
cv2.namedWindow('img')

cv2.createTrackbar('H_LOW', 'mask', hsv_green_lower[0], 255, update)
cv2.createTrackbar('H_HIGH', 'mask', hsv_green_upper[0], 255, update)

cv2.createTrackbar('S_LOW', 'mask', hsv_green_lower[1], 255, update)
cv2.createTrackbar('S_HIGH', 'mask', hsv_green_upper[1], 255, update)

cv2.createTrackbar('V_LOW', 'mask', hsv_green_lower[2], 255, update)
cv2.createTrackbar('V_HIGH', 'mask', hsv_green_upper[2], 255, update)

frames_grabber = AcquireFrames()
frames_grabber.start()

detector_handler = DetectorHandler()

while True:

    _, frame = cap.retrieve(ret)
    if frame is None:
        continue

    mask = cv2.inRange(frame, hsv_green_lower, hsv_green_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cv2.imshow('mask', mask)
    cv2.imshow('img', frame)

    detector_handler.find_target(frame, color="red", type_obj="object")
    print "Showing frame"
    # se trovi un target vai al target
    if detector_handler.target is not None:
        following = True
        # conn.send(str(detector_handler.do_action()))
        print "Going to object"
        continue

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
running = False
cap.release()

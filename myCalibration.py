import threading
from DetectorHandler import DetectorHandler
import cv2
import numpy as np
import Thresholder

running = True


def normalize2D(img):
    x = img - img.min()
    return 255 / x.max() * x


def normalize3D(frame):
    frame[:, :, 0] = normalize2D(frame[:, :, 0])
    frame[:, :, 1] = normalize2D(frame[:, :, 1])
    frame[:, :, 2] = normalize2D(frame[:, :, 1])
    return frame


def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth


def update(x):
    bgr_lower[0] = cv2.getTrackbarPos('B_LOW', 'mask')
    bgr_lower[1] = cv2.getTrackbarPos('G_LOW', 'mask')
    bgr_lower[2] = cv2.getTrackbarPos('R_LOW', 'mask')
    bgr_upper[0] = cv2.getTrackbarPos('B_HIGH', 'mask')
    bgr_upper[1] = cv2.getTrackbarPos('G_HIGH', 'mask')
    bgr_upper[2] = cv2.getTrackbarPos('R_HIGH', 'mask')

    #mask = cv2.inRange(hsv, hsv_green_lower, hsv_green_upper)
    #mask = cv2.erode(mask, None, iterations=2)
    #mask = cv2.dilate(mask, None, iterations=2)

    #cv2.imshow('mask', mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


#img = adjust_gamma(img, gamma=0.6)

#cap = cv2.VideoCapture(0)


bgr_lower = [3, 27, 45]
bgr_upper = [197, 255, 95]

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

cv2.createTrackbar('B_LOW', 'mask', bgr_lower[0], 255, update)
cv2.createTrackbar('B_HIGH', 'mask', bgr_upper[0], 255, update)

cv2.createTrackbar('G_LOW', 'mask', bgr_lower[1], 255, update)
cv2.createTrackbar('G_HIGH', 'mask', bgr_upper[1], 255, update)

cv2.createTrackbar('R_LOW', 'mask', bgr_lower[2], 255, update)
cv2.createTrackbar('R_HIGH', 'mask', bgr_upper[2], 255, update)

frames_grabber = AcquireFrames()
frames_grabber.start()

detector_handler = DetectorHandler()

try:
    while True:
        print bgr_lower, bgr_upper
        _, src = cap.retrieve(ret)
        if src is None:
            print "Frame is None"
            continue
        cv2.imshow('img', src)
        src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

        # src[:, :, 2] = cv2.equalizeHist(src[:, :, 2])
        mask = Thresholder.threshold(src, bgr_lower, bgr_upper)

        cv2.imshow('mask', mask)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    pass
cv2.destroyAllWindows()
running = False
frames_grabber.join()

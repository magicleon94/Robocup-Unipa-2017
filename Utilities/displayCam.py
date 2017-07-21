from __future__ import division
import cv2
import imutils
import numpy as np
import sys
sys.path.append('..')
import Thresholder


min_color = [0, 161, 36]
max_color = [14, 255, 201]

# cap = cv2.VideoCapture('rtsp://@192.168.1.1/live/ch00_0', cv2.CAP_FFMPEG)
cap = cv2.VideoCapture(0)
while True:
    #frame = cv2.imread('immagini/50cm.jpg', 1)
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame[:, :, 2] = np.where(
        (255 - frame[:, :, 2]) < 90, 255, frame[:, :, 2] + 90)
    mask = Thresholder.threshold(frame, min_color, max_color)
    ones = np.count_nonzero(mask)
    w, h = mask.shape
    total = w * h
    print "Total number of pixels: ", total
    print "White pixels: ", ones
    print "Ratio: ", (ones / total) * 100, "%"

    cv2.imshow('frame', cv2.cvtColor(frame, cv2.COLOR_HSV2BGR))
    cv2.imshow('mask', mask)
    # cv2.waitKey(0)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    # cv2.destroyAllWindows()

cap.release()
cv2.destroyAllWindows()
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))

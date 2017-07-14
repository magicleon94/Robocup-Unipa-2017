import numpy as np
import cv2


def normalize2D(img):
    x = img - img.min()
    return 255 / x.max() * x


def normalize3D(frame):
    frame[:, :, 0] = normalize2D(frame[:, :, 0])
    frame[:, :, 1] = normalize2D(frame[:, :, 1])
    frame[:, :, 2] = normalize2D(frame[:, :, 2])
    return frame


def threshold(src, lowerVals, upperVals):
    if src is None:
        print "Thresholder.threshold(), src is None!"
        return None

    frame = normalize3D(np.copy(src))
    mask = cv2.inRange(frame, np.array(lowerVals), np.array(upperVals))
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)
    return mask

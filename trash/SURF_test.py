import sys
sys.path.append("../")
import Thresholder
import cv2
import threading
import matplotlib as plt
import numpy as np

running = True
cap = cv2.VideoCapture('rtsp://@192.168.1.101/live/ch00_0', cv2.CAP_FFMPEG)

ret = None

min_color = [101, 165, 31]
max_color = [233, 255, 123]


class FramesGrabber(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global cap
        global ret
        global running
        while running:
            ret = cap.grab()


frames_grabber = FramesGrabber()

frames_grabber.start()
orb = cv2.ORB_create()
#sift = cv2.xfeatures2d.SIFT_create()
print "starting"
# while True:
#     ret, frame = cap.retrieve()
#     if frame is not None:
#         cv2.imshow('frame', frame)
#         c = cv2.waitKey(0) & 0xFF

#         if c == ord('q'):
#             break
#         elif c == ord('d'):
#             continue

#         cv2.imwrite("red_obj_test.jpg", frame)
#         break

img1 = cv2.imread("red_obj_test.jpg", 0)
kp1, des1 = orb.detectAndCompute(img1, None)
MIN_MATCH_COUNT = 10

try:
    while True:
        ret, frame = cap.retrieve()

        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            kp2, des2 = orb.detectAndCompute(frame, None)
            # FLANN_INDEX_KDTREE = 1
            # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            # search_params = dict(checks=50)
            # flann = cv2.FlannBasedMatcher(index_params, search_params)
            # matches = flann.knnMatch(des1, des2, k=2)
            # # store all the good matches as per Lowe's ratio test.
            # good = []
            # for m, n in matches:
            #     if m.distance < 0.7 * n.distance:
            #         good.append(m)
            # if len(good) > MIN_MATCH_COUNT:
            #     src_pts = np.float32(
            #         [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            #     dst_pts = np.float32(
            #         [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            #     M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            #     matchesMask = mask.ravel().tolist()
            #     print img1.shape
            #     h, w = img1.shape
            #     pts = np.float32(
            #         [[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            #     dst = cv2.perspectiveTransform(pts, M)
            #     img2 = cv2.polylines(
            #         frame, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
            # else:
            #     print(
            #         "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
            #     matchesMask = None

            # create BFMatcher object
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            # Match descriptors.
            matches = bf.match(des1, des2)

            # Sort them in the order of their distance.
            matches = sorted(matches, key=lambda x: x.distance)

            # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
            #                    singlePointColor=None,
            #                    matchesMask=matchesMask,  # draw only inliers
            #                    flags=2)
            img3 = cv2.drawMatches(img1, kp1, frame, kp2,
                                   matches[:10], flags=2, outImg=None)

            cv2.imshow('img3', img3)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            print "Frame is None"


except KeyboardInterrupt:
    print "Shutting down"

running = False
frames_grabber.join()
cap.release()
print "Capture device released"
cv2.destroyAllWindows()
print "Windows cleared"

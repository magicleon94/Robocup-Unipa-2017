import sys
sys.path.append("../")
import Thresholder
import cv2
import threading


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
counter = 0
target = "BLUE_OBJECT_IMAGE_"
folder = "BLUE_OBJECT/"
try:
    while True:
        ret, frame = cap.retrieve()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = Thresholder.threshold(
                frame, min_color, max_color)
            cv2.imshow('mask', mask)
            c = cv2.waitKey(0) & 0xFF

            if c == ord('q'):
                break
            elif c == ord('d'):
                continue

            cv2.imwrite(folder + target + str(counter) + ".jpg", mask)
            counter += 1
except KeyboardInterrupt:
    print "Shutting down"

running = False
frames_grabber.join()
cap.release()
print "Capture device released"
cv2.destroyAllWindows()
print "Windows cleared"

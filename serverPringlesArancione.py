#this script accept a JSON, as a string, and send a string that contains an integer
#that indicates the speed

import json
import socket
from object_detection import Object, Detector, DetectorHandler
import cv2
import threading
import constants
running = True


following = False
reached = False
target = "orange"







TCP_IP = "192.168.1.234"
TCP_PORT = 1931
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IP .4 & TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #this should prevent errors of "already in use"
s.bind((TCP_IP, TCP_PORT)) #bind socket

BUFFER_SIZE = 512  #  BUFFER SIZE - da controllare se aumentare o diminuire
# This function takes an int argument called backlog, which specifies the
# maximum number of  connections that are kept waiting if the application is
# already busy.
s.listen(1)
cap = cv2.VideoCapture('rtsp://@192.168.1.245/live/ch00_0', cv2.CAP_FFMPEG)
class AcquireFrames(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global cap
        global ret
        global running
        while running:
            ret = cap.grab()

frames_grabber = AcquireFrames()

frames_grabber.start()

detectors = [Detector(Object(target))]

detector_handler = DetectorHandler(detectors)

cv2.namedWindow('mask')
cv2.namedWindow('img')

print "Listening started"
try:
    while True: # wait connection
        conn, addr = s.accept() #accept connection
        #message from the client
        message = conn.recv(BUFFER_SIZE)

        print message,'\n'

        if not message:
            print "There is no message"
            break

        ret, frame = cap.retrieve(ret)


        input_dictionary = json.loads(message)

        leftObstacle = input_dictionary["leftObstacle"] == 0
        frontObstacle = input_dictionary["frontObstacle"] == 0
        rightObstacle = input_dictionary["rightObstacle"] == 0

        if frontObstacle and target == "red":
            print "Yay!"
            break

        if frame is not None:
            detector_handler.update(frame)
            detector_handler.find_target()
            if detector_handler.target:
                server_message = detector_handler.do_action()
                following = True
            else:
                if not following:
                    server_message = constants.TURN_RIGHT
                else:
                    following = False
                    target = "red"
                    server_message = constants.BACKWARD
                    detector_handler.detectors = [Detector(Object(target))]


            cv2.imshow('img', frame)

            conn.send(str(server_message))

        cv2.waitKey(1)
except KeyboardInterrupt:
    print "Shutting down"
    running = False
    s.close()
running = False
cap.release()
cv2.destroyAllWindows()

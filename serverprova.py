#this script accept a JSON, as a string, and send a string that contains an integer
#that indicates the speed

import json
import socket
from object_detection import Object, Detector, DetectorHandler
import cv2
import imutils
import threading

FORWARD           =     0
FORWARD_FAST      =     1
BACKWARD          =     2
TURN_LEFT         =     3
TURN_LEFT_MICRO   =     4
TURN_RIGHT        =     5
TURN_RIGHT_MICRO  =     6
GRAB              =     10
RELEASE           =     11
BACKWARD_LEFT     =     12
BACKWARD_RIGHT    =     13




TCP_IP = "192.168.1.101"
TCP_PORT = 1931
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IP .4 & TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #this should prevent errors of "already in use"
s.bind((TCP_IP, TCP_PORT)) #bind socket

BUFFER_SIZE = 100  #  BUFFER SIZE - da controllare se aumentare o diminuire
# This function takes an int argument called backlog, which specifies the
# maximum number of  connections that are kept waiting if the application is
# already busy.
#s.listen(1)
cap = cv2.VideoCapture('rtsp://@192.168.1.21/live/ch00_0', cv2.CAP_FFMPEG)
class AcquireFrames(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global cap
        global ret
        while True:
            ret = cap.grab()

frames_grabber = AcquireFrames()

frames_grabber.start()

detectors = [
        Detector(Object("green")),
        Detector(Object("blue")),
        Detector(Object("red")),
        Detector(Object("yellow"))
    ]

detector_handler = DetectorHandler(detectors)

cv2.namedWindow('mask')
cv2.namedWindow('img')

print "Listening started"
try:
    while True: # wait connection
        conn, addr = s.accept() #accept connection
        ret, frame = cap.retrieve(ret)

        #message from the client
        message = conn.recv(BUFFER_SIZE)

        print message,'\n'

        if not message:
            print "There is no message"
            break

        input_dictionary = json.loads(message)

        leftObstacle = input_dictionary["leftObstacle"] == 0
        frontObstacle = input_dictionary["frontObstacle"] == 0
        rightObstacle = input_dictionary["rightObstacle"] == 0

        if not leftObstacle and not rightObstacle and not frontObstacle:
            detector_handler.update(frame)
            detector_handler.find_target()
            if detector_handler.target:
                server_message = detector_handler.do_action()
            else:
                server_message = FORWARD
        elif leftObstacle and rightObstacle:
            server_message = BACKWARD_RIGHT
        elif leftObstacle:
            server_message = TURN_RIGHT
        elif rightObstacle:
            server_message = TURN_LEFT
        else:
            server_message = BACKWARD_LEFT

        conn.send(str(server_message))
        frame = imutils.resize(frame, width=600)
        cv2.imshow('img', frame)
except KeyboardInterrupt:
    print "Shutting down"
    s.close()
cap.release()
cv2.destroyAllWindows()

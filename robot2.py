from __future__ import division
import json
import socket
import constants
import cv2
import threading
from DetectorHandler import DetectorHandler
import time
import numpy as np
from States import States


# globals
running = True
cap = cv2.VideoCapture('rtsp://@192.168.1.101/live/ch00_0', cv2.CAP_FFMPEG)
ret = None

# networking parameters
TCP_IP = "192.168.1.234"
TCP_PORT = 1931
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))  # bind socket
BUFFER_SIZE = 512
ticker = 0


class FramesGrabber(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global cap
        global ret
        global running
        while running:
            ret = cap.grab()


ticker = 0


def reactive(leftObstacle, rightObstacle, frontObstacle, somethingAtLeft, somethingAtRight):
    global ticker
    print "Reactive"
    if not leftObstacle and not rightObstacle and not frontObstacle:
        prev_action = str(constants.FORWARD_FAST)
        ticker += 1
        conn.send(prev_action)
    elif leftObstacle and rightObstacle:
        if somethingAtRight:
            prev_action = str(constants.BACKWARD_LEFT)
            conn.send(prev_action)
        else:
            prev_action = str(constants.BACKWARD_RIGHT)
            conn.send(prev_action)
    elif leftObstacle:
        # prev_action = str(constants.TURN_RIGHT)
        prev_action = str(constants.RIGHT_AND_FORWARD)
        conn.send(prev_action)
    elif rightObstacle:
        # prev_action = str(constants.TURN_LEFT)
        prev_action = str(constants.LEFT_AND_FORWARD)
        conn.send(prev_action)
    else:
        if somethingAtRight:
            prev_action = str(constants.BACKWARD_LEFT)
            conn.send(prev_action)
        else:
            prev_action = str(constants.BACKWARD_RIGHT)
            conn.send(prev_action)

# L'ANGOLO AUMENTA IN SENSO ANTIORARIO


def reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle, toTurn, t1, t2):
    print "ToTurn: ", toTurn
    # se non ho nulla alla mia destra ha senso orientarmi ora
    if not somethingAtRight:
        if toTurn < -t1 and not rightObstacle:
            print "Reorienting"
            if toTurn > -t2:
                prev_action = str(constants.TURN_RIGHT_MICRO)
                conn.send(prev_action)
                return True
            else:
                prev_action = str(constants.TURN_RIGHT)
                conn.send(prev_action)
                return True
    # se non ho nulla alla mia sinistra ha senso orientarmi ora
    if not somethingAtLeft:
        if toTurn > t1 and not leftObstacle:
            print "Reorienting"
            if toTurn < t2:
                prev_action = str(constants.TURN_LEFT_MICRO)
                conn.send(prev_action)
                return True

            else:
                prev_action = str(constants.TURN_LEFT)
                conn.send(prev_action)
                return True
    print "Not reoriented"
    return False


def shouldRelease(target, width):
    center_x = target.bounding_box[0][0]
    range_min = width * 0.5 - width / 6
    range_max = width * 0.5 + width / 6
    return (range_min <= center_x <= range_max)


frames_grabber = FramesGrabber()
detector_handler = DetectorHandler()
states_manager = States()

following = False
grabbed = False
prev_action = None


frames_grabber.start()
print "Grabbing frames started"
s.listen(1)
print "Listening started"

try:
    while True:
        conn, addr = s.accept()
        message = conn.recv(BUFFER_SIZE)

        # print message, '\n'

        input_dictionary = json.loads(message)

        # IR data
        leftObstacle = input_dictionary["leftObstacle"] == 0
        frontObstacle = input_dictionary["frontObstacle"] == 0
        rightObstacle = input_dictionary["rightObstacle"] == 0
        leftArmObstacle = input_dictionary["leftArmObstacle"] == 0
        rightArmObstacle = input_dictionary["rightArmObstacle"] == 0
        upObstacle = input_dictionary["upObstacle"] == 0

        # Merge IR left and right
        if grabbed:
            leftObstacle = leftObstacle or leftArmObstacle
            rightObstacle = rightObstacle or rightArmObstacle

        # Sonar data
        somethingAtLeft = 0 < input_dictionary['leftDistance'] < 30
        somethingAtRight = 0 < input_dictionary['rightDistance'] < 30

        # Compass data
        currentDegrees = input_dictionary['degrees']
        print "Degrees: ", currentDegrees
        print "Ticker: ", ticker

        targetDegrees, targetType, targetColor = states_manager.get_targets()
        print targetDegrees, targetType, targetColor

        if targetColor == "green":
            toTurn = 0
        else:
            toTurn = (targetDegrees - currentDegrees) % 360
            #  porto toTurn nell'intervallo [-180, 180]
            if toTurn > 180.0:
                toTurn -= 360.0

        ret, frame = cap.retrieve()

        if frame is not None:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            detector_handler.find_target(
                frame, following, color=targetColor, type_obj=targetType)

            # se trovi un target vai al target
            if targetType == "object":
                if detector_handler.target is not None:
                    if not (leftObstacle or frontObstacle or rightObstacle):
                        following = True
                        prev_action = str(detector_handler.do_action())
                        conn.send(prev_action)
                        continue
                    elif frontObstacle and (not upObstacle):
                        if following:
                            grabbed = True
                            prev_action = str(constants.GRAB)
                            following = False
                            conn.send(prev_action)
                            ticker = 0
                            states_manager.state_transition()
                            continue
                    else:
                        following = False
                else:
                    if frontObstacle and (not upObstacle):
                        if following:
                            grabbed = True
                            prev_action = str(constants.GRAB)
                            following = False
                            conn.send(prev_action)
                            ticker = 0
                            states_manager.state_transition()
                            continue

            else:  # se il target e' un'area
                if detector_handler.target is not None:
                    if not (leftObstacle or frontObstacle or rightObstacle):
                        prev_action = str(detector_handler.do_action())
                        if prev_action == str(constants.FORWARD):
                            ticker += 1
                        conn.send(prev_action)
                        continue
                    else:
                        if frontObstacle and grabbed:
                            if ticker > 18:
                                prev_action = str(constants.RELEASE)
                                ticker = 0
                                conn.send(prev_action)
                                states_manager.state_transition()
                                continue
                else:
                    if frontObstacle and grabbed:
                        if ticker > 18:
                            prev_action = str(constants.RELEASE)
                            ticker = 0
                            conn.send(prev_action)
                            states_manager.state_transition()
                            continue

            if reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle, toTurn, 5, 20):
                continue

            reactive(leftObstacle, rightObstacle, frontObstacle,
                     somethingAtLeft, somethingAtRight)

        else:
            prev_action = '0'
            conn.send('0')  # send NOP
            print "Frame is none"


except KeyboardInterrupt:
    print "Shutting down"

running = False
cap.release()
print "Capture device released"
cv2.destroyAllWindows()
print "Windows cleared"
s.close()
frames_grabber.join()
print "Socket closed"

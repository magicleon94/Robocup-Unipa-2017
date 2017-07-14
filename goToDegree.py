import json
import socket
import constants
import cv2
import threading
from DetectorHandler import DetectorHandler
import time

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


class FramesGrabber(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global cap
        global ret
        global running
        while running:
            ret = cap.grab()


def reactive(leftObstacle, rightObstacle, frontObstacle):
    print "Reactive"
    if not leftObstacle and not rightObstacle and not frontObstacle:
        conn.send(str(constants.FORWARD_FAST))
    elif leftObstacle and rightObstacle:
        conn.send(str(constants.BACKWARD))
    elif leftObstacle:
        conn.send(str(constants.TURN_RIGHT))
    elif rightObstacle:
        conn.send(str(constants.TURN_LEFT))
    else:
        conn.send(str(constants.BACKWARD_LEFT))


def reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle, toTurn, t1, t2):

    print "ToTurn: ", toTurn
    print "Left: ", leftObstacle
    print "Right: ", rightObstacle

    # se non ho nulla alla mia destra ha senso orientarmi ora
    if not somethingAtRight:
        if toTurn > t1 and not rightObstacle:
            print "Reorienting"
            if toTurn < t2:
                conn.send(str(constants.TURN_RIGHT_MICRO))
                return True
            else:
                conn.send(str(constants.TURN_RIGHT))
                return True
    # se non ho nulla alla mia sinistra ha senso orientarmi ora
    if not somethingAtLeft:
        if toTurn < -t1 and not leftObstacle:
            print "Reorienting"
            if toTurn < -t2:
                conn.send(str(constants.TURN_LEFT_MICRO))
                return True

            else:
                conn.send(str(constants.TURN_LEFT))
                return True
    print "Not reoriented"
    return False


frames_grabber = FramesGrabber()
detector_handler = DetectorHandler()

targetDegrees = constants.OBJECTS_FROM_START_DEGREE
following = False
targedColor = 'red'
targetType = 'object'

frames_grabber.start()
print "Grabbing frames started"
s.listen(1)
print "Listening started"
try:
    while True:
        conn, addr = s.accept()
        message = conn.recv(BUFFER_SIZE)

        print message, '\n'

        input_dictionary = json.loads(message)

        # IR data
        leftObstacle = input_dictionary["leftObstacle"] == 0
        frontObstacle = input_dictionary["frontObstacle"] == 0
        rightObstacle = input_dictionary["rightObstacle"] == 0
        upObstacle = input_dictionary["upObstacle"] == 0

        # Sonar data
        somethingAtLeft = 0 < input_dictionary['leftDistance'] < 20
        somethingAtRight = 0 < input_dictionary['rightDistance'] < 20

        # Compass data
        currentDegrees = input_dictionary['degrees']
        toTurn = targetDegrees - currentDegrees

        print "Degrees to turn: ", toTurn

        ret, frame = cap.retrieve()

        # if reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle, toTurn, 5, 20):
        # continue

        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            detector_handler.find_target(
                frame, color=targedColor, type_obj=targetType)
            cv2.imshow('frame', frame)
            # se trovi un target vai al target
            if detector_handler.target is not None:
                rect_width = detector_handler.target.bounding_box[1][0] * \
                    detector_handler.target.bounding_box[1][1]
                print "Rect area: ", rect_width
                if not (leftObstacle or frontObstacle or rightObstacle):
                    following = True
                    conn.send(str(detector_handler.do_action()))
                    print "Going to object"
                    continue
                else:
                    if targetType == 'object':
                        if (not upObstacle) and frontObstacle:
                            print "grabbing object"
                            targetDegrees = constants.AREA_RED_FROM_OBJECTS_DEGREE
                            targetType = 'area'
                            conn.send(str(constants.GRAB))
                            continue
                    if targetType == 'area':
                        if upObstacle and frontObstacle:
                            targetDegrees = constants.OBJECTS_FROM_RED_AREA_DEGREE
                            targetType = 'object'
                            conn.send(str(constants.RELEASE))
                            continue

            # no proper target found, adjust the orientation
            if reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle, toTurn, 5, 10):
                continue

            reactive(leftObstacle, rightObstacle, frontObstacle)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            conn.send('0')  # send NOP
            print "Frame is none"


except KeyboardInterrupt:
    print "Shutting down"

running = False
frames_grabber.join()
cap.release()
print "Capture device released"
cv2.destroyAllWindows()
print "Windows cleared"
s.close()
print "Socket closed"

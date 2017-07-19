import json
import socket
import constants
import cv2
import threading
from DetectorHandler import DetectorHandler
import time
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


class FramesGrabber(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global cap
        global ret
        global running
        while running:
            ret = cap.grab()


def reactive(leftObstacle, rightObstacle, frontObstacle, somethingAtLeft, somethingAtRight):
    print "Reactive"
    if not leftObstacle and not rightObstacle and not frontObstacle:
        conn.send(str(constants.FORWARD_FAST))
    elif leftObstacle and rightObstacle:
        if somethingAtRight:
            conn.send(str(constants.BACKWARD_LEFT))
        else:
            conn.send(str(constants.BACKWARD_RIGHT))
    elif leftObstacle:
        conn.send(str(constants.TURN_RIGHT))
    elif rightObstacle:
        conn.send(str(constants.TURN_LEFT))
    else:
        if somethingAtRight:
            conn.send(str(constants.BACKWARD_LEFT))
        else:
            conn.send(str(constants.BACKWARD_RIGHT))





###### SE L'ANGOLO AUMENTA IN SENSO ORARIO #########
def reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle, toTurn, t1, t2):
    print "ToTurn: ", toTurn
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
            if toTurn > -t2:
                conn.send(str(constants.TURN_LEFT_MICRO))
                return True

            else:
                conn.send(str(constants.TURN_LEFT))
                return True
    print "Not reoriented"
    return False

# #### SE L'ANGOLO AUMENTA IN SENSO ANTIORARIO
# def reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle, toTurn, t1, t2):
#     print "ToTurn: ", toTurn
#     # se non ho nulla alla mia destra ha senso orientarmi ora
#     if not somethingAtRight:
#         if toTurn < -t1 and not rightObstacle:
#             print "Reorienting"
#             if toTurn > -t2:
#                 conn.send(str(constants.TURN_RIGHT_MICRO))
#                 return True
#             else:
#                 conn.send(str(constants.TURN_RIGHT))
#                 return True
#     # se non ho nulla alla mia sinistra ha senso orientarmi ora
#     if not somethingAtLeft:
#         if toTurn > t1 and not leftObstacle:
#             print "Reorienting"
#             if toTurn < t2:
#                 conn.send(str(constants.TURN_LEFT_MICRO))
#                 return True
#
#             else:
#                 conn.send(str(constants.TURN_LEFT))
#                 return True
#     print "Not reoriented"
#     return False

frames_grabber = FramesGrabber()
detector_handler = DetectorHandler()
states_manager = States()

following = False
grabbed = False

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
        upSonar = input_dictionary["upSonar"]
        upObstacle = 0 < upSonar < 10

        # Sonar data
        somethingAtLeft = 0 < input_dictionary['leftDistance'] < 30
        somethingAtRight = 0 < input_dictionary['rightDistance'] < 30

        # Compass data
        currentDegrees = input_dictionary['degrees']
        print "Degrees: ", currentDegrees
        # print "Up Sonar: ", upSonar
        targetDegrees, targetType, targetColor = states_manager.get_targets()
        print targetDegrees, targetType, targetColor
        # if targetType == "area" and targetColor == "blue":
        #    targetColor = "green"

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
                frame, color=targetColor, type_obj=targetType)

            # if targetColor == "blue" and targetType == "area" and detector_handler.target is None:
            #     targetColor = "green"
            #     detector_handler.find_target(
            #         frame, color=targetColor, type_obj=targetType)

            # se trovi un target vai al target
            if detector_handler.target is not None:
                # rect_area = detector_handler.target.bounding_box[1][0] * \
                #    detector_handler.target.bounding_box[1][1]
                if not (leftObstacle or frontObstacle or rightObstacle):  # se non ci sono ostacoli
                    following = True
                    if grabbed:
                        if 10 < upSonar < detector_handler.target.obj.distanceAreaRelease:
                            conn.send(str(constants.RELEASE))
                            grabbed = False
                            states_manager.state_transition()
                            continue
                        else:
                            conn.send(str(detector_handler.do_action()))
                            print "Going to target"
                            continue
                    else:
                        conn.send(str(detector_handler.do_action()))
                        print "Going to target"
                        continue
                else:
                    if targetType == 'object':
                        if (not upObstacle) and frontObstacle:
                            print "grabbing object"
                            states_manager.state_transition()
                            conn.send(str(constants.GRAB))
                            grabbed = True
                            continue
                        #else:
                        #    conn.send(str(constants.BACKWARD))

            # no proper target found, adjust the orientation
            if reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle, toTurn, 5, 20):
                continue

            reactive(leftObstacle, rightObstacle, frontObstacle,
                     somethingAtLeft, somethingAtRight)

        else:
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

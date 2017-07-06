import json
import socket
import constants
import cv2
import threading
from DetectorHandler import DetectorHandler
import time

running = True

TCP_IP = "192.168.1.234"
TCP_PORT = 1931
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IP .4 & TCP
# this should prevent errors of "already in use"
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))  # bind socket

BUFFER_SIZE = 512

cap = cv2.VideoCapture('rtsp://@192.168.1.101/live/ch00_0', cv2.CAP_FFMPEG)

ret = None
class AcquireFrames(threading.Thread):
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
        conn.send(str(constants.FORWARD))
    elif leftObstacle and rightObstacle:
        conn.send(str(constants.BACKWARD))
    elif leftObstacle:
        conn.send(str(constants.TURN_RIGHT))
    elif rightObstacle:
        conn.send(str(constants.TURN_LEFT))
    else:
        conn.send(str(constants.BACKWARD_LEFT))

targetDegrees = constants.OBJECTS_DEGREE
def reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle, toTurn):
    print "Reorienting"
    print "ToTurn: ", toTurn
    print "Left: ", leftObstacle
    print "Right: ", rightObstacle

    # se non ho nulla alla mia destra ha senso orientarmi ora
    if not somethingAtRight:
        if toTurn > 5.0 and not rightObstacle:
            if toTurn < 20.0:
                conn.send(str(constants.TURN_RIGHT_MICRO))
                return True
            else:
                conn.send(str(constants.TURN_RIGHT))
                return True
    # se non ho nulla alla mia sinistra ha senso orientarmi ora
    if not somethingAtLeft:
        if toTurn < -5.0 and not leftObstacle:
            if toTurn < -20.0:
                conn.send(str(constants.TURN_LEFT_MICRO))
                return True
            else:
                conn.send(str(constants.TURN_LEFT))
                return True
    print "Not reoriented"
    return False

frames_grabber = AcquireFrames()
frames_grabber.start()

detector_handler = DetectorHandler()

targetDegrees = constants.OBJECTS_DEGREE
following = False
targedColor = 'red'
targetType = 'object'
s.listen(1)
print "Listening started"
try:
    while True:  # wait connection
        conn, addr = s.accept()  # accept connection

        # message from the client
        message = conn.recv(BUFFER_SIZE)

        print message, '\n'

        if not message:
            print "There is no message"
            break

        input_dictionary = json.loads(message)

        leftObstacle = input_dictionary["leftObstacle"] == 0
        frontObstacle = input_dictionary["frontObstacle"] == 0
        rightObstacle = input_dictionary["rightObstacle"] == 0
        somethingAtLeft = False#0 < input_dictionary['leftDistance'] < 10
        somethingAtRight = False#0 < input_dictionary['rightDistance'] < 10
        currentDegrees = input_dictionary['degrees']
        toTurn = targetDegrees - currentDegrees
        time.sleep(0.01)
        ret, frame = cap.retrieve()

        # se il frame non e' nullo
        if frame is not None:
            cv2.imshow('frame', frame)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
            detector_handler.find_target(frame, color=targedColor, type_obj=targetType)
            print "Showing frame"
            # se trovi un target vai al target
            if detector_handler.target is not None:
                following = True
                conn.send(str(detector_handler.do_action()))
                print "Going to object"
                continue
        # se la ricerca da camera non ha prodotto risultati
            else:
                # se stavo seguendo il rosso aggiorna l'obiettivo
                if following == True:
                    targetDegrees = constants.AREA_RED_DEGREE
                    targetType = 'area'
                    following = False

                if reorient(somethingAtRight, rightObstacle, somethingAtLeft, leftObstacle,toTurn):
                    continue

                reactive(leftObstacle, rightObstacle, frontObstacle)
        else:
            conn.send('0')
            print "Frame is none"


except KeyboardInterrupt:
    print "Shutting down"
    running = False
    cap.release()
    cv2.destroyAllWindows()
    s.close()

running = False
cap.release()
cv2.destroyAllWindows()
s.close()

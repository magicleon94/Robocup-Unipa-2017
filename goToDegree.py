import json
import socket
import constants
import cv2
import threading
import DetectorHandler


TCP_IP = "192.168.1.83"
TCP_PORT = 1931
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IP .4 & TCP
# this should prevent errors of "already in use"
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))  # bind socket

BUFFER_SIZE = 512

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
        somethingAtLeft = 0 < input_dictionary['leftDistance'] < 10
        somethingAtRight = 0 < input_dictionary['rightDistance'] < 10
        currentDegrees = input_dictionary['degrees']
        toTurn = targetDegrees - currentDegrees

        ret, frame = cap.retrieve()
        # se il frame non è nullo
        if frame is not None:
            detector_handler.find_target(frame, color=targedColor, type_obj=targetType)
            # se trovi un target vai al target
            if detector_handler.target is not None:
                following = True
                conn.send(str(detector_handler.doAction))
                continue
        # se la ricerca da camera non ha prodotto risultati
        else:
            # se stavo seguendo il rosso aggiorna l'obiettivo
            if following == True:
                targetDegrees = constants.HOME_RED_DEGREE
                targetType = 'area'
            # se non ho nulla alla mia destra ha senso orientarmi ora
            if not somethingAtRight:
                if toTurn > 5.0 and not rightObstacle:
                    if toTurn < 20.0:
                        conn.send(str(constants.TURN_RIGHT_MICRO))
                        continue
                    else:
                        conn.send(str(constants.TURN_RIGHT))
                        continue
            # se non ho nulla alla mia sinistra ha senso orientarmi ora
            elif not somethingAtLeft:
                if toTurn < -5.0 and not leftObstacle:
                    if toTurn < -20.0:
                        conn.send(str(constants.TURN_LEFT_MICRO))
                        continue
                    else:
                        conn.send(str(constants.TURN_LEFT))
                        continue
            # se non posso riorientarmi vado un po' avanti reattivo
            else:
                if not leftObstacle and not rightObstacle and not frontObstacle:
                    conn.send(str(constants.FORWARD))
                    continue
                elif leftObstacle and rightObstacle:
                    conn.send(str(constants.BACKWARD))
                    continue
                elif leftObstacle:
                    conn.send(str(constants.TURN_RIGHT))
                    continue
                elif rightObstacle:
                    conn.send(str(constants.TURN_LEFT))
                    continue
                else:
                    conn.send(str(constants.BACKWARD_LEFT))
                    continue

except KeyboardInterrupt:
    print "Shutting down"
    s.close()

#this script accept a JSON, as a string, and send a string that contains an integer
#that indicates the speed

import json
import socket
import constants

DEBUG = True


TCP_IP = "192.168.1.83"
TCP_PORT = 1931
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IP .4 & TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #this should prevent errors of "already in use"
s.bind((TCP_IP, TCP_PORT)) #bind socket

BUFFER_SIZE = 512  #  BUFFER SIZE - da controllare se aumentare o diminuire
# This function takes an int argument called backlog, which specifies the
# maximum number of connections that are kept waiting if the application is
# already busy.
s.listen(1)
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

        input_dictionary = json.loads(message)

        leftObstacle = input_dictionary["leftObstacle"] == 0
        frontObstacle = input_dictionary["frontObstacle"] == 0
        rightObstacle = input_dictionary["rightObstacle"] == 0
        if not DEBUG:
            if not leftObstacle and not rightObstacle and not frontObstacle:
                server_message = constants.FORWARD
            elif leftObstacle and rightObstacle:
                server_message = constants.BACKWARD
            elif leftObstacle:
                server_message = constants.TURN_RIGHT#utils.calcRotationCode(TURN_RIGHT, 45)
            elif rightObstacle:
                server_message = constants.TURN_LEFT#utils.calcRotationCode(TURN_LEFT, 45)
            else:
                server_message = constants.BACKWARD_LEFT#utils.calcRotationCode(TURN_RIGHT, 180)
            print "Responding: ", server_message
            conn.send(str(server_message))
        else:
            conn.send(str(raw_input("Insert response\n")))
except KeyboardInterrupt:
    print "Shutting down"
    s.close()

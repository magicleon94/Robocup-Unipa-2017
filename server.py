#this script accept a JSON, as a string, and send a string that contains an integer
#that indicates the speed

import json
import socket

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
# maximum number of connections that are kept waiting if the application is
# already busy.
s.listen(1)
print "Sisteming started"
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

        if not leftObstacle and not rightObstacle and not frontObstacle:
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
except KeyboardInterrupt:
    print "Shutting down"
    s.close()

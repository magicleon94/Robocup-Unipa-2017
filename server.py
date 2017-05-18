#this script accept a JSON, as a string, and send a string that contains an integer
#that indicates the speed

import json
import socket
TCP_IP = "localhost"
TCP_PORT = 1931
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IP .4 & TCP
s.bind((TCP_IP, TCP_PORT)) #bind socket

BUFFER_SIZE = 100  #  BUFFER SIZE - da controllare se aumentare o diminuire
# This function takes an int argument called backlog, which specifies the
# maximum number of  connections that are kept waiting if the application is
# already busy.
s.listen(1)

while True: # wait connection
    conn, addr = s.accept() #accept connection

    #message from the client
    message = conn.recv(BUFFER_SIZE)

    if not message:
        print "There is no message"
        break

    input_dictionary = json.loads(message)

    # FORWARD           0
    # FORWARD_FAST      1
    # BACKWARD          2
    # TURN_LEFT         3
    # TURN_LEFT_MICRO   4
    # TURN_RIGHT        5
    # TURN_RIGHT_MICRO  6
    # GRAB              10
    # RELEASE           11
    # BACKWARD_LEFT     12
    # BACKWARD_RIGHT    13


    if input_dictionary["leftObstacle"] == 1 and input_dictionary["frontObstacle"] == 1 and input_dictionary["rightObstacle"] == 1:
        server_message = 1
    elif input_dictionary["leftObstacle"] == 0 and input_dictionary["frontObstacle"] == 1 and input_dictionary["rightObstacle"] == 1:
        server_message = 6
    elif input_dictionary["leftObstacle"] == 1 and input_dictionary["frontObstacle"] == 1 and input_dictionary["rightObstacle"] == 0 :
        server_message = 4
    elif input_dictionary["leftObstacle"] == 1 and input_dictionary["frontObstacle"] == 0 and input_dictionary["rightObstacle"] == 1:
        server_message = 6
    elif input_dictionary["leftObstacle"] == 0 and input_dictionary["frontObstacle"] == 1 and input_dictionary["rightObstacle"] == 0:
        server_message = 1
    elif input_dictionary["leftObstacle"] == 0 and input_dictionary["frontObstacle"] == 0 and input_dictionary["rightObstacle"] == 1:
        server_message = 12
    elif input_dictionary["leftObstacle"] == 1 and input_dictionary["frontObstacle"] == 0 and input_dictionary["rightObstacle"] == 0:
        server_message = 13
    else :
        server_message = 2

    #the message sent from the server must be a string or buffer
    server_message = str(server_message)

    conn.send(server_message)

s.close()

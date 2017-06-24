

planner = simulation.planner()

import json
import socket
import constants
import Planner

DEBUG = True


TCP_IP = "192.168.1.234"
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

        server_message = planner.plan(leftObstacle, rightObstacle)

        conn.send(str(server_message))

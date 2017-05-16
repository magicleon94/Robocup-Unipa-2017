#this script accept a vector from arduino and send
#a json to it
import json
import socket
TCP_IP = "192.168.1.101"
TCP_PORT = 1931
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IP .4 & TCP
s.bind((TCP_IP, TCP_PORT)) #bind socket

BUFFER_SIZE = 96  #  PENSO POTREBBE ESSERE ANCHE PIU' PICCOLO

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


    #input_vector = [left_sensor, central_sensor, right_sensor]
    input_vector = eval(message)


    if input_vector == [1, 1, 1]:
        data = {"left_engine":80,"right_engine":80,"time":200}
    elif input_vector == [0, 1, 1]:
        data = {"left_engine":80,"right_engine":0,"time":200}
    elif input_vector == [1, 1, 0]:
        data = {"left_engine":0,"right_engine":80,"time":200}
    elif input_vector == [1, 0, 1]:
        data = {"left_engine":80,"right_engine":0,"time":200}
    elif input_vector == [0, 1, 0]:
        data = {"left_engine":80,"right_engine":80,"time":100}
    elif input_vector == [0, 0, 1]:
        data = {"left_engine":0,"right_engine":-80,"time":1000}
    elif input_vector == [1, 0, 0]:
        data = {"left_engine":-80,"right_engine":0,"time":1000}
    elif input_vector == [0, 0, 0]:
        data = {"left_engine":-80,"right_engine":-80,"time":1500}

    #the message sent from the server must be a string or buffer
    server_message = str(json.dumps(data))

    conn.send(server_message)

s.close()

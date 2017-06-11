import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('192.168.1.83', 1931)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(10)
    print "Accelerometer X value: ", data

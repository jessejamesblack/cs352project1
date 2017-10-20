import binascii
import socket as syssock
import struct
import sys


# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

def init(UDPportTx, UDPportRx):  # initialize your UDP socket here
    global udpSock
    udpSock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    udpSock.bind(('', int(UDPportRx)))
    pass


class socket:
    address = ""
    def __init__(self):  # fill in your code here
        print "in __init__"
        return

    def bind(self, address):
        return

    def connect(self, address):  # fill in your code here
        print address
        socket.bind(address)
        # bind
        # create SYN header
        # send the SYN packet A
        # start the timer
        # recv SYN ACK B
        # send ACK C
        # if there is an error send header again
        return

    def listen(self, backlog):
        pass
        return

    def accept(self):
        print self.address
        # recv SYN A
        # send SYN ACK B
        # ACK C
        (clientsocket, address) = (udpSock, self.address)  # change this to your code
        print clientsocket
        print address
        return (clientsocket, address)

    def close(self):  # fill in your code here
        return

    def send(self, buffer): # fill in your code here
        # Create header
        # Send data
        # start timer
        # if time out send same packet again
        bytessent = 0
        return bytesent

    def recv(self, nbytes):
        #reason for error is it's returning and int not socket
        bytesreceived = 0  # fill in your code here
        return bytesreceived

import binascii
import socket as syssock
import struct
import sys


# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

def init(UDPportTx, UDPportRx):  # initialize your UDP socket here
    pass


class socket:
    def __init__(self):  # fill in your code here
        return

    def bind(self, address):
        return

    def connect(self, address):  # fill in your code here
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
        # recv SYN A
        # send SYN ACK B
        # ACK C
        (clientsocket, address) = (1, 1)  # change this to your code
        return (clientsocket, address)

    def close(self):  # fill in your code here
        return

    def send(self, buffer):
        # Create header
        # Send data
        # start timer
        # if time out send same packet again
        bytessent = 0  # fill in your code here
        return bytesent

    def recv(self, nbytes):
        bytesreceived = 0  # fill in your code here
        return bytesreceived

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
    def __init__(self, sock=None):  # fill in your code here
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        #return

    def bind(self, address):
        return

    def connect(self, address):  # fill in your code here
        self.sock.connect((host, port))
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
        chunks = []
        while bytesreceived < nbytes:
            chunk = self.sock.recv(min(nbytes - bytesreceived, 2048))
            if chunk == '':
                raise RuntimeError("broken")
            chunks.append(chunk)
            bytesreceived = bytesreceived + len(chunk)
        return ''.join(chunks)

import binascii
import socket as syssock
import struct
import sys
from collections import namedtuple
import time
from Queue import *
from random import *
import math
# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

socketTimeout = 0.2
packetSize = 5000
def init(UDPportTx, UDPportRx):  # initialize your UDP socket here
    global udpSock
    udpSock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    udpSock.bind(('', int(UDPportRx)))
    # global address


class socket:
    def __init__(self):  # fill in your code here
        print "in __init__"
        # self.sock = socket

        return

    def bind(self, address):
        udpSock.setsockopt(syssock.SOL_SOCKET, syssock.SO_REUSEADDR, 1)
        udpSock.bind(address)
        return

    def connect(self, address):  # fill in your code here
        self.initial_seq_no = randint(0, (math.pow(2, 64) - 1))
        self.ack_number = 0
        syn_packet = packet()
        syn_packet.create_syn(self.initial_seq_no)
        packed_syn_packet = syn_packet.packPacked()
        while True:
            udpSock.sendto(packed_syn_packet, address)
            try:
                udpSock.settimeout(socketTimeout)
                raw_paclet, sender = udpSock.recvfrom(packetSize)
                break;
            except syssock.timeout:
                time.sleep(5)
            finally:
                udpSock.settimeout(None)
        recieved_packet_header = recieved_packet_header(raw_packet[:40])

        if (recieved_packet_header.flags != 5
            or recieved_packet_header.ack_no != (syn_packet.header.sequence_no + 1)):
            print "error"
        else:
            print "connected"
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
        # print self.address
        # recv SYN A
        # send SYN ACK B
        # ACK C
        (clientsocket, address) = (udpSock, self.address)  # change this to your code
        return (clientsocket, address)

    def close(self):  # fill in your code here
        return

    def send(self, buffer):  # fill in your code here
        # Create header
        message = buffer[:8000]
        # Send data
        socket.send(udpSock, self.address)
        # start timer
        # if time out send same packet again
        bytessent = 0
        return bytessent

    def recv(self, nbytes):
        # reason for error is it's returning and int not socket
        bytesreceived = 0  # fill in your code here
        return bytesreceived

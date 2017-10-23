import binascii
import socket as syssock
import struct
import sys
from collections import namedtuple
import time
from Queue import *
from random import *
import math
import packetHeader
import packet

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

socketTimeout = 0.2
packetSize = 5000

HeaderData = '!BBBBHHLLQQLL'
UnPackedHeaderData = struct.Struct(HeaderData)

headerLength = struct.calcsize(packetSize)

SYNFlag = 0x1
FINFlag = 0x2
ACKFlag = 0x4
RESETFlag = 0x8
HASOPTFlag = 0xA0


def init(UDPportTx, UDPportRx):  # initialize your UDP socket here
    global udpSock
    udpSock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)

    if udpSock is None:
        print "Socket not created"
    else:
        print "Socket created successfully"
    #
    if UDPportTx < 1 or UDPportTx > 65535:
        UDPportTx = 27182
    if UDPportRx < 1 or UDPportRx > 65535:
        UDPportRx = 27182


class socket:
    def __init__(self):  # fill in your code here
        # self.sock = socket
        self.connections = []
        self.backlog = []
        self.connected = False
        self.last_acked = 0
        self.next_seq_num = 0
        self.next_ack_no = 0
        self.initial_seq_no = 0
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
            print "Address: ", address
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
            self.connected = True
            self.connections.append(address)
            self.next_seq_num = recieved_packet_header.ack_no
            self.last_acked = recieved_packet_header.ack_no - 1
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
        while True:
            try:
                udpSock.settimeout(socketTimeout)
                raw_packet, sender = udpSock.recvfrom(packetSize)
                print sender

                recieved_packet_header = packetHeader(raw_packet[:40])
                if (recieved_packet_header.flags != SYNFlag):
                    print "Connection request refused"
                else:
                    break
            except syssock.timeout:
                print "Socket timed out"
                time.sleep(5)
                continue
            finally:
                udpSock.settimeout(None)

        self.initial_seq_no = randint(0, (math.pow(2, 64) - 1))
        self.last_acked = recieved_packet_header.sequence_no + recieved_packet_header.payload_len - 1
        ack_packet = packet()
        ack_packet.header.flags = (SOCK352_ACK + SOCK352_SYN)
        ack_packet.header.sequence_no = self.initial_seq_no
        packed_ack_packet = ack_packet.packPacket()
        bytesSent = udpGlobalSocket.sendto(packed_ack_packet, sender)
        print bytesSent

        client_sock = self
        client_sock.connections.append(sender)
        return (client_sock, sender)
        return (clientsocket, address)

    def close(self):  # fill in your code here
        FIN_packet = packet()
        FIN_packet.header.flag = FINFlag
        packed_FIN = FIN_packet.packPacket()
        udpSock.sendto(packed_FIN, self.connections[0])
        self.connections = []
        self.backlog = []
        self.connected = False
        self.last_acked = 0
        self.next_seq_num = 0
        self.next_ack_no = 0
        self.initial_seq_no = 0
        return

    def send(self, buffer):  # fill in your code here
        global sPort  # example using a variable global to the Python module
        bytessent = 0  # fill in your code here
        payload = buffer[:4096]
        data_packet = packet()
        data_packet.header.payload_len = len(payload)
        data_packet.header.sequence_no = self.next_seq_num
        data_packet.header.ack_no = self.next_ack_no
        data_packet.payload = payload

        packed_data_packet = data_packet.packPacket()
        while True:
            bytesSent = udpSock.sendto(packed_data_packet, self.connections[0])

            try:
                HeaderData.settimeout(socketTimeout)
                raw_packet_header, sender = udpSock.recvfrom(headerLength)
                recieved_packet_header = HeaderData(raw_packet_header)
                if (recieved_packet_header.flags != ACKFlag or
                            recieved_packet_header.ack_no != (
                                    data_packet.header.sequence_no + data_packet.header.payload_len)):
                    print "No ACK"
                break

            except syssock.timeout:
                print "Timed out Resending Packet"
                continue

            finally:
                HeaderData.settimeout(None)

        self.next_seq_num = recieved_packet_header.ack_no
        self.last_acked = recieved_packet_header.ack_no - 1
        self.next_ack_no = recieved_packet_header.ack_no + 1

        print "Returning ", bytesSent
        return bytesSent - headerLength


    def recv(self, nbytes):
        print "bytes to recieve: ", nbytes
        while True:
            try:
                udpSock.settimeout(socketTimeout)
                raw_packet, sender = udpSock.recvfrom(5000)
                recieved_packet_header = HeaderData(raw_packet[:40])
                print "Packed Header: ", binascii.hexlify(raw_packet[:40])
                print "Unpacked Header: ", UnPackedHeaderData.unpack(raw_packet[:40])
                if (recieved_packet_header.flags > 0):
                    if (recieved_packet_header.flags == FINFlag):
                        udpSock.close()
                        break;

                else:
                    break

            except syssock.timeout:
                print "Socket timed out"

            finally:
                udpSock.settimeout(None)

        self.next_seq_num = recieved_packet_header.ack_no
        self.last_acked = recieved_packet_header.ack_no - 1
        self.next_ack_no = recieved_packet_header.ack_no + 1

        payload = raw_packet[40: (40 + nbytes)]
        print "payload length: ", len(payload)

        ack_packet = packet()
        ack_packet.create_ack(recieved_packet_header)
        print "Ack Packet Ack_NO: ", ack_packet.header.ack_no
        packed_ack_packet = ack_packet.packPacket()
        udpGlobalSocket.sendto(packed_ack_packet, sender)

        return payload

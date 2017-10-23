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

class packetHeader:
    def __init__(self, rawHeader=None):
        self.header_struct = struct.Struct(sock352PktHdrData)

        if (rawHeader is None):
            self.flags = 0x0
            self.version = 0x1
            self.opt_ptr = 0x0
            self.protocol = 0x0
            self.checksum = 0x0
            self.sequence_no = 0x0
            self.source_port = 0x0
            self.ack_no = 0x0
            self.dest_port = 0x0
            self.window = 0x0
            self.payload_len = 0
        else:
            self.unpackHeader(rawHeader)

    def packPacketHeader(self):
        return self.header_struct.pack(self.version, self.flags, self.opt_ptr, self.protocol,
                                       struct.calcsize(sock352PktHdrData),
                                       self.checksum, self.source_port, self.dest_port, self.sequence_no, self.ack_no,
                                       self.window, self.payload_len)

    def unpackHeader(self, rawUDPHeader):
        if len(rawUDPHeader) < 40:
            print ("Corrupt Packet, Invalid Header Data")
            return -1

        header_array = self.header_struct.unpack(rawUDPHeader)
        self.version = header_array[0]
        self.flags = header_array[1]
        self.opt_ptr = header_array[2]
        self.protocol = header_array[3]
        self.headerLength = header_array[4]
        self.checksum = header_array[5]
        self.source_port = header_array[6]
        self.dest_port = header_array[7]
        self.sequence_no = header_array[8]
        self.ack_no = header_array[9]
        self.window = header_array[10]
        self.payload_len = header_array[11]
        return header_array
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

class packet:
    def __init__(self, header=None, payload=None):
        if header is None:
            self.header = packetHeader()
        else:
            self.header = header
        if payload is None:
            self.payload = None
        else:
            self.payload = payload
            self.header.payload_len = len(self.payload)
        pass

    def packPacket(self):
        packed_header = self.header.packPacketHeader()

        if (self.payload is None):
            packed_packet = packed_header
        else:
            packed_packet = packed_header + self.payload

        return packed_packet

    def create_ack(self, recievedHeader):
        self.header.ack_no = recievedHeader.sequence_no + recievedHeader.payload_len
        self.header.sequence_no = recievedHeader.ack_no + 1;
        self.header.flags = ACKFlag;

    def create_syn(self, seq_num):
        self.header.flags = SYNFlag
        self.header.sequence_no = seq_num

import binascii
import socket as syssock
import struct
import sys
import random

transmit = -1
rcv = -1
sock = (0, 0)
hostAddress = ""
sequenceNumber = 0
packetHeaderData = "!8BLLBB"
ver = 0x1
pointer = 0x0
protocol = 0x0
checksum = 0x0
sourcePort = 0x0
destPort = 0x0
window = 0x0
headerLength = 18
dataSent = ""

SOCK352_SYN = 0x01
SOCK352_FIN = 0x02
SOCK352_ACK = 0x04
SOCK352_RESET = 0x08
SOCK352_HAS_OPT = 0xA0

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from


def init(UDPportTx, UDPportRx):  # initialize your UDP socket here
    global sock, transmit, rcv

    sock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    rcv = int(UDPportRx)
    if(UDPportTx == ''):
        transmit = rcv
    else:
        transmit = int(UDPportTx)
    sock.bind(('', rcv))
    sock.settimeout(2)
    return


class socket:

    def __init__(self):  # fill in your code here
        return

    def bind(self, address):
        return

    def connect(self, address):  # fill in your code here
        global sock, sequenceNumber
        sequenceNumber = int(random.randint(20, 100))
        header = self.__make_header(SOCK352_SYN, sequenceNumber, 0, 0)
        ACKFlag = -1
        while(ACKFlag != sequenceNumber):
            newHeader = self.__get_Packet()
            ACKFlag = newHeader[9]
        sock.connect((address[0], transmit))
        sequenceNumber += 1
        return

    def listen(self, buffer):
        pass
        return

    def accept(self):  # change this to your code
        global sock, rcv, sequenceNumber
        flag = -1
        newHeader = ""
        while(flag != SOCK352_SYN):
            newHeader = self.__get_Packet()
            flag = newHeader[1]
        sequenceNumber = newHeader[8]
        header = self.__make_header(SOCK352_ACK, 0, sequenceNumber, 13)
        sock.sendto(header + "accepted", hostAddress)
        sequenceNumber += 1
        clientsocket = socket()
        return (clientsocket, hostAddress)

    def close(self):  # fill in your code here
        terminal = random.randint(7, 19)
        header = self.__make_header(SOCK352_FIN, terminal, 0, 0)
        ACKFlag = -1

        while(ACKFlag != terminal):
            try:
                sock.sendto(header, hostAddress)
            except TypeError:
                sock.send(header)
            newHeader = self.__get_Packet()
            ACKFlag = newHeader[9]
        sock.close()
        return

    def send(self, buffer):
        global sock, headerLength, sequenceNumber

        bytessent = 0  # fill in your code here
        messageLength = len(buffer)

        while(messageLength > 0):
            message = buffer[:255]
            messageHeader = self.__make_header(
                0x03, sequenceNumber, 0, len(message))
            temp = 0
            ACKFlag = -1
            while(ACKFlag != sequenceNumber):
                temp = sock.send(messageHeader + message) - headerLength
                newHeader = self.__get_Packet()
                ACKFlag = newHeader[9]

            messageLength -= 255
            buffer = buffer[255:]
            bytessent += temp
            sequenceNumber += 1
        return bytessent

    def recv(self, bytesreceived):
        global sock, dataSent, sequenceNumber
        bytesreceived = 0  # fill in your code here
        dataSent = ""
        sendMessage = ""
        while(bytesreceived > 0):
            num = -1

            while(num != sequenceNumber):
                newHeader = self.__get_Packet()
                num = newHeader[8]
                if(num != sequenceNumber):
                    print("error in recv")
                header = self.__make_header(SOCK352_ACK, 0, num, 0)
                sock.sendto(header, hostAddress)
            sendMessage += dataSent
            bytesreceived -= len(dataSent)

            sequenceNumber += 1
        return sendMessage

    def __get_Packet(self):
        global sock, packetHeaderData, hostAddress, dataSent

        try:
            (data, senderAddress) = sock.recvfrom(4096)
        except syssock.timeout:
            error = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return error

        (data_header, data_msg) = (data[:18], data[18:])
        header = struct.unpack(packetHeaderData, data_header)
        flag = header[1]

        if(flag == SOCK352_SYN):
            hostAddress = senderAddress
            return header

        elif(flag == SOCK352_FIN):
            terminalHeader = self.__make_header(SOCK352_ACK, 0, header[8], 0)
            sock.sendto(terminalHeader, senderAddress)
            return header

        # elif(flag == 0x03):
            # dataSent = data_msg
            # return header
        elif(flag == SOCK352_ACK):
            return header

        elif(flag == SOCK352_RESET):
            return header

        else:
            header = self.__make_header(SOCK352_RESET, header[8], header[9], 0)
            if(sock.sendto(header, senderAddress) > 0):
                print("Reset")
            else:
                print("Error in reset")
            return header

    def __make_header(self, givenFlag, givenSeqNo, givenAckNo, givenPayload):
        global packetHeaderData, headerLength, ver, pointer, protocol
        global checksum, sourcePort, destPort, window

        flags = givenFlag
        sequence_no = givenSeqNo
        ack_no = givenAckNo
        payload_len = givenPayload
        udpPkt_hdr_data = struct.Struct(packetHeaderData)
        return udpPkt_hdr_data.pack(ver, flags, pointer, protocol,
                                    headerLength, checksum, sourcePort, destPort, sequence_no,
                                    ack_no, window, payload_len)

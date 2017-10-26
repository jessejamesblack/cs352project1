
import binascii
import socket as syssock
import struct
import sys
import random

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

# init stuff
transmit = -1
recv = -1
socket = (0, 0)
hostAddress = ""
sequenceNumber = 0
packetHeaderData = "!8BLLBB"
version = 0x1
pointer = 0x0
protocol = 0x0
checksum = 0x0
sourcePort = 0x0
destPort = 0x0
window = 0x0
headerLength = 18
dataSent = ""

# defines all UDP ports


def init(UDPportTx, UDPportRx):   # initialize your UDP socket here
    global socket, transmit, recv
    # create a UDP/datagram socket
    # bind the port to the Rx (receive) port number
    socket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    recv = int(UDPportRx)
    if UDPportTx == '':
        transmit = recv
    else:
        transmit = int(UDPportTx)
    socket.bind(('', recv))
    # Our protocol defines a timeout of 0.2 seconds
    socket.settimeout(0.2)
    print('Initialization complete!')
    pass


class socket:

    def __init__(self):  # fill in your code here
        print("New Socket created")
        return

    def bind(self, address):
        print("Binding")
        return

    def connect(self, address):  # fill in your code here
        global socket, sequenceNumber

        # create sequence number
        sequenceNumber = int(random.randint(20, 100))

        # create header for packet  with SYN flags
        packetHeader = self.makeHeader(0x01, sequenceNumber, 0, 0)
        ackFLAG = -1

        # set the timeout, wait for SYN, retransmit if needed
        while(ackFLAG != sequenceNumber):
            print("New connection being made")
            newHeader = self.getPacket()
            ackFLAG = newHeader[9]

        socket.connect((address[0], transmit))

        sequenceNumber += 1
        return

    def listen(self, backlog):
        pass
        return

    def accept(self):
        global socket, recv, sequenceNumber

        print("Waiting connection")
        flag = -1
        newHeader = ""

        # call get packet
        while(flag != 0x01):
            newHeader = self.getPacket()
            flag = newHeader[1]
        sequenceNumber = newHeader[8]
        # ACK
        header = self.makeHeader(0x04, 0, sequenceNumber, 13)
        socket.sendto(header + "accepted", hostAddress)

        # accept new datagrams
        sequenceNumber += 1
        print("target acquired")
        clientsocket = socket(0)
        #(clientsocket, address) = (1, 1)  # change this to your code
        return (clientsocket, hostAddress)

    def close(self):   # fill in your code here
        # send FIN
        print("Goodbye")
        # new header with random sequence number
        termNumber = random.randint(7, 19)
        header = self.makeHeader(0x02, termNumber, 0, 0)
        ackFLAG = -1

        # set timeout and wait for ACK, etc
        while(ackFLAG != termNumber):
            try:
                socket.sendto(header, hostAddress)
            except TypeError:
                socket.send(header)
            newHeader = self.getPacket()
            ackFLAG = newHeader[9]

        socket.close()
        return

    def send(self, buffer):
        global socket, headerLength, sequenceNumber
        bytessent = 0     # fill in your code here
        messageLength = len(buffer)

        print("Sending")
        while(messageLength > 0):
            package = buffer[:255]
            packageHeader = self.makeHeader(
                0x03, sequenceNumber, 0, len(package))
            temp = 0
            ackFLAG = -1
            while(ackFLAG != sequenceNumber):
                temp = socket.send(packageHeader + package) - headerLength
                newHeader = self.getPacket()
                ackFLAG = newHeader[9]

            messageLength -= 255
            buffer = buffer[255:]
            bytessent += temp
            sequenceNumber += 1
        return bytessent

    def recv(self, nbytes):
        global socket, dataSent, sequenceNumber
        bytesreceived = 0     # fill in your code here
        print("starting recv")
        datasent = ""

        message = ""
        while(bytesreceived > 0):
            num = -1
            while(num != sequenceNumber):
                newHeader = self.getPacket()
                num = newHeader[8]
                if(num != sequenceNumber):
                    print("Error in recv")

                header = self.makeHeader(0x04, 0, num, 0)
                socket.sendto(header, hostAddress)

            message += datasent
            bytesreceived -= len(datasent)

            sequenceNumber += 1
        print("fin")
        return message

    # had to create a packet function

    def getPacket(self):
        global socket, packetHeaderData, hostAddress, dataSent

        try:
            (data, senderAddress) = socket.recvfrom(4096)
        except syssock.timeout:
            print("error in timeout")
            error = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return error

        (dataHeader, dataMessage) = (data[:18], data[18:])
        header = struct.unpack(packetHeaderData, dataHeader)
        flag = header[1]
        if (flag == 0x01):
            hostAddress = senderAddress
            return header

        elif (flag == 0x02):
            termHeader = self.makeHeader(0x04, 0, header[8], 0)
            socket.sendto(termHeader, senderAddress)
            return header

        elif(flag == 0x03):
            dataSent = dataMessage
            return header

        elif(flag == 0x04):
            return header

        elif (flag == 0x08):
            return header

        else:
            header = self.makeHeader(0x08, header[8], header[9], 0)

            if(socket.sendto(header, senderAddress) > 0):
                print("Reset")
            else:
                print("Failed")
            return header

    def makeHeader(self, flag, sequenceNumber, ACK, Payload):
        global packetHeaderData, headerLength, version, pointer, protocol
        global checksum, sourcePort, destPort, window

        flag = flag
        sequenceNumber = sequenceNumber
        ACKNum = ACK
        payloadLength = Payload

        udpPkt_hdr_data = struct.Struct(packetHeaderData)

        return udpPkt_hdr_data.pack(version, flag, pointer, protocol, headerLength, checksum, sourcePort, destPort, sequenceNumber, ACKNum, window, payloadLength)

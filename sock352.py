import binascii
import socket as syssock
import struct
import sys
import random

transmitter = -1
receiver = -1
mainSocket = (0, 0)
otherHostAddress = ""
currentSeqNo = 0
sock352PktHdrData = "!BBBBHHLLQQLL"


version = 0x1
opt_ptr = 0x0
protocol = 0x0
checksum = 0x0
source_port = 0x0
dest_port = 0x0
window = 0x0
header_len = 40
deliveredData = ""

SOCK352_SYN = 0x01
SOCK352_FIN = 0x02
SOCK352_ACK = 0x04
SOCK352_RESET = 0x08
SOCK352_HAS_OPT = 0xA0


# this init function is global to the class and
# defines the UDP ports all messages are sent
# and received from.
def init(UDPportTx, UDPportRx):
    global mainSocket, transmitter, receiver

    mainSocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    receiver = int(UDPportRx)
    if(UDPportTx == ''):
        transmitter = receiver
    else:
        transmitter = int(UDPportTx)
    mainSocket.bind(('', receiver))
    mainSocket.settimeout(2)
    return


class socket:

    def __init__(self):
        return

    def bind(self, address):
        pass
        return

    def connect(self, address):
        global mainSocket, currentSeqNo, sock352PktHdrData, header_len, version, opt_ptr, protocol, checksum, \
            source_port, dest_port, window
        print("Starting connection on %s" % (transmitter))

        currentSeqNo = int(random.randint(20, 100))

        header1 = struct.Struct(sock352PktHdrData)

        flags = 0x01
        sequence_no = currentSeqNo
        ack_no = 0
        payload_len = 0

        header = header1.pack(version, flags, opt_ptr, protocol,
                                    header_len, checksum, source_port, dest_port, sequence_no,
                                    ack_no, window, payload_len)

        ackFlag = -1

        while(ackFlag != currentSeqNo):
            print("Total sent %d" % (mainSocket.sendto(header,
                                                       (address[0], transmitter))))
            newHeader = self.__sock352_get_packet()
            ackFlag = newHeader[9]

        mainSocket.connect((address[0], transmitter))

        currentSeqNo += 1
        return

    def accept(self):
        global mainSocket, receiver, currentSeqNo

        print('Awaiting connection at %s\n' % (receiver))
        flag = -1
        newHeader = ""

        while(flag != 0x01):
            newHeader = self.__sock352_get_packet()
            flag = newHeader[1]
        currentSeqNo = newHeader[8]
        # Acknowledge this new connection
        ####################
        header1 = struct.Struct(sock352PktHdrData)

        flags = 0x04
        sequence_no = 0
        ack_no = currentSeqNo
        payload_len = 13

        header = header1.pack(version, flags, opt_ptr, protocol,
                              header_len, checksum, source_port, dest_port, sequence_no,
                              ack_no, window, payload_len)
        ##################
        mainSocket.sendto(header + " accepted", otherHostAddress)

        currentSeqNo += 1
        print("Target acquired")
        clientsocket = socket()
        print("Connection closed")
        return (clientsocket, otherHostAddress)

    def close(self):

        terminal_no = random.randint(7, 19)

        ###################
        header1 = struct.Struct(sock352PktHdrData)

        flags = 0x02
        sequence_no = terminal_no
        ack_no = 0
        payload_len = 0

        header = header1.pack(version, flags, opt_ptr, protocol,
                              header_len, checksum, source_port, dest_port, sequence_no,
                              ack_no, window, payload_len)

        ####################
        ackFlag = -1
        while(ackFlag != terminal_no):
            try:
                mainSocket.sendto(header, otherHostAddress)
            except TypeError:
                mainSocket.send(header)
            newHeader = self.__sock352_get_packet()
            ackFlag = newHeader[9]
        mainSocket.close()
        return

    def listen(self, buffer):
        pass
        return

    def send(self, buffer):
        global mainSocket, header_len, currentSeqNo

        bytesSent = 0
        msglen = len(buffer)

        while(msglen > 0):
            parcel = buffer[:255]

            ######################
            header1 = struct.Struct(sock352PktHdrData)

            flags = 0x05
            sequence_no = currentSeqNo
            ack_no = 0
            payload_len = len(parcel)

            parcelHeader = header1.pack(version, flags, opt_ptr, protocol,
                                  header_len, checksum, source_port, dest_port, sequence_no,
                                  ack_no, window, payload_len)
            ######################
            tempBytesSent = 0
            ackFlag = -1
            while(ackFlag != currentSeqNo):
                tempBytesSent = mainSocket.send(
                    parcelHeader + parcel) - header_len

                newHeader = self.__sock352_get_packet()
                ackFlag = newHeader[9]

            msglen -= 255
            buffer = buffer[255:]
            bytesSent += tempBytesSent
            currentSeqNo += 1
        print("One segment of %d total bytes was sent!" % bytesSent)
        return bytesSent

    def recv(self, bytes_to_receive):
        global mainSocket, deliveredData, currentSeqNo

        deliveredData = ""
        fullMessage = ""
        while(bytes_to_receive > 0):
            seq_no = -1
            while(seq_no != currentSeqNo):
                newHeader = self.__sock352_get_packet()
                seq_no = newHeader[8]
                if(seq_no != currentSeqNo):
                    print("Error in recv at %d" % currentSeqNo)
                ###############
                header1 = struct.Struct(sock352PktHdrData)

                flags = 0x04
                sequence_no = 0
                ack_no = currentSeqNo
                payload_len = 0

                header = header1.pack(version, flags, opt_ptr, protocol,
                                      header_len, checksum, source_port, dest_port, sequence_no,
                                      ack_no, window, payload_len)
                ###############
                mainSocket.sendto(header, otherHostAddress)
            fullMessage += deliveredData
            bytes_to_receive -= len(deliveredData)
            # Get ready to expect the next packet
            currentSeqNo += 1
        print("Finished RECV")
        return fullMessage

    def __sock352_get_packet(self):
        global mainSocket, sock352PktHdrData, otherHostAddress, deliveredData
        try:
            (data, senderAddress) = mainSocket.recvfrom(5000)
        except syssock.timeout:
            print("No packets recived in timeout window!")
            z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return z

        # Randomly pretend this packet got dropped or corrupted
        """
        if(random.randint(1,3) == 2):
            print("\t\tIncoming packet got dropped! Timeout.")
            #z = self.__make_header(1,1,1,1)
            #print("\t\tAssembled this header: ")
            #print(z)
            z = [0,0,0,0,0,0,0,0,0,0,0,0]
            return z
        """
        (data_header, data_msg) = (data[:40], data[40:])
        header = struct.unpack(sock352PktHdrData, data_header)
        flag = header[1]

        if(flag == 0x01):
            otherHostAddress = senderAddress
            return header
        elif(flag == 0x02):
            ###############
            header1 = struct.Struct(sock352PktHdrData)

            flags = 0x04
            sequence_no = 0
            ack_no = header[8]
            payload_len = 0

            terminalHeader = header1.pack(version, flags, opt_ptr, protocol,
                                  header_len, checksum, source_port, dest_port, sequence_no,
                                  ack_no, window, payload_len)
            ###############
            mainSocket.sendto(terminalHeader, senderAddress)
            return header

        elif(flag == 0x05):
            deliveredData = data_msg
            return header
        elif(flag == 0x04):
            return header

        elif(flag == 0x08):
            return header

        else:

            #####################
            header1 = struct.Struct(sock352PktHdrData)

            flags = 0x08
            sequence_no = header[8]
            ack_no = header[9]
            payload_len = 0

            header = header1.pack(version, flags, opt_ptr, protocol,
                                  header_len, checksum, source_port, dest_port, sequence_no,
                                  ack_no, window, payload_len)
            #####################
            if(mainSocket.sendto(header, senderAddress) > 0):
                print("Reset packet sent")
            else:
                print("Reset packet failed to send")
            return header
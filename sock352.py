import binascii
import socket as syssock
import struct
import sys
import random
import math

port = -1
recv = -1
sock = (0, 0)
address = ''
curr = 0
sock352PktHdrData = '!BBBBHHLLQQLL'



version = 0x1
#flags
SOCK352_SYN = 0x01  
SOCK352_FIN = 0x02
SOCK352_ACK = 0x04
SOCK352_RESET = 0x08
SOCK352_HAS_OPT = 0xA0
SOCK352_FLAG = 0x05
opt_ptr = 0x0
protocol = 0x0
header_len = 40
checksum = 0x0
source_port = 0x0
dest_port = 0x0
sequence_no = 0x0
ack_no = 0x0
window = 0x0
data = ''


# this init function is global to the class and
# defines the UDP ports all messages are sent
# and received from.
def init(UDPportTx, UDPportRx):     # initialize your UDP socket here 
    global sock, port, recv

    sock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    recv = int(UDPportRx)
    if(UDPportTx == ''):
        port = recv
    else:
        port = int(UDPportTx)
    sock.bind(('', recv))
    sock.settimeout(5)
    return


class socket:

    def __init__(self):     # fill in your code here 
        return

    def bind(self, address):
        pass
        return

    def connect(self, address):     # fill in your code here 
        global sock, curr, sock352PktHdrData, header_len, version, opt_ptr, protocol, checksum, \
            source_port, dest_port, window

        curr = random.randint(10, 100)

        header1 = struct.Struct(sock352PktHdrData)

        flags = SOCK352_SYN
        sequence_no = curr
        ack_no = 0
        payload_len = 0

        header = header1.pack(version, flags, opt_ptr, protocol,
                                    header_len, checksum, source_port, dest_port, sequence_no,
                                    ack_no, window, payload_len)

        ACKFlag = -1

        while(ACKFlag != curr):
            print("Total sent %d" % (sock.sendto(header,(address[0], port))))
            newHeader = self.packet()
            ACKFlag = newHeader[9]

        sock.connect((address[0], port))

        curr += 1
        print("Connection achieved")
        return

    def listen(self, backlog):
        pass
        return

    def accept(self):
        global sock, recv, curr
        flag = -1
        newHeader = ""

        while(flag != SOCK352_SYN):
            newHeader = self.packet()
            flag = newHeader[1]
        curr = newHeader[8]

        ####################
        header1 = struct.Struct(sock352PktHdrData)

        flags = SOCK352_ACK
        sequence_no = 0
        ack_no = curr
        payload_len = 13

        header = header1.pack(version, flags, opt_ptr, protocol,
                              header_len, checksum, source_port, dest_port, sequence_no,
                              ack_no, window, payload_len)
        ##################
        sock.sendto(header + " accepted", address)

        curr += 1
        print("Target acquired")
        clientsocket = socket()
       # (clientsocket, address) = (1,1)     # change this to your code
        return (clientsocket, address)      

    def close(self):    # fill in your code here 

        temp = random.randint(10, 100)

        ###################
        header1 = struct.Struct(sock352PktHdrData)

        flags = SOCK352_FIN
        sequence_no = temp
        ack_no = 0
        payload_len = 0

        header = header1.pack(version, flags, opt_ptr, protocol,
                              header_len, checksum, source_port, dest_port, sequence_no,
                              ack_no, window, payload_len)

        ####################
        ACKFlag = -1
        while(ACKFlag != temp):
            try:
                sock.sendto(header, address)
            except TypeError:
                sock.send(header)
            newHeader = self.packet()
            ACKFlag = newHeader[9]
        sock.close()
        print("Connection closed")
        return

    def send(self, buffer):
        global sock, header_len, curr

        bytessent = 0       # fill in your code here 
        length = len(buffer)

        while(length > 0):
            message = buffer[:255]

            ######################
            header1 = struct.Struct(sock352PktHdrData)

            flags = 0x05
            sequence_no = curr
            ack_no = 0
            payload_len = len(message)

            parcelHeader = header1.pack(version, flags, opt_ptr, protocol,
                                  header_len, checksum, source_port, dest_port, sequence_no,
                                  ack_no, window, payload_len)
            ######################
            temp = 0
            ACKFlag = -1
            while(ACKFlag != curr):
                temp = sock.send(
                    parcelHeader + message) - header_len

                newHeader = self.packet()
                ACKFlag = newHeader[9]

            length -= 255
            buffer = buffer[255:]
            bytessent += temp
            curr += 1
        return bytessent

    def recv(self, nbytes):
        global sock, data, curr

        data = ""
        bytesreceived  = ""
        while(nbytes > 0):
            seq_no = -1
            while(seq_no != curr):
                newHeader = self.packet()
                seq_no = newHeader[8]
            
                ###############
                header1 = struct.Struct(sock352PktHdrData)

                flags = SOCK352_ACK
                sequence_no = 0
                ack_no = curr
                payload_len = 0

                header = header1.pack(version, flags, opt_ptr, protocol,
                                      header_len, checksum, source_port, dest_port, sequence_no,
                                      ack_no, window, payload_len)
                ###############
                sock.sendto(header, address)
            bytesreceived  += data
            nbytes -= len(data)
            
            curr += 1
        print("Finished RECV")
        return bytesreceived 

    def packet(self):
        global sock, sock352PktHdrData, address, data
        try:
            (data, dest) = sock.recvfrom(8000)
        except syssock.timeout:
            print("Timeout window maxed")
            head = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return head
        (data, message) = (data[:40], data[40:])
        header = struct.unpack(sock352PktHdrData, data)
        flag = header[1]

        if(flag == SOCK352_SYN):
            address = dest
            return header
        elif(flag == SOCK352_FIN):
            ###############
            header1 = struct.Struct(sock352PktHdrData)

            flags = SOCK352_ACK
            sequence_no = 0
            ack_no = header[8]
            payload_len = 0

            terminalHeader = header1.pack(version, flags, opt_ptr, protocol,
                                  header_len, checksum, source_port, dest_port, sequence_no,
                                  ack_no, window, payload_len)
            ###############
            sock.sendto(terminalHeader, dest)
            return header

        elif(flag == SOCK352_FLAG):
            data = message
            return header
        elif(flag == SOCK352_ACK):
            return header

        elif(flag == SOCK352_RESET):
            return header

        else:

            #####################
            header1 = struct.Struct(sock352PktHdrData)

            flags = SOCK352_RESET
            sequence_no = header[8]
            ack_no = header[9]
            payload_len = 0

            header = header1.pack(version, flags, opt_ptr, protocol,
                                  header_len, checksum, source_port, dest_port, sequence_no,
                                  ack_no, window, payload_len)
            #####################
            if(sock.sendto(header, dest) > 0):
                print("Reset packet sent")
            else:
                print("Reset packet failed to send")
            return header
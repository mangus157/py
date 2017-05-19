#-*-coding:utf-8 -*-
import socket, sys
import struct

import binascii

try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error, msg:
    print "Failed to create socket. Error code : " +str(msg[0])+ " Message : " +msg[1]
    sys.exit()

data = s.recv(65565)

#Ethernet Header
ethernet_header = data[0:14]
ethernet_header = struct.unpack("!6s6s2s", ethernet_header)
print "Destination MAC Address : ", binascii.hexlify(ethernet_header)
print "Source MAC Address : ", binascii.hexlify(ethernet_header)
print

#IP Header
ip_header = data[14:34] #20Byte
ip_header = struct.unpack("!12s4s4s", ip_header) #for only src/dst IP
print "Source IP Address : ", socket.inet_ntoa(ip_header[1])
print "Destination IP Address : ", socket.inet_ntoa(ip_header[2])
print

#TCP Header
tcp_header = data[34:54]
tcp_header = struct.unpack("!2H16s", tcp_header) # for only src/dst Port

print "Source Port Number : ", tcp_header[0]
print "Destination Port Number : ", tcp_header[1]
print



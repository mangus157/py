#python 2.7
#-*-coding:utf-8 -*-
import socket
from struct import *

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

data = s.recv(65535)

ip_header = data[0:20] #extract 20 byte
ip_header = unpack("!2B3H2BH4s4s", ip_header)

version_ip_header_length = ip_header[0]
version = version_ip_header_length >> 4
ip_header_length = version_ip_header_length & 0xF
ip_header_length = ip_header_length * 4
ttl = ip_header[5]
protocol = ip_header[6]
ip_source_address = socket.inet_ntoa(ip_header[8])
ip_destination_address =socket.inet_ntoa(ip_header[9])

print "Version : ", str(version)
print "IP Header Length : ", str(ip_header_length)
print "TTL : ", str(ttl)
print "Protocol : ", str(protocol)
print "Source IP Address : ", str(ip_source_address)
print "Destination IP Address : ", str(ip_destination_address)
print

tcp_header = data[ip_header_length:ip_header_length + 20]

tcp_header = unpack("!2H2L2B3H", tcp_header)

source_port = tcp_header[0]
destination_port = tcp_header[1]
sequence_number = tcp_header[2]
acknowledgment_number = tcp_header[3]
offset_reserved = tcp_header[4]
tcp_header_length = (offset_reserved >> 4)

print "Source port number : ", str(source_port)
print "Destination port number : ", str(destination_port)
print "Sequence number : ", str(sequence_number)
print "Acknowledgment number : ", str(acknowledgment_number)
print "TCP Header Length : ", str(tcp_header_length)
print

header_size = ip_header_length + (tcp_header_length * 4)

payload_data_size = len(data) - header_size

payload_data = data[header_size:]

print "Payload Data : " + payload_data
print







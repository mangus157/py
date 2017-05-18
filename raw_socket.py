#python 2.7
#-*-coding:utf-8 -*-
import socket, sys
from struct import *

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
        s = s + w
        s = (s >> 16) + (s & 0xffff)
        s = s + (s >> 16)
        s = ~s & 0xffff
        return s

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW )
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error, msg:
    print "Failed to create socket. Error code : " + str(msg[0]) + " Messgae : " + msg[1]
    sys.exit()

#IP Header
version = 4
ip_header_length = 5
version_ip_header_length = (version << 4) + ip_header_length
tos = 0
total_length  = 0
identification = 54321
fragment_offset = 0
ttl = 255
protocol = socket.IPPROTO_TCP
ip_checksum = 0
source_ip = "127.0.0.1"
destination_ip = "127.0.0.1"
source_ip_address = socket.inet_aton(source_ip)
destination_ip_address = socket.inet_aton(destination_ip)

ip_header = pack("!2B3H2BH4s4s", version_ip_header_length, tos,
                 total_length, identification, fragment_offset, ttl, protocol,
                 ip_checksum, source_ip_address, destination_ip_address)

#TCP Header
source_port = 1234
destination_port = 22
sequence_number = 454
acknowledgment_number = 0
offset = 5
reserved = 0
offset_reserved = ( offset << 4) + reserved

fin = 0
syn = 1
rst = 0
psh = 0
ack = 0
urg = 0
flags = ( urg << 5 ) + ( ack << 4 ) + ( psh << 3 ) + ( rst << 2 ) + ( syn << 1 ) + ( fin << 0 )
window = socket.htons(5840)
tcp_checksum = 0
urg_ptr = 0

tcp_header = pack("!2H2L2B3H", source_port, destination_port, sequence_number,
                  acknowledgment_number, offset_reserved, flags, window,
                  tcp_checksum, urg_ptr)

payload_data = "Hello, how are you"

#Pseudo Header
source_ip_address = socket.inet_aton(source_ip)
destination_ip_address = socket.inet_aton(destination_ip)
place_holder = 0
protocol = socket.IPPROTO_TCP
length = len(tcp_header) + len(payload_data)

pseudo_header = pack("!4s4sBBH", source_ip_address,
                     destination_ip_address, place_holder, protocol, length)

pseudo_header = pseudo_header + tcp_header + payload_data

tcp_checksum = checksum(pseudo_header)
print "TCP_Checksum:",tcp_checksum

tcp_header = pack("!2H2L2BH", source_port, destination_port, sequence_number, acknowledgment_number,offset_reserved,
                  flags, window,) + pack("H",tcp_checksum) + pack("!H", urg_ptr)


#IP Packet
ip_packet = ip_header + tcp_header + payload_data

print s.sendto(ip_packet, (destination_ip, 0))

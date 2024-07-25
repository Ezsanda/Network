import sys
import socket
import struct

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
UDP_IP = sys.argv[3]
UDP_PORT = int(sys.argv[4])
UDP_ADDRESS = (UDP_IP,UDP_PORT)

tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_sock.connect((TCP_IP,TCP_PORT))

udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

packer = struct.Struct('1024s 1024s 1024s 1024s')

ip = input('Ip: ')
classroom = input('Classroom: ')
date = input('Date: ')
code = input('Code: ')

msg = (ip.encode(),classroom.encode(),date.encode(),code.encode())
packed_data = packer.pack(*msg)

tcp_sock.sendall(packed_data)

reply = tcp_sock.recv(packer.size)
trimmed = reply.decode().strip('\x00')

print(trimmed)

if trimmed == 'INVALID':
    udp_sock.sendto(b'GET_CAPTCHA',UDP_ADDRESS)
    udp_reply,_ = udp_sock.recvfrom(10)

    msg = (ip.encode(),classroom.encode(),date.encode(),udp_reply)
    packed_data = packer.pack(*msg)
    tcp_sock.sendall(packed_data)

    reply = tcp_sock.recv(packer.size)
    print(reply.decode().strip('\x00'))    

udp_sock.close()
tcp_sock.close()
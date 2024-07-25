import sys
import socket

UDP_IP = sys.argv[1]
UDP_PORT = int(sys.argv[2])

udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_sock.bind((UDP_IP,UDP_PORT))
udp_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

while True:
    msg,client = udp_sock.recvfrom(64)

    if msg.decode().strip('\x00') == 'GET_CAPTCHA':
        code = input('Code: ')
        udp_sock.sendto(code.encode(),client)
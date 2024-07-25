import sys
import socket
import select
import random
import json
import ipaddress
import struct
import string

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
FILE_PATH = sys.argv[3]

tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_sock.bind((TCP_IP,TCP_PORT))
tcp_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
tcp_sock.listen(5)

inputs = [tcp_sock]

code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

print(code)

with open(FILE_PATH,'r') as file:
    class_data = json.load(file)

valids = []
for i in range(len(class_data)):
    valids.append(0)

unpacker = struct.Struct('1024s 1024s 1024s 1024s')

while True:
    readables,_,_ = select.select(inputs,[],[])

    for s in readables:
        if s is tcp_sock:
            connection,client_info = tcp_sock.accept()
            inputs.append(connection)
        else:
            msg = s.recv(unpacker.size)
            if not msg:
                s.close()
                inputs.remove(s)
            else:
                unpacked_data = unpacker.unpack(msg)

                for i in range(len(class_data)):
                    valid_classroom = unpacked_data[1].decode().strip('\x00') == class_data[i]['classroom']
                    valid_date = int(unpacked_data[2].decode().strip('\x00')) >= int(class_data[i]['start']) and int(unpacked_data[2].decode().strip('\x00')) < int(class_data[i]['end'])
                    valid_code = unpacked_data[3].decode().strip('\x00') == code
                    valid_ip = ipaddress.ip_address(unpacked_data[0].decode().strip('\x00')) in ipaddress.ip_network(class_data[i]['ip'])
                        
                    if valid_classroom and valid_date and valid_code and valid_ip:
                        s.sendall(b'VALID')
                        valids[i] += 1
                    else:
                        s.sendall(b'INVALID')
                    
                    print(class_data[i])
                    print(valids[i])
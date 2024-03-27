import socket
import numpy as np
import cv2

def recvall(sock,count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)

    return buf

HOST = "192.168.31.87"
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
count = 0
while True:
    message = '1'
    client_socket.send(message.encode())
    length = recvall(client_socket, 16)
    #print(length)
    stringData = recvall(client_socket, int(length))
    data = np.frombuffer(stringData, dtype='uint8')
    if count == 0:
        print(length, "len")
        print(stringData, "std")
        print(data)
        print(type(data))
        for i in data:
            count+= 1
            print(i)
            print(count, ":c\n")

    decimg = cv2.imdecode(data, 1)
    cv2.imshow('client', decimg)
    key = cv2.waitKey(1)

client_socket.close()
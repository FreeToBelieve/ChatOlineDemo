"""
@author 赵国磊
@create 2019-09-08-15:59
"""
from socket import *


class TCP(object):
    def __init__(self, addr=('10.25.115.164', 6066), client=0):
        self.addr = addr
        self.socket = socket()
        if not client:
            self.socket.bind(self.addr)
            self.socket.listen()

    def accept(self):
        return self.socket.accept()

    def conn(self):
        self.socket.connect(self.addr)

    def client_send(self, data):
        self.socket.send(data.encode('utf-8'))

    def client_receive(self, size=2048):
        return self.socket.recv(size).decode('utf-8')

    def send(self, conn, data):
        conn.send(data.encode('utf-8'))

    def receive(self, conn, size=2048):
        return conn.recv(size).decode('utf-8')

    def close(self):
        return self.socket.close()

"""
@author 
@create 2019-09-07-16:33
"""
from socket import *


class UDP(object):
    def __init__(self):
        self.addr = ('10.25.115.164', 6066)
        self.socket = socket(type=SOCK_STREAM)
        self.socket.bind(self.addr)

    def udp_send(self, data, addr):
        self.socket.sendto(data, addr)

    def upd_receive(self):
        return self.socket.recvfrom(1024)

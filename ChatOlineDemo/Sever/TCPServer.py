"""
@author 
@create 2019-09-09-8:37
"""
import threading
from ChatOlineDemo import TCP


class TCPServer(object):
    def __init__(self, addr):
        self.tcp = TCP.TCP(addr)
        print('---监听已开启---')

    def accept(self):
        self.conn1, self.addr1 = self.tcp.accept()
        print(f'{self.conn1}已接入服务器')
        self.conn2, self.addr2 = self.tcp.accept()
        print(f'{self.conn2}已接入服务器')

    def send1(self):
        while True:
            re = self.tcp.receive(self.conn1)
            self.tcp.send(self.conn2, re)

    def send2(self):
        while True:
            re = self.tcp.receive(self.conn2)
            self.tcp.send(self.conn1, re)

    def run(self):
        self.accept()
        t1 = threading.Thread(target=self.send1)
        t2 = threading.Thread(target=self.send2)
        t1.start()
        t2.start()

    def close(self):
        self.tcp.close()


if __name__ == '__main__':
    tcp = TCPServer()
    tcp.run()

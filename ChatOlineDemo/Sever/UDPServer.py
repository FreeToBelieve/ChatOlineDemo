"""
@author 赵国磊
@create 2019-09-07-20:55
"""
import json
import threading
import time

from ChatOlineDemo import UDP


class UDPServer(object):
    def __init__(self):
        self.udp = UDP.UDP()
        self.user_list = list() #记录登陆用户与地址

    def server_receive(self): #接收用户信息
        while True:
            re_data, addr = self.udp.upd_receive()
            data = json.loads(re_data)
            if data['state'] == 'Login':
                self.user_list.append((data['data'], addr))
            elif data['state'] == 'Quit':
                self.user_list.remove((data['data'], addr))
            elif data['state'] == 'Send':  #断定为群聊信息，将信息发给所有在线用户
                dic = {'data': data['data'], 'state': 'SendReturn'}
                send_data = json.dumps(dic)
                for i in self.user_list:
                    if not i[1] == addr:
                        self.udp.udp_send(send_data.encode('utf-8'), i[1])
            elif data['state'] == 'Apply':   #断定为私聊请求，从当前用户中匹配要私聊的用户
                name = str()
                for i in self.user_list: #从用户列表中取到发送申请要求的用户
                    if addr == i[1]:
                        name = i[0][2]
                    for j in self.user_list: #从用户列表中匹配发送对象
                        if data['data'] == j[0][2]:
                            dic = {'data': name, 'state': 'Apply'}
                            apply_data = json.dumps(dic)
                            self.udp.udp_send(apply_data.encode('utf-8'), j[1])
            elif data['state'] == 'Comfirm':
                for j in self.user_list:  # 从用户列表中匹配发送对象
                    if data['data'] == j[0][2]:
                        print(f'{j[0][2]}匹配成功')
                        dic = {'data': data['prot'], 'state': 'Comfirm'}
                        apply_data = json.dumps(dic)
                        self.udp.udp_send(apply_data.encode('utf-8'), j[1])

    def server_send(self): #向客户端发送在线用户信息
        while True:
            time.sleep(0.1)
            temp = str()
            for j in self.user_list:
                temp += j[0][2]+' '+j[1][0]+'\n'
            dic = {'data': temp, 'state': 'User'}
            data = json.dumps(dic)
            for i in self.user_list:
                self.udp.udp_send(data.encode('utf-8'), i[1])

    def sever_run(self):
        print('---服务端已启动---')
        t1 = threading.Thread(target=self.server_receive)
        t2 = threading.Thread(target=self.server_send)
        t1.start()
        t2.start()


if __name__ == '__main__':
    udps = UDPServer()
    udps.sever_run()

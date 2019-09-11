"""
@author 
@create 2019-09-09-11:03
"""
import datetime
import threading
import tkinter

from ChatOlineDemo import TCP, Conn
from ChatOlineDemo.Server import TCPServer

red = '#FFB6C1'
blue = '#00BFFF'
sql_update0 = 'update prot set state=0 where protnum=%s'


class PrivateChat(object):
    def __init__(self, addr, master=0):
        self.master = master
        self.addr = addr
        self.chat_ui = tkinter.Tk()
        self.chat_ui.title('Private Chat')
        self.chat_ui.geometry('400x600')
        if self.master:
            t = threading.Thread(target=self.tcp_conn) #利用多线程启动服务器
            t.start()
        self.tcp = TCP.TCP(self.addr, client=1) #创建客户端的TCP连接
        print('成功创建')
        self.tcp.conn()
        self.font_format = '宋体 -15'
        self.chat_text = tkinter.Text(self.chat_ui, state=tkinter.DISABLED, font=self.font_format, width=80,
                                      height=22)
        self.chat_text.tag_config("tag_1", foreground=red) #用户发送的消息tag
        self.chat_text.tag_config("tag_2", foreground=blue) #对面发送过来的消息tag
        self.user_input = tkinter.Text(self.chat_ui, width=50, height=8)
        self.btn_send = tkinter.Button(self.chat_ui, text='发送', height=2, width=4, command=self.user_send)
        self.chat_text.pack(side=tkinter.TOP)
        self.btn_send.pack(side=tkinter.BOTTOM, fill=tkinter.X, anchor=tkinter.E)
        self.user_input.pack(side=tkinter.BOTTOM, fill=tkinter.X, anchor=tkinter.W)
        self.mainloop()

    def tcp_conn(self): #创建服务器端TCP
        self.sever_tcp = TCPServer.TCPServer(self.addr)
        self.sever_tcp.run()

    def user_send(self): #用户发送信息
        user_input = self.user_input.get('1.0', tkinter.END)
        # 将发送的信息显示在text上并保持text不能修改
        self.tcp.client_send(user_input)
        self.user_input.delete('1.0', tkinter.END)
        self.chat_text.config(state=tkinter.NORMAL)
        self.chat_text.insert(tkinter.END, str(datetime.datetime.now()) + '\n' + user_input + '\n', 'tag_1')
        self.chat_text.config(state=tkinter.DISABLED)

    def user_receive(self): #用户接收从TCP发送来的信息
        while True:
            data = self.tcp.client_receive()
            chat_data = str(datetime.datetime.now()) + '\n' + data + '\n'
            self.chat_text.config(state=tkinter.NORMAL)
            self.chat_text.insert(tkinter.END, chat_data, 'tag_2')
            self.chat_text.config(state=tkinter.DISABLED)

    def mainloop(self): #主循环
        t = threading.Thread(target=self.user_receive)
        t.start()
        self.chat_ui.mainloop()
        self.tcp.close()
        if self.master:
            self.sever_tcp.close()
            del self.sever_tcp
        con = Conn.Conn()
        con.excute_sql(sql_update0, self.addr[1])
        del con

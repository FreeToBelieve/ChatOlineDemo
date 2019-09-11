import datetime
import json
import os
import threading
import time
import tkinter
from tkinter import messagebox

from ChatOlineDemo import UDP, Conn
from ChatOlineDemo.Client import PrivateChat, FileOP

sql_select = 'select * from prot where state=0 limit 1'
sql_update1 = 'update prot set state=1 where protnum=%s'
red = '#FFB6C1'
blue = '#00BFFF'


class MainInterface(object):
    def __init__(self, user):
        self.user = user
        self.font_format = '宋体 -15'
        self.btn_width = 5
        self.btn_height = 5
        self.name = str() #私聊申请的用户名
        self.main_ui = tkinter.Tk()
        self.main_ui.title('ChatOline')
        self.main_ui.geometry('400x650')
        self.frame_btn = tkinter.Frame(self.main_ui)
        self.frame_root = tkinter.Frame(self.main_ui)
        self.welcome_lable = tkinter.Label(self.main_ui, text='欢迎' + user[2], font=self.font_format)
        self.private_frame = tkinter.Frame(self.frame_root)
        self.public_frame = tkinter.Frame(self.frame_root)
        self.file_frame = tkinter.Frame(self.frame_root)
        self.welcome_lable.pack(side=tkinter.TOP)
        self.frame_btn.pack(side=tkinter.TOP)
        self.frame_root.pack(side=tkinter.TOP)
        self.private_frame.pack()
        #私聊功能界面
        self.private_lable = tkinter.Label(self.private_frame, text='在线列表', font=self.font_format)
        self.oline_list = tkinter.Label(self.private_frame, text='', font=self.font_format)
        self.private_lable.pack(side=tkinter.TOP)
        self.oline_list.pack(side=tkinter.TOP)
        self.apl_frame = tkinter.Frame(self.private_frame) #私聊申请弹窗
        self.apl_lable = tkinter.Label(self.apl_frame, text=f'{self.name}发来私聊请求', font=self.font_format)
        self.apl_btn_confirm = tkinter.Button(self.apl_frame, text='确认', width=5, height=2, command=self.apply_comfirm)
        self.apl_btn_refuse = tkinter.Button(self.apl_frame, text='拒绝', width=5, height=2, command=self.apply_refuse)
        self.apl_frame.pack(side=tkinter.TOP)
        self.apl_frame.pack_forget()
        self.apl_lable.grid(row=0, column=0, columnspan=2)
        self.apl_btn_confirm.grid(row=1, column=0)
        self.apl_btn_refuse.grid(row=1, column=1)
        self.private_apl = tkinter.Frame(self.private_frame) #用户申请私聊的frame
        self.private_apl_lable = tkinter.Label(self.private_apl, text='请输入要私聊的用户名', font=self.font_format)
        self.private_apl_entry = tkinter.Entry(self.private_apl)
        self.private_apl_btn = tkinter.Button(self.private_apl, text='发起私聊', width=8, height=2, command=self.apply)
        self.private_apl.pack(side=tkinter.TOP)
        self.private_apl.pack(side=tkinter.BOTTOM)
        self.private_apl_lable.grid(row=0, column=0, columnspan=2)
        self.private_apl_entry.grid(row=1, column=0)
        self.private_apl_btn.grid(row=1, column=1)
        #群聊功能界面
        self.public_lable = tkinter.Label(self.public_frame, text='在线用户', font=self.font_format)
        self.public_oline = tkinter.Label(self.public_frame, text='', font=self.font_format)
        self.public_lable.pack(side=tkinter.TOP)
        self.public_oline.pack(side=tkinter.TOP)
        self.chat_fram = tkinter.Frame(self.public_frame)
        self.chat_text = tkinter.Text(self.chat_fram, state=tkinter.DISABLED, font=self.font_format, width=80,
                                      height=22)
        self.chat_text.tag_config("tag_1", foreground=red)
        self.chat_text.tag_config("tag_2", foreground=blue)
        self.user_input = tkinter.Text(self.chat_fram, width=50, height=8)
        self.btn_send = tkinter.Button(self.chat_fram, text='发送', height=2, width=4, command=self.user_send)
        self.chat_fram.pack(side=tkinter.TOP)
        self.chat_text.pack(side=tkinter.TOP)
        self.btn_send.pack(side=tkinter.BOTTOM, fill=tkinter.X, anchor=tkinter.E)
        self.user_input.pack(side=tkinter.BOTTOM, fill=tkinter.X, anchor=tkinter.W)
        #文件功能界面
        self.file_btn = tkinter.Button(self.file_frame, text='上传/下载文件', width=10, height=4, command=self.goto_file)
        self.file_btn.pack()

        self.btn_private = tkinter.Button(self.frame_btn, text='私聊', height=self.btn_height,
                                          width=self.btn_width, command=self.btn_private_act)
        self.btn_public = tkinter.Button(self.frame_btn, text='群聊', height=self.btn_height,
                                         width=self.btn_width, command=self.btn_public_act)
        self.btn_file = tkinter.Button(self.frame_btn, text='文件', height=self.btn_height,
                                       width=self.btn_width, command=self.btn_file_act)
        self.btn_private.grid(row=0, column=0)
        self.btn_public.grid(row=0, column=1)
        self.btn_file.grid(row=0, column=2)
        self.mainloop()

    def btn_private_act(self):
        self.public_frame.pack_forget()
        self.file_frame.pack_forget()
        self.private_frame.pack()

    def btn_public_act(self):
        self.private_frame.pack_forget()
        self.file_frame.pack_forget()
        self.public_frame.pack()

    def btn_file_act(self):
        self.private_frame.pack_forget()
        self.public_frame.pack_forget()
        self.file_frame.pack()

    def user_receive(self): #用户接收信息
        data = json.dumps({'data': self.user, 'state': 'Login'})
        self.udp.udp_send(data.encode('utf-8'), self.udp.addr)
        while True:
            time.sleep(0.1)
            rev_data, addr = self.udp.upd_receive()
            rev_data = json.loads(rev_data.decode('utf-8'))
            if rev_data['state'] == 'User':
                user_list = rev_data['data']
                self.oline_list['text'] = user_list #动态改变用户在线列表的值
                self.public_oline['text'] = user_list #动态改变群聊用户在线列表的值
            elif rev_data['state'] == 'SendReturn': #接收用户的群聊信息
                chat_data = str(datetime.datetime.now()) + '\n' + rev_data['data'] + '\n'
                self.chat_text.config(state=tkinter.NORMAL)
                self.chat_text.insert(tkinter.END, chat_data, 'tag_2')
                self.chat_text.config(state=tkinter.DISABLED)
            elif rev_data['state'] == 'Apply': #接收私聊请求
                self.apl_frame.pack() #显示私聊弹窗
                self.name = rev_data['data']
            elif rev_data['state'] == 'Comfirm': #点击确认按钮后进行私聊
                prot = rev_data['data']
                addr = ('10.25.115.164', int(prot[0][0])) #获得TCP连接的地址与端口号
                re_p = PrivateChat.PrivateChat(addr)



    def user_send(self): #用户发送信息
        user_input = self.user_input.get('1.0', tkinter.END)
        data = {'data': user_input, 'state': 'Send'}
        data = json.dumps(data)
        #将发送的信息显示在text上并保持text不能修改
        self.udp.udp_send(data.encode('utf-8'), self.udp.addr)
        self.user_input.delete('1.0', tkinter.END)
        self.chat_text.config(state=tkinter.NORMAL)
        self.chat_text.insert(tkinter.END, str(datetime.datetime.now()) + '\n' + user_input + '\n', 'tag_1')
        self.chat_text.config(state=tkinter.DISABLED)

    def apply(self): #用户发送私聊申请
        user_input = self.private_apl_entry.get()
        data = {'data': user_input, 'state': 'Apply'}
        data = json.dumps(data)
        self.udp.udp_send(data.encode('utf-8'), self.udp.addr)

    def apply_comfirm(self):  # 申请确认按钮的回调函数
        self.private_apl_entry.delete(0, tkinter.END)
        self.apl_frame.pack_forget()
        #连接数据库得到未被占用的端口号
        con = Conn.Conn()
        prot = con.select(sql_select)
        if prot is None:
            messagebox.showinfo('提示', '端口已全部被占用')
        print(prot)
        addr = ('10.25.115.164', int(prot[0][0]))
        con.excute_sql(sql_update1, prot[0][0])
        del con
        #将端口号信息与发信用户名发给服务器端
        data = {'data': self.name, 'state': 'Comfirm', 'prot': prot}
        data = json.dumps(data)
        self.udp.udp_send(data.encode('utf-8'), self.udp.addr)
        p = PrivateChat.PrivateChat(addr, master=1)

    def apply_refuse(self):   # 申请拒绝按钮的回调函数
        self.apl_frame.pack_forget()

    def goto_file(self):
        file_op = FileOP.FileOP()

    def mainloop(self): #事件主循环
        self.udp = UDP.UDP(1)
        t1 = threading.Thread(target=self.user_receive)
        t1.start()
        self.main_ui.mainloop()
        data = json.dumps({'data': self.user, 'state': 'Quit'})
        self.udp.udp_send(data.encode('utf-8'), self.udp.addr)
        os._exit(0)


if __name__ == '__main__':
    m = MainInterface(('1', '1', '小明'))

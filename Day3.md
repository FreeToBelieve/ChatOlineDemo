Day3
===
进行项目第3天的总结与回顾<br>

今日成果
---
* 基本上完成了本项目的第二大需求：私聊功能的创建。<br>
具体上来说就是完成了TCP、TCPSever模块的构建，对MainInterface模块的功能增强与优化。<br>

实现过程
---
* 刚开始完成了TCP服务器端的基本收发功能，由于TCP连接进行私聊，发送的数据都为string类型不需要利用字典获取信息状态位（也就是说信息全为聊天信息）
TCPSever的构建较为简单。
以下位TCPSever的源码：
```python
class TCPServer(object):
    def __init__(self, addr):
        self.tcp = TCP.TCP(addr)
        self.user_list = list()
        print('---监听已开启---')

    def accept(self):
        self.conn1, self.addr1 = self.tcp.accept()
        print(f'{self.conn1}已接入服务器')
        self.conn2, self.addr2 = self.tcp.accept()
        print(f'{self.conn2}已接入服务器')
        self.user_list.append((self.conn1, self.conn2))

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
```
* 之后就是私聊窗口PrivateChat类的创建，大体思路就是将内嵌在MainInterface里的聊天界面单独拿出来再进行对TCP连接的更改与优化。
（代码就不在此处列出之后会列出修改完整版）
* 最后就是核心内容的构建，刚开始我发现当我使用TCP连接实现私聊功能的时候有一点困难，比起UDP实现的消息私发（sendto()）有一些困难，尤其是在如何实现多个用户同时进行私聊操作时。一开始的思路是将accept单独列出一个线程用以接收接入的用户，创建属性user_list（内存的元素为2个元素的元祖）存放一对用户互联信息，后来发现要为每一对接入的用户创建一个send1()与send2()，比较难以实现，于是放弃寻求其他方法。<br>
之后想用多进程的方式实现，这样每一个进程内部就能有send1()与send()2进程，但是觉得这样对系统消耗过于巨大，根本承受不了多个用户同时进行私聊。<br>
最后折中想到了一个方法：用户每一次私聊利用多线程生成一个独立的TCPServer，端口号利用数据库保存，有一个'state'位记录是否被占用。
* 同时在进行私聊设计时为了使系统更加人性化我增加了一个利用UDP私聊提示弹窗系统。
以下为弹窗系统的部分源码（该源码为MainInterface类__init__()的部分源码）：
```python
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
```
以下为按钮绑定的回调函数：
```python
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
 ```
以下为PrivateChat类的实现：
```python
class PrivateChat(object):
    def __init__(self, addr, master=0):
        self.addr = addr
        self.chat_ui = tkinter.Tk()
        self.chat_ui.title('Private Chat')
        self.chat_ui.geometry('400x600')
        if master:
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
        sever_tcp = TCPServer.TCPServer(self.addr)
        sever_tcp.run()

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
        con = Conn.Conn()
        con.excute_sql(sql_update0, self.addr[1])
        del con
 ```
 * 其它代码我就不再一一列出
 
 明日计划
 ---
 计划完成第三个主要需求：文件的上传与下载。
 

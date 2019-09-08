Day2
===
开始项目的第二天的总结<br>

需求分析
---
* 刚开始我对项目做了简单的需求分析，绘制了UML用例图与时序图，由于对于项目的细节把握不足目前还不能绘制出类图，准备在项目结束总结的时候进行绘制。
 在做需求分析时我分解了项目的架构进行梳理，鉴于昨天已经完成了三个模块，但是没有进入核心内容的编程，所以我对之后的核心模块进行了解构分析绘制了如下的UML用例图与时序图。
* UML用例图<br>
![UseCase Diagrams](https://github.com/FreeToBelieve/ChatOlineDeom/blob/master/info/用例图.jpg) 
* UML时序图<br>
![Sequence Diagrams](https://github.com/FreeToBelieve/ChatOlineDeom/blob/master/info/时序图.jpg)
群聊功能的编写
---
* 在实现群聊功能之前我先实现了显示用户列表的小功能。<br>
服务器端启动2个线程：接收和发送的线程。在用户登陆之后向服务端发送信息（dic['state']='Login'）服务器接收之后立即在用户列表中添加登陆用户信息。同时服务器端的另一个线程每隔0.1秒向客户端发送用户列表信息。<br>
以下为服务器端接收信息源码：
```python
    def server_receive(self): #接收用户信息
        while True:
            data, addr = self.udp.upd_receive()
            data = json.loads(data)
            if data['state'] == 'Login':
                self.user_list.append((data['data'], addr))
            elif data['state'] == 'Quit':
                self.user_list.remove((data['data'], addr))
            elif data['state'] == 'Send':
                dic = {'data': data['data'], 'state': 'SendReturn'}
                data = json.dumps(dic)
                for i in self.user_list:
                    if not i[1] == addr:
                        self.udp.udp_send(data.encode('utf-8'), i[1]) #断定为群聊信息，将信息发给所有在线用户
```
以下为服务器端发送在线用户信息源码：
```python
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
```
* 经过简单的测试可以实现该小功能之后我就着手开始实现第一个主要的需求：`群聊功能`<br>
其实整体的结构与思想与上一个功能类似，只不过是在Text的基础上实现。先将Text设为不可修改，然后在按下按钮调用函数时修改属性state为NORMAL
插入完之后再改为DISABLE即可。<br>
以下为用户接收信息的方法：
```python
    def user_receive(self): #用户接收信息
        data = json.dumps({'data': self.user, 'state': 'Login'})
        self.udp.udp_send(data.encode('utf-8'), self.udp.addr)
        while True:
            time.sleep(0.1)
            rev_data, addr = self.udp.upd_receive()
            rev_data = json.loads(rev_data.decode('utf-8'))
            if rev_data['state'] == 'User':
                user_list = rev_data['data']
                self.oline_list['text'] = user_list
                self.public_oline['text'] = user_list
            if rev_data['state'] == 'SendReturn':
                chat_data = str(datetime.datetime.now()) + '\n' + rev_data['data'] + '\n'
                self.chat_text.config(state=tkinter.NORMAL)
                self.chat_text.insert(tkinter.END, chat_data, 'tag_2')
                self.chat_text.config(state=tkinter.DISABLED)
```
以下为用户发送信息的方法：
```python
    def user_send(self): #用户发送信息
        user_input = self.user_input.get('1.0', tkinter.END)
        data = {'data': user_input, 'state': 'Send'}
        data = json.dumps(data)
        self.udp.udp_send(data.encode('utf-8'), self.udp.addr)
        self.user_input.delete('1.0', tkinter.END)
        self.chat_text.config(state=tkinter.NORMAL)
        self.chat_text.insert(tkinter.END, str(datetime.datetime.now()) + '\n' + user_input + '\n', 'tag_1')
        self.chat_text.config(state=tkinter.DISABLED)
```
在编码时出现的问题：<br>
---
* 刚开始写了2个线程：接收线程与主循环线程，但是在运行时发现线程之间如果要动态的修改Lable显示的文字的话要用到queqe。
于是决定将mainloop()放进主线程中。

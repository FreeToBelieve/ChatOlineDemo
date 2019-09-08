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
* 经过简单的测试可以实现该小功能之后我就着手开始实现第一个主要的需求：`群聊功能`

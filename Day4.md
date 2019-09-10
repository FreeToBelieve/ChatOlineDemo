Day4
===
项目进行的第四天总结<br>

今日成果
---
* 完成了项目的第三大需求：文件的上传与下载。<br>
该模块核心还是用TCP完成的，为此我又创建了一个一直开启的TCP服务器专门用于文件传输。<br>

实现过程
---
* 刚开始的想法是想进行文件的批量下载，但是鉴于时间可能不够，于是先完成文件的单次下载，如果时间有冗余就尝试进行批量下载功能的添加。<br>
* 实现文件上传与下载还是在传送json文件的标志位供服务器端判断执行的操作。
以下为FileTCPSever类的核心功能实现:
```python
    def run(self): #核心功能函数，执行文件的上传与下载
        while True:
            re = self.file_tcp.receive(self.conn, 9090)
            dic = json.loads(re)
            if dic['op'] == 'upload':
                with open('file/' + dic['filename'], 'w', encoding='utf-8') as f:
                    f.write(dic['content'])
                print(dic['filename'] + '接收完毕')
                self.show_file()
            elif dic['op'] == 'download':
                try:
                    with open('file/' + dic['filename'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    dic['content'] = content
                    data = json.dumps(dic)
                    self.file_tcp.send(self.conn, data)
                except Exception as e:
                    dic['op'] = 'error'
                    data = json.dumps(dic)
                    self.file_tcp.send(self.conn, data)

    def show_file(self): #向客户端发送服务器端存在的文件信息
        filename = str()
        for fpathe, dirs, fs in os.walk('./'): #利用os将file文件夹下的文件遍历
            if fpathe == './file':
                for i in fs:
                    filename += i + '\n'
        dic = {"filename": filename, "op": "show"}
        data = json.dumps(dic)
        print(data)
        self.file_tcp.send(self.conn, data)
```
* 在服务器端创建一个文件夹用以存放用户从客户端传送过来的文件，并且在用户连接TCP之后立即向用户发送文件夹内的文件信息以供用户选择下载。<br>
用户下载需要输入下载到本地文的路径以及服务器端的文件名。由于服务器端的文件信息只有在FileOP类生成时和文件上传时发送给用户，所以目前系统具有一个缺陷：如果2个用户同时创建FileOP类，在用户A上传完文件之后用户B将无法看到该文件信息。
以下为FileOP类的核心功能源码：
```python
    def receive(self): #接收服务器端发来的数据
        while True:
            re = self.tcp.client_receive(9090)
            data = json.loads(re)
            if data['op'] == 'show':
                self.file_lable['text'] = data['filename']
            elif data['op'] == 'download':
                with open(self.path + data['filename'], 'w', encoding='utf-8') as f:
                    f.write(data['content'])
                messagebox.showinfo('提示', '下载完成！')
            elif data['op'] == 'error':
                messagebox.showinfo('提示', '无此下载文件！')

    def upload_file(self): #上传文件
        dic = {'op': 'upload', 'filename': None, 'content': None}
        file_path = self.upload_entry.get()
        self.upload_entry.delete(0, tkinter.END)
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            dic['filename'], dic['content'] = file_name, content
            data = json.dumps(dic)
            self.tcp.client_send(data)
            messagebox.showinfo('提示', '文件上传成功')
        except Exception as e:
            messagebox.showinfo('提示', '无此文件！')

    def download_file(self): #向服务器发送下载请求
        dic = {'op': 'download', 'filename': None, 'content': None}
        filename = self.download_entry1.get()
        self.path = self.download_entry2.get()
        self.download_entry1.delete(0, tkinter.END)
        self.download_entry2.delete(0, tkinter.END)
        result = re.match(r'^[CDEFcdef]:\\', self.path) #利用正则表达式简单的检查用户输入本地路径格式
        if result is not None:
            dic['filename'] = filename
            data = json.dumps(dic)
            self.tcp.client_send(data)
        else:
            messagebox.showinfo('提示', '请输入正确的本地路径！')
```
明日计划
---
明天计划将会测试该系统并进行一定的性能以及功能优化。

"""
@author 赵国磊
@create 2019-09-10-11:17
"""
import json
import os
import re
import threading
import time
import tkinter
from tkinter import messagebox

from ChatOlineDemo import TCP


class FileOP(object):
    def __init__(self):
        self.font_format = '宋体 -15'
        self.tcp = TCP.TCP(('10.25.115.164', 5000), client=1)
        self.tcp.conn()   #连接客户端TCP
        self.file_ui = tkinter.Tk()
        self.path = str() #用户下载文件的本地路径
        self.file_ui.title('FileOP')
        self.file_ui.geometry('300x400')
        self.file_lable = tkinter.Label(self.file_ui, text='', font=self.font_format)
        self.file_frame = tkinter.Frame(self.file_ui)
        self.file_lable.pack(side=tkinter.TOP)
        self.file_frame.pack(side=tkinter.BOTTOM)
        self.upload_lable = tkinter.Label(self.file_frame, text='请输入要上传文件的全路径：', font=self.font_format)
        self.upload_entry = tkinter.Entry(self.file_frame)
        self.upload_btn = tkinter.Button(self.file_frame, text='上传', width=4, height=1, command=self.upload_file)
        self.upload_lable.grid(row=0, column=0, columnspan=2)
        self.upload_entry.grid(row=1, column=0)
        self.upload_btn.grid(row=1, column=1)
        self.download_lable1 = tkinter.Label(self.file_frame, text='请选择要下载的文件：', font=self.font_format)
        self.download_entry1 = tkinter.Entry(self.file_frame)
        self.download_lable2 = tkinter.Label(self.file_frame, text='请输入下载到本地的路径：', font=self.font_format)
        self.download_entry2 = tkinter.Entry(self.file_frame)
        self.download_btn = tkinter.Button(self.file_frame, text='下载', width=4, height=1, command=self.download_file)
        self.download_lable1.grid(row=2, column=0, columnspan=2)
        self.download_entry1.grid(row=3, column=0)
        self.download_lable2.grid(row=4, column=0, columnspan=2)
        self.download_entry2.grid(row=5, column=0)
        self.download_btn.grid(row=5, column=1)
        self.mainloop()

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

    def mainloop(self):
        t = threading.Thread(target=self.receive)
        t.start()
        self.file_ui.mainloop()
        self.tcp.close()


if __name__ == '__main__':
    f = FileOP()
    f.mainloop()

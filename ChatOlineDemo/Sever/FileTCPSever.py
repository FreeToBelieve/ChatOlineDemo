"""
@author 赵国磊
@create 2019-09-10-8:56
"""
import json
import os
import threading

from ChatOlineDemo import TCP


class FileTCPServer(object):
    def __init__(self):
        self.file_tcp = TCP.TCP(('10.25.115.164', 5000))
        print('---监听已开启---')

    def accept(self):
        self.conn, self.addr = self.file_tcp.accept()
        print(f'{self.conn}已接入服务器')

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

    def main(self):
        while True:
            self.accept()
            self.show_file()
            t1 = threading.Thread(target=self.run)
            t1.start()


if __name__ == '__main__':
    file_tcp = FileTCPServer()
    file_tcp.main()

import tkinter
from tkinter import messagebox


class MainInterface(object):
    def __init__(self, user):
        self.user = user
        self.font_format = '宋体 -15'
        self.btn_width = 5
        self.btn_height = 5
        self.main_ui = tkinter.Tk()
        self.main_ui.title('ChatOline')
        self.main_ui.geometry('150x400')
        self.frame_btn = tkinter.Frame(self.main_ui)
        self.frame_root = tkinter.Frame(self.main_ui)
        self.private_frame = tkinter.Frame(self.frame_root)
        self.public_frame = tkinter.Frame(self.frame_root)
        self.file_frame = tkinter.Frame(self.frame_root)
        self.frame_btn.pack(side=tkinter.TOP)
        self.frame_root.pack(side=tkinter.BOTTOM)
        self.private_frame.pack()
        self.private_lable = tkinter.Label(self.private_frame, text='在线列表', font=self.font_format)
        self.public_lable = tkinter.Label(self.public_frame, text='公共', font=self.font_format)
        self.file_lable = tkinter.Label(self.file_frame, text='文件', font=self.font_format)
        self.private_lable.pack(side=tkinter.TOP)
        self.public_lable.pack()
        self.file_lable.pack()
        self.btn_private = tkinter.Button(self.frame_btn, text='私聊', height=self.btn_height,
                                          width=self.btn_width, command=self.btn_private_act)
        self.btn_public = tkinter.Button(self.frame_btn, text='群聊', height=self.btn_height,
                                         width=self.btn_width, command=self.btn_public_act)
        self.btn_file = tkinter.Button(self.frame_btn, text='文件', height=self.btn_height,
                                       width=self.btn_width, command=self.btn_file_act)
        self.btn_private.grid(row=0, column=0)
        self.btn_public.grid(row=0, column=1)
        self.btn_file.grid(row=0, column=2)
        self.main_ui.mainloop()

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


if __name__ == '__main__':
    m = MainInterface(('1',))


import tkinter
from tkinter import messagebox
import ChatOlineDeom.Conn as Conn
import ChatOlineDeom.Client.Register as Register
from ChatOlineDeom.Client import MainInterface


class Login(object):
    def __init__(self):
        self.font_format = '宋体 -15'
        self.login_ui = tkinter.Tk()
        self.login_ui.title('Deom')
        self.login_ui.geometry('300x200')
        self.lable_user = tkinter.Label(self.login_ui, text='请输入用户名：', font=self.font_format)
        self.lable_password = tkinter.Label(self.login_ui, text='请输入密码：', font=self.font_format)
        self.entry_user = tkinter.Entry(self.login_ui)
        self.entry_password = tkinter.Entry(self.login_ui, show='*')
        self.btn_login = tkinter.Button(self.login_ui, text='登陆', height=2, width=4,
                                   command=self.login_check)
        self.btn_register = tkinter.Button(self.login_ui, text='注册', height=2, width=4,
                                           command=self.register)
        self.lable_user.grid(row=1, column=0)
        self.lable_password.grid(row=2, column=0)
        self.entry_user.grid(row=1, column=1, columnspan=2)
        self.entry_password.grid(row=2, column=1, columnspan=2)
        self.btn_login.grid(row=3, column=0)
        self.btn_register.grid(row=3, column=2)
        self.login_ui.mainloop()

    def register(self): #用户注册
        self.login_ui.destroy()
        r = Register.Register()

    def login_check(self):  # 登陆检验
        sql = 'select * from user_base where usernum = %s'
        user_num = self.entry_user.get()
        try:
            con = Conn.Conn()
            user = con.select(sql, user_num)[0]
            user_psw = user[3]
            password = self.entry_password.get()
            if user_psw == password:
                messagebox.showinfo('提示', '登陆成功！')
                m = MainInterface.MainInterface(user)
            else:
                messagebox.showinfo('提示', '密码错误，登陆失败！')
        except Exception as e:
            print(e)
            messagebox.showinfo('提示', '无此用户，请检查账号！')
        finally:
            del con


if __name__ == '__main__':
    l = Login()

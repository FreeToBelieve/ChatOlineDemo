
import tkinter
from tkinter import messagebox
import ChatOlineDeom.Conn as Conn
import ChatOlineDeom.Register as Register
font_format = '宋体 -15'


def login_check(entry_user, entry_password): #登陆检验
    sql = 'select * from user_base where usernum = %s'
    user_num = entry_user.get()
    try:
        con = Conn.Conn()
        user_psw = con.select(sql, user_num)[0][3]
        password = entry_password.get()
        if user_psw == password:
            messagebox.showinfo('提示', '登陆成功！')
        else:
            messagebox.showinfo('提示', '密码错误，登陆失败！')
    except Exception as e:
        print(e)
        messagebox.showinfo('提示', '无此用户，请检查账号！')
    finally:
        del con


def register(login_ui): #用户注册
    login_ui.destroy()
    Register.Register()


def Login():
    login_ui = tkinter.Tk()
    login_ui.title('Deom')
    login_ui.geometry('300x200')
    lable_user = tkinter.Label(login_ui, text='请输入用户名：', font=font_format)
    lable_password = tkinter.Label(login_ui, text='请输入密码：', font=font_format)
    entry_user = tkinter.Entry(login_ui)
    entry_password = tkinter.Entry(login_ui, show='*')
    btn_login = tkinter.Button(login_ui, text='登陆', height=2, width=4, command=lambda: login_check(entry_user, entry_password))
    btn_register = tkinter.Button(login_ui, text='注册', height=2, width=4, command=lambda: register(login_ui))
    lable_user.grid(row=1, column=0)
    lable_password.grid(row=2, column=0)
    entry_user.grid(row=1, column=1, columnspan=2)
    entry_password.grid(row=2, column=1, columnspan=2)
    btn_login.grid(row=3, column=0)
    btn_register.grid(row=3, column=2)
    tkinter.mainloop()


if __name__ == '__main__':
    Login()

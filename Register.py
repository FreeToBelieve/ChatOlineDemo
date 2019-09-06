import tkinter
from tkinter import messagebox
import ChatOlineDeom.Login as Login
import ChatOlineDeom.Conn as Conn
import re
font_format = '宋体 -15'


def register_check(register_ui, entry_num, entry_name, entry_password, entry_cofirm_password):
    if not entry_password.get() == entry_cofirm_password.get():
        messagebox.showinfo('提示', '2次输入的密码不相等请重新确认！')
        register_ui.destroy()
        Register()
    elif not check_num(entry_num):
        messagebox.showinfo('提示', '用户名未按照格式输入！')
        register_ui.destroy()
        Register()
    else:
        try:
            sql = 'insert into user_base(usernum,username,userpsw) values(%s,%s,%s)'
            con = Conn.Conn()
            con.excute_sql(sql, entry_num.get(), entry_name.get(), entry_password.get())
        except Exception as e:
            print(e)
            messagebox.showinfo('提示', '注册失败！')
        else:
            messagebox.showinfo('提示', '注册成功！')
            register_ui.destroy()
            Login.Login()
        finally:
            del con


def return_top(register_ui):
    register_ui.destroy()
    Login.Login()


def check_num(entry_num):
    num = entry_num.get()
    if 6 <= len(num) <= 9:
        result = re.match(r'\w+', num)
        if result:
            return True if len(result.group()) == len(num) else False
        else:
            return False
    else:
        return False


def Register():
    register_ui = tkinter.Tk()
    register_ui.title('注册')
    register_ui.geometry('400x300')
    lable_num1 = tkinter.Label(register_ui, text='请输入账号：', font=font_format)
    lable_num2 = tkinter.Label(register_ui, text='(6-9位数字字母下划线组合)', font=font_format)
    lable_name = tkinter.Label(register_ui, text='请输入用户名：', font=font_format)
    lable_password = tkinter.Label(register_ui, text='请输入密码：', font=font_format)
    lable_cofirm_password = tkinter.Label(register_ui, text='请再次输入密码：', font=font_format)
    entry_num = tkinter.Entry(register_ui)
    entry_name = tkinter.Entry(register_ui)
    entry_password = tkinter.Entry(register_ui, show='*')
    entry_cofirm_password = tkinter.Entry(register_ui, show='*')
    btn_register = tkinter.Button(register_ui, text='注册', height=2, width=4, command=lambda: register_check(register_ui, entry_num, entry_name, entry_password, entry_cofirm_password))
    btn_return = tkinter.Button(register_ui, text='返回', height=2, width=4, command=lambda: return_top(register_ui))
    lable_num1.grid(row=1, column=0)
    lable_num2.grid(row=2, column=0)
    lable_name.grid(row=3, column=0)
    lable_password.grid(row=4, column=0)
    lable_cofirm_password.grid(row=5, column=0)
    entry_num.grid(row=1, column=1, columnspan=2)
    entry_name.grid(row=3, column=1, columnspan=2)
    entry_password.grid(row=4, column=1, columnspan=2)
    entry_cofirm_password.grid(row=5, column=1, columnspan=2)
    btn_register.grid(row=6, column=0)
    btn_return.grid(row=6, column=2)
    tkinter.mainloop()


if __name__ == '__main__':
    Register()
import tkinter
from tkinter import messagebox
import ChatOlineDeom.Login as Login
import ChatOlineDeom.Conn as Conn
import re


class Register(object):
    def __init__(self):
        self.font_format = '宋体 -15'
        self.register_ui = tkinter.Tk()
        self.register_ui.title('注册')
        self.register_ui.geometry('400x300')
        self.lable_num1 = tkinter.Label(self.register_ui, text='请输入账号：', font=self.font_format)
        self.lable_num2 = tkinter.Label(self.register_ui, text='(6-9位数字字母下划线组合)', font=self.font_format)
        self.lable_name = tkinter.Label(self.register_ui, text='请输入用户名：', font=self.font_format)
        self.lable_password = tkinter.Label(self.register_ui, text='请输入密码：', font=self.font_format)
        self.lable_cofirm_password = tkinter.Label(self.register_ui, text='请再次输入密码：', font=self.font_format)
        self.entry_num = tkinter.Entry(self.register_ui)
        self.entry_name = tkinter.Entry(self.register_ui)
        self.entry_password = tkinter.Entry(self.register_ui, show='*')
        self.entry_cofirm_password = tkinter.Entry(self.register_ui, show='*')
        self.btn_register = tkinter.Button(self.register_ui, text='注册', height=2, width=4, command=self.register_check)
        self.btn_return = tkinter.Button(self.register_ui, text='返回', height=2, width=4, command=self.return_top)
        self.lable_num1.grid(row=1, column=0)
        self.lable_num2.grid(row=2, column=0)
        self.lable_name.grid(row=3, column=0)
        self.lable_password.grid(row=4, column=0)
        self.lable_cofirm_password.grid(row=5, column=0)
        self.entry_num.grid(row=1, column=1, columnspan=2)
        self.entry_name.grid(row=3, column=1, columnspan=2)
        self.entry_password.grid(row=4, column=1, columnspan=2)
        self.entry_cofirm_password.grid(row=5, column=1, columnspan=2)
        self.btn_register.grid(row=6, column=0)
        self.btn_return.grid(row=6, column=2)
        self.register_ui.mainloop()

    def check_num(self):  # 以正则表达式的方式校验用户名格式，如果错误返回False
        num = self.entry_num.get()
        if 6 <= len(num) <= 9:
            result = re.match(r'\w+', num)
            if result:
                return True if len(result.group()) == len(num) else False
            else:
                return False
        else:
            return False

    def return_top(self):  # 返回登陆界面
        self.register_ui.destroy()
        l = Login.Login()

    def register_check(self):  # 注册校验：包括2次密码输入校验、用户名格式校验
        if not self.entry_password.get() == self.entry_cofirm_password.get():
            messagebox.showinfo('提示', '2次输入的密码不相等请重新确认！')
            self.register_ui.destroy()
            Register()
        elif not self.check_num():
            messagebox.showinfo('提示', '用户名未按照格式输入！')
            self.register_ui.destroy()
            Register()
        else:
            try:
                sql = 'insert into user_base(usernum,username,userpsw) values(%s,%s,%s)'
                con = Conn.Conn()
                con.excute_sql(sql, self.entry_num.get(), self.entry_name.get(), self.entry_password.get())
            except Exception as e:
                print(e)
                messagebox.showinfo('提示', '注册失败！')
            else:
                messagebox.showinfo('提示', '注册成功！')
                self.register_ui.destroy()
                Login.Login()
            finally:
                del con


if __name__ == '__main__':
    r = Register()

from pymysql import *


class Conn(object):
    def __init__(self):
        self.conn = connect(host='localhost', port=3306, database='chatoline', user='root', password='root')
        self.cur = self.conn.cursor()
        print('连接已开启')

    def __del__(self):
        self.cur.close()
        self.conn.close()
        print('连接已关闭')

    def select(self, sql, *args):
        self.cur.execute(sql, args)
        return self.cur.fetchall()

    def excute_sql(self, sql, *args):
        self.cur.execute(sql, args)
        self.conn.commit()


if __name__ == '__main__':
    c = Conn()
    sql = 'select * from user_base where usernum = 123456789'
    print(c.select(sql))
    del c
import time
import threading
import string
import pymysql

DB_IP = '10.18.2.114'
DB_PORT = 3306
DB_USER = "root"
DB_PWD = "CqkWnd46FV1tDgBZ5RKMkD"
DB_NAME_REPORT = 'ES_REPORT'



class DB_REPORT(object):
    def __init__(self):
        self.file = 0
        self.mysql = ''
        self.num = 0

    def init(self):
        self.mysql = pymysql.connect(
            host=DB_IP,  # 连接地址, 本地
            user=DB_USER,  # 用户
            password=DB_PWD,  # 数据库密码,记得修改为自己本机的密码
            port=DB_PORT,  # 端口,默认为3306
            charset='utf8',  # 编码
            database=DB_NAME_REPORT  # 选择数据库
        )
    def insert(self, index, main_imsi, token, main_msisdn, create_at, update_at):
        db = self.mysql.cursor()
        # data='VALUES'+"("+str(index)+","+str(main_imsi)+","+"'"+str(token)+"'"+","+str(main_msisdn)+","+"'"+create_at+"'"+","+"'"+update_at+"'"+")"
        # append = 'INSERT INTO account_auth'
        append = 'INSERT INTO account_auth VALUES'+"("+str(index)+","+str(main_imsi)+","+"'"+str(token)+"'"+","+str(main_msisdn)+","+"'"+create_at+"'"+","+"'"+update_at+"'"+")"

        # print(append)
        try:
            # db.executemany(append, data)
            db.execute(append)
        except Exception as e:
            print('操作失败', e)
            # self.mysql.rollback()  # 表示不成功则回滚数据
        # self.num = self.num + 1
        # if (self.num % 1000 == 0):
        #     self.mysql.commit()
        # try:
            # 执行sql
            # db.execute('show databases;')
            # 添加
            # db.execute(append)
            # self.mysql.commit()  # 表示将修改操作提交到数据库
            # print('创建表成功')
            # print('添加成功')

        # except Exception as e:
        #     print('操作失败', e)
        #     self.mysql.rollback()  # 表示不成功则回滚数据

        # 游标关闭
        # db.close()
        def insert(self, index, main_imsi, token, main_msisdn, create_at, update_at):
            db = self.mysql.cursor()
            # data='VALUES'+"("+str(index)+","+str(main_imsi)+","+"'"+str(token)+"'"+","+str(main_msisdn)+","+"'"+create_at+"'"+","+"'"+update_at+"'"+")"
            # append = 'INSERT INTO account_auth'
            append = 'INSERT INTO account_auth VALUES' + "(" + str(index) + "," + str(main_imsi) + "," + "'" + str(
                token) + "'" + "," + str(main_msisdn) + "," + "'" + create_at + "'" + "," + "'" + update_at + "'" + ")"

            # print(append)
            try:
                # db.executemany(append, data)
                db.execute(append)
            except Exception as e:
                print('操作失败', e)
                # self.mysql.rollback()  # 表示不成功则回滚数据
            # self.num = self.num + 1
            # if (self.num % 1000 == 0):
            #     self.mysql.commit()
            # try:
            # 执行sql
            # db.execute('show databases;')
            # 添加
            # db.execute(append)
            # self.mysql.commit()  # 表示将修改操作提交到数据库
            # print('创建表成功')
            # print('添加成功')

            # except Exception as e:
            #     print('操作失败', e)
            #     self.mysql.rollback()  # 表示不成功则回滚数据

            # 游标关闭
            # db.close()
    def insert_new(self, append):
        db = self.mysql.cursor()
        # data='VALUES'+"("+str(index)+","+str(main_imsi)+","+"'"+str(token)+"'"+","+str(main_msisdn)+","+"'"+create_at+"'"+","+"'"+update_at+"'"+")"
        # append = 'INSERT INTO account_auth'
        # append = 'INSERT INTO account_auth VALUES'+"("+str(index)+","+str(main_imsi)+","+"'"+str(token)+"'"+","+str(main_msisdn)+","+"'"+create_at+"'"+","+"'"+update_at+"'"+")"

        # print(append)
        try:
            # db.executemany(append, data)
            db.execute(append)
        except Exception as e:
            print('操作失败', e)

    def insert_new_data(self, append, data):
        db = self.mysql.cursor()
        # data='VALUES'+"("+str(index)+","+str(main_imsi)+","+"'"+str(token)+"'"+","+str(main_msisdn)+","+"'"+create_at+"'"+","+"'"+update_at+"'"+")"
        # append = 'INSERT INTO account_auth'
        # append = 'INSERT INTO account_auth VALUES'+"("+str(index)+","+str(main_imsi)+","+"'"+str(token)+"'"+","+str(main_msisdn)+","+"'"+create_at+"'"+","+"'"+update_at+"'"+")"

        # print(append)
        try:
            db.executemany(append, data)
            # db.execute(append)
        except Exception as e:
            print('操作失败', e)

    def commit(self):
        self.mysql.commit()

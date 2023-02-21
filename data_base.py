import time
import threading
import string
import pymysql

DB_IP = '10.10.0.4'
DB_PORT = 3306
DB_USER = "root"
DB_PWD = "PxX5ksKU801vOYBYj2CVsU1fP3"
DB_NAME_BIZ = 'ES_BIZ'
DB_NAME_BSS = 'ES_BSS_MANAGER_DB'



class DB_BIZ(object):
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
            database=DB_NAME_BIZ  # 选择数据库
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

class DB_BSS(object):
    def __init__(self):
        self.file = 0
        self.mysql = ''

    def init(self):
        self.mysql = pymysql.connect(
            host=DB_IP,  # 连接地址, 本地
            user=DB_USER,  # 用户
            password=DB_PWD,  # 数据库密码,记得修改为自己本机的密码
            port=DB_PORT,  # 端口,默认为3306
            charset='utf8',  # 编码
            database=DB_NAME_BSS  # 选择数据库
        )

    def insert(self, id, primary_msisdn, alt_smdp_fqdn, msisdn, iccid, imei, eid, activation_status, date_time, display_name, type, batch_update_code, update_at, create_at):
        db = self.mysql.cursor()
        # data = 'VALUES'+"("+str(id)+","+str(primary_msisdn)+","+"'"+str(alt_smdp_fqdn)+"'"+\
        #          ","+str(msisdn)+","+str(iccid)+","+str(imei)+","+str(eid)+","+"'"+str(activation_status)+"'"+","+str(date_time)+\
        #          ","+"'"+str(display_name)+"'"+","+str(type)+","+"'"+str(batch_update_code)+"'"+","+"'"+str(update_at)+"'"+","+"'"+str(create_at)+"'"+")"
        #
        # append = 'INSERT INTO bss_snmd_as_profile'
        append = 'INSERT INTO bss_snmd_as_profile VALUES'+"("+str(id)+","+str(primary_msisdn)+","+"'"+str(alt_smdp_fqdn)+"'"+\
                 ","+str(msisdn)+","+str(iccid)+","+str(imei)+","+str(eid)+","+"'"+str(activation_status)+"'"+","+str(date_time)+\
                 ","+"'"+str(display_name)+"'"+","+str(type)+","+"'"+str(batch_update_code)+"'"+","+"'"+str(update_at)+"'"+","+"'"+str(create_at)+"'"+")"
        # print(append)
        try:
            # # 执行sql
            # db.execute(self.mysql)
            # 添加
            db.execute(append)
            # db.executemany(append, data)
            # self.mysql.commit()  # 表示将修改操作提交到数据库
            # print('创建表成功')
            # print('添加成功')

        except Exception as e:
            print('操作失败', e)
            self.mysql.rollback()  # 表示不成功则回滚数据

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

    def insert_new_data(self, append,data):
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
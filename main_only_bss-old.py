# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from isim import Isim
from file_csv import File_csv
from data_base import DB_BIZ
from data_base import DB_BSS
from redis_DB import Db_myRedis
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


ES_TEST_TIME = 100000
ES_TEST_MAX_ITEM = 5000

# FLAG_MAIN = 1
# FLAG_SECD = 2
FILE_CSV_PREFIX = "/Users/redtea/Desktop/account-quth"
FILE_CSV_SUFFIX = ".csv"
FILE_token_expire = "/Users/redtea/Desktop/token_expire.csv"
i_flag=1000


def process(i):
    print("并发函数 %s 开始：", i)
    FLAG_MAIN = i+100000000
    FLAG_SECD = i+200000000
    isim = Isim()
    file_csv = File_csv()
    mysql_BIZ = DB_BIZ()
    mysql_BSS = DB_BSS()
    myredis = Db_myRedis()
    file_csv_num = 1
    mysql_BIZ.init()
    mysql_BSS.init()
    myredis.init()
    userValues_BIZ = []
    userValues_BSS = []
    alt_smdp_fqdn = "LPA:1$esim.yhdzd.chinamobile.com:8002$"
    date_time = "20220826163508"
    create_at = time.strftime('%Y-%m-%d %H:%M:%S')
    update_at = time.strftime('%Y-%m-%d %H:%M:%S')
    activation_status = 'Active'
    type = 1
    batch_update_code = 'A_220708182148_moa1g'
    sql_BIZ = 'INSERT INTO account_auth VALUES '
    sql_BSS = 'insert into bss_snmd_as_profile values '

    csvValue = []
    # sql_BIZ_1 = "INSERT INTO account_auth VALUE (%s,%s,%s,%s,%s,%s)"
    # sql_BSS_1 = "INSERT INTO bss_snmd_as_profile VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    # sql_BIZ_1 = "INSERT INTO account_auth(imsi, token, msisdn, create_at, update_at) VALUE (%s,%s,%s,%s,%s)"
    sql_BSS_1 = "INSERT INTO bss_snmd_as_profile(primary_msisdn, alt_smdp_fqdn, msisdn, iccid, imei, eid, activation_status, " \
                "date_time, display_name, type, batch_update_code, update_at, create_at) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    # time_start = time.time()
    # print("start time: ", time.strftime('%Y-%m-%d %H:%M:%S'))
    # if i <= 20000 or i >= 9980001:
    #     file_name = FILE_CSV_PREFIX + str(i) + FILE_CSV_SUFFIX
    #     print(i, "open file: ", file_name)
    #     file_csv.open(file_name)
    for i in range(i, i+i_flag):
        index = i
        token = isim.get_token()
        imsi_main = isim.get_imsi(FLAG_MAIN)
        imsi_secd = isim.get_imsi(FLAG_SECD)
        subscribe = isim.get_subs(imsi_main)
        msisdn_main = isim.get_msisdn(FLAG_MAIN)
        msisdn_second = isim.get_msisdn(FLAG_SECD)
        iccid_main = isim.get_iccid(FLAG_MAIN)
        iccid_secd = isim.get_iccid(FLAG_SECD)
        # imei = isim.get_imei()
        imei = isim.get_imei_id()
        eid = isim.get_eid()
        ##前20000条用来测试token 有效，后20000测试token无效
        # if i<=20000 or i>=9980001:
        #     file_csv.write(index, subscribe,
        #                        imsi_main, msisdn_main,iccid_main,
        #                        imsi_secd, iccid_secd,
        #                        imei, eid,
        #                        token)
        # file_csv_num = file_csv_num + 1

        # userValues_BIZ.append(
        #     (str(index), str(imsi_main), str(token), str(msisdn_main), str(create_at), str(update_at)))
        # userValues_BSS.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second), str(iccid_secd),
        #                        str(imei), str(eid), str(activation_status), str(date_time), str(index), str(type),
        #                        str(batch_update_code), str(update_at), str(create_at)))
        ###最后20000条不写token
        # if i <= 9980001:
        #     userValues_BIZ.append(
        #     (str(imsi_main), str(token), str(msisdn_main), str(create_at), str(update_at)))
        userValues_BSS.append((str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second), str(iccid_secd),
                               str(imei), str(eid), str(activation_status), str(date_time), str(index), str(type),
                               str(batch_update_code), str(update_at), str(create_at)))

        # if i % 2000 == 0:
        #     # print(sql_BIZ_1,userValues_BIZ)
        #     print("i 时间: ", i, time.strftime('%Y-%m-%d %H:%M:%S'))
        #     mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
        #     mysql_BSS.insert_new_data(sql_BSS_1, userValues_BSS)
        #     userValues_BIZ = []
        #     userValues_BSS = []
        #     print("i 结束: ", i, time.strftime('%Y-%m-%d %H:%M:%S'))

        # 最后20000条数据，不会写入redis，构造token过期的数据
        # if i<=9980001:
        #     myredis.insert(imsi_main, token, msisdn_main)
    # print(sql_BIZ_1,userValues_BIZ)
    print("第 %s 数据库插入开始: ", i, time.strftime('%Y-%m-%d %H:%M:%S'))
    # mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
    mysql_BSS.insert_new_data(sql_BSS_1, userValues_BSS)
    userValues_BIZ = []
    userValues_BSS = []
    # mysql_BIZ.commit()
    mysql_BSS.commit()
    print("第 %s 数据库插入结束: ", i, time.strftime('%Y-%m-%d %H:%M:%S'))
    # myredis.commit()
    # time_end = time.time()
    # print("finish time: ", time.strftime('%Y-%m-%d %H:%M:%S'))
    # print("cost time: ", time_end - time_start)


if __name__ == '__main__':
    time_start = time.time()
    print("start time: ",  time.strftime('%Y-%m-%d %H:%M:%S'))

    for j in range(1, 10000001, 10000):
    # for j in range(9990001, 10000001, 10000):
        ####1000条数据，执行一次SQL，并发10次。
        items = [j, j+1000, j+2000, j+3000, j+4000, j+5000, j+6000, j+7000, j+8000, j+9000]
        pool = ThreadPool()
        pool.map(process, items)
        pool.close()
        j += 10000
        # print(j, "=j")
    time_end = time.time()
    print("finish time: ",  time.strftime('%Y-%m-%d %H:%M:%S'))
    print("cost time: ",  time_end - time_start)
    # isim = Isim()
    # file_csv = File_csv()
    # mysql_BIZ = DB_BIZ()
    # mysql_BSS = DB_BSS()
    # myredis = Db_myRedis()
    # file_csv_num = 1
    # mysql_BIZ.init()
    # mysql_BSS.init()
    # myredis.init()
    #
    # time_start = time.time()
    # print("start time: ", time.strftime('%Y-%m-%d %H:%M:%S'))
    #
    # for i in range(1, ES_TEST_TIME+1):
    #     index = i
    #     token = isim.get_token()
    #     imsi_main = isim.get_imsi(FLAG_MAIN)
    #     imsi_secd = isim.get_imsi(FLAG_SECD)
    #     subscribe = isim.get_subs(imsi_main)
    #     msisdn_main = isim.get_msisdn(FLAG_MAIN)
    #     msisdn_second = isim.get_msisdn(FLAG_SECD)
    #     iccid_main = isim.get_iccid(FLAG_MAIN)
    #     iccid_secd = isim.get_iccid(FLAG_SECD)
    #     #imei = isim.get_imei()
    #     imei = isim.get_imei_id()
    #     eid = isim.get_eid()
    #
    #     userValues_BIZ.append((str(index), str(imsi_main), str(token), str(msisdn_main), str(create_at), str(update_at)))
    #     userValues_BSS.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second), str(iccid_secd), str(imei), str(eid), str(activation_status), str(date_time), str(index), str(type), str(batch_update_code), str(update_at), str(create_at)))
    #
    #     if i % 2000 == 0:
    #             # print(sql_BIZ_1,userValues_BIZ)
    #         print("i 时间: ", i, time.strftime('%Y-%m-%d %H:%M:%S'))
    #         mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
    #         mysql_BSS.insert_new_data(sql_BSS_1, userValues_BSS)
    #         userValues_BIZ = []
    #         userValues_BSS = []
    #         print("i 结束: ", i, time.strftime('%Y-%m-%d %H:%M:%S'))
    #
    #     #最后10000条数据，不会写入redis，构造token过期的数据
    #     myredis.insert(imsi_main, token, msisdn_main)
    #
    # mysql_BIZ.commit()
    # mysql_BSS.commit()
    # # myredis.commit()
    # time_end = time.time()
    # print("finish time: ", time.strftime('%Y-%m-%d %H:%M:%S'))
    # print("cost time: ", time_end - time_start)

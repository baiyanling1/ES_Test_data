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

# #数据总条数
# ES_TEST_TIME = 100000
#
# #一个文件最大5000条数据
# ES_TEST_MAX_ITEM = 5000

ES_TEST_TIME = 5
ES_TEST_MAX_ITEM = 1

FLAG_MAIN = 1
FLAG_SECD = 2
FILE_CSV_PREFIX = "/Users/hejian/Desktop/2024移动ES性能测试数据/token-expire/account-auth-token-expire"
FILE_CSV_SUFFIX = ".csv"
FILE_token_expire = "/Users/hejian/Desktoptoken_expire.csv"

alt_smdp_fqdn = "LPA:1$esim.yhdzd.chinamobile.com:8002$"
date_time = "20220826163508"
create_at = time.strftime('%Y-%m-%d %H:%M:%S')
update_at = time.strftime('%Y-%m-%d %H:%M:%S')
activation_status = 'Active'
type = 1
batch_update_code = 'A_220708182148_moa1g'
sql_BIZ = 'INSERT INTO account_auth VALUES '
sql_BSS = 'insert into bss_snmd_as_profile values '
userValues_BIZ = []
userValues_BSS = []
csvValue=[]
sql_BIZ_1 = "INSERT INTO account_auth VALUE (%s,%s,%s,%s,%s,%s,%s)"
sql_BSS_1 = "INSERT INTO bss_snmd_as_profile VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
if __name__ == '__main__':

    isim = Isim()
    file_csv = File_csv()
    mysql_BIZ = DB_BIZ()
    mysql_BSS = DB_BSS()
    # myredis = Db_myRedis()
    file_csv_num = 1
    mysql_BIZ.init()
    mysql_BSS.init()
    # myredis.init()

    time_start = time.time()
    print("start time: ", time_start)
    # file_name = FILE_CSV_PREFIX + str(file_csv_num) + FILE_CSV_SUFFIX
    # file_csv.open(file_name)
    for i in range(1, ES_TEST_TIME+1):
        if (i - 1) % ES_TEST_MAX_ITEM == 0:
            file_csv.write_all(csvValue)
            mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
            mysql_BSS.insert_new_data(sql_BSS_1, userValues_BSS)
            file_name = FILE_CSV_PREFIX + str(file_csv_num) + FILE_CSV_SUFFIX
            print(i, "open file: ", file_name)
            file_csv.open(file_name)
            file_csv_num = file_csv_num + 1
            userValues_BIZ = []
            userValues_BSS = []
            csvValue = []

        index = 15000000 + i
        token = isim.get_token()
        imsi_main = isim.get_imsi(FLAG_MAIN)
        imsi_secd = isim.get_imsi(FLAG_SECD)
        subscribe = isim.get_subs(imsi_main)
        msisdn_main = isim.get_msisdn(FLAG_MAIN)
        msisdn_second = isim.get_msisdn(FLAG_SECD)
        iccid_main = isim.get_iccid(FLAG_MAIN)
        iccid_secd = isim.get_iccid(FLAG_SECD)
        #imei = isim.get_imei()
        device_type = 1
        imei = isim.get_imei_id()
        eid = isim.get_eid()

        # file_csv.write(index, subscribe, imsi_main, msisdn_main, iccid_main, imsi_secd,
        #                iccid_secd, imei, eid, msisdn_second, token)

        csvValue.append((index, subscribe,
                         imsi_main, msisdn_main, iccid_main,
                         imsi_secd, iccid_secd,
                         imei, eid,
                         token))


        # file_csv.write_all(csvValue)
        # print(index, subscribe, imsi_main, msisdn_main, imsi_secd, iccid_secd, imei, eid, token)

        # file_csv.write(index, subscribe,
        #                imsi_main, msisdn_main,
        #                imsi_secd, iccid_secd,
        #                imei, eid,
        #                token)
        ##########
        # if i <= 30000:
        #     csvValue.append((index, subscribe,
        #                    imsi_main, msisdn_main, iccid_main,
        #                    imsi_secd, iccid_secd,
        #                    imei, eid,
        #                    token))
        userValues_BIZ.append((str(index), str(imsi_main), str(token), str(msisdn_main), str(device_type),  str(create_at), str(update_at)))
        userValues_BSS.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second), str(iccid_secd), str(imei), str(eid), str(activation_status), str(date_time), str(index), str(type), str(batch_update_code), str(update_at), str(create_at)))
        # 最后一次文件写入和sql执行
        if i == ES_TEST_TIME:
            file_csv.write_all(csvValue)
            mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
            mysql_BSS.insert_new_data(sql_BSS_1, userValues_BSS)
        # print("开始", i)
        # mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
        # mysql_BSS.insert_new_data(sql_BSS_1, userValues_BSS)
        # if i<= 90000:
        #     if i % 5000 == 0:
        #         # print(sql_BIZ_1,userValues_BIZ)
        #         print("开始", i)
        #         mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
        #         mysql_BSS.insert_new_data(sql_BSS_1, userValues_BSS)
        #         if i <=30000:
        #             file_csv.write_all(csvValue)
        #         userValues_BIZ = []
        #         userValues_BSS = []
        #         csvValue = []
        #         print("结束", i)

        ##########
        ###################
        # if i % 5000 != 0:
        #     sql_BIZ += "("+str(index)+","+str(imsi_main)+","+"'"+str(token)+"'"+","+str(msisdn_main)+","+"'"+create_at+"'"+","+"'"+update_at+"'"+")"+','
        #     sql_BSS += "("+str(index)+","+str(msisdn_main)+","+"'"+str(alt_smdp_fqdn)+"'"+\
        #              ","+str(msisdn_second)+","+str(iccid_secd)+","+str(imei)+","+str(eid)+","+"'"+str(activation_status)+"'"+","+str(date_time)+\
        #              ","+"'"+str(index)+"'"+","+str(type)+","+"'"+str(batch_update_code)+"'"+","+"'"+str(update_at)+"'"+","+"'"+str(create_at)+"'"+")"+','
        #
        # if i % 5000 == 0:
        #     sql_BIZ += "(" + str(index) + "," + str(imsi_main) + "," + "'" + str(token) + "'" + "," + str(
        #         msisdn_main) + "," + "'" + create_at + "'" + "," + "'" + update_at + "'" + ")"
        #     sql_BSS += "(" + str(index) + "," + str(msisdn_main) + "," + "'" + str(alt_smdp_fqdn) + "'" + \
        #                "," + str(msisdn_second) + "," + str(iccid_secd) + "," + str(imei) + "," + str(
        #         eid) + "," + "'" + str(activation_status) + "'" + "," + str(date_time) + \
        #                "," + "'" + str(index) + "'" + "," + str(type) + "," + "'" + str(
        #         batch_update_code) + "'" + "," + "'" + str(update_at) + "'" + "," + "'" + str(
        #         create_at) + "'" + ")"
        #
        #     mysql_BIZ.insert_new(sql_BIZ)
        #     mysql_BSS.insert_new(sql_BSS)
        #     sql_BIZ = 'INSERT INTO account_auth VALUES '
        #     sql_BSS = 'insert into bss_snmd_as_profile values '
#######################################
            # mysql_BIZ.insert(index, imsi_main, token, msisdn_main, create_at, update_at)
            # ES_BSS_MANAGER_DB数据库中bss_snmd_as_profile添加数据
            # mysql_BSS.insert(index, msisdn_main, alt_smdp_fqdn, msisdn_second, iccid_secd, imei,
            #                  eid, activation_status, date_time, index, type, batch_update_code, create_at, update_at)
        #BIZ数据库中account_auth添加数据
        # mysql_BIZ.insert(index, imsi_main, token, msisdn_main, create_at, update_at)
        # #ES_BSS_MANAGER_DB数据库中bss_snmd_as_profile添加数据
        # mysql_BSS.insert(index, msisdn_main, alt_smdp_fqdn, msisdn_second, iccid_secd, imei,
        #                  eid, activation_status, date_time, index, type, batch_update_code, create_at, update_at)

        #最后10000条数据，不会写入redis，构造token过期的数据
        # if i<=90000:
        #    myredis.insert(imsi_main, token, msisdn_main)
        # #最后10000条数据token过期，构造token过期的数据
        # if i>90000:
        #     file_csv.open(FILE_token_expire)
        #     file_csv.write(index, subscribe,
        #                                   imsi_main, msisdn_main, iccid_main,
        #                                   imsi_secd, iccid_secd,
        #                                   imei, eid,
        #                                   token)



    mysql_BIZ.commit()
    mysql_BSS.commit()
    # myredis.commit()
    time_end = time.time()
    print("finish time: ", time_end)
    print("cost time: ", time_end - time_start)

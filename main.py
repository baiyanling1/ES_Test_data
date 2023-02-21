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
import os
import io


ES_TEST_TIME = 10000
ES_TEST_MAX_ITEM = 10000

FLAG_MAIN = 1
FLAG_SECD = 2
FILE_CSV_PREFIX = "/Users/redtea/Desktop/account-quth"
FILE_CSV_SUFFIX = ".csv"

alt_smdp_fqdn = "LPA:1$esim.yhdzd.chinamobile.com:8002$"
date_time = "20220826163508"
create_at = time.strftime('%Y-%m-%d %H:%M:%S')
update_at = time.strftime('%Y-%m-%d %H:%M:%S')
activation_status = 'Active'
type = 1
batch_update_code = 'A_220708182148_moa1g'
sql_BIZ = 'INSERT INTO account_auth VALUES '
sql_BSS = 'insert into bss_snmd_as_profile values '
userValues_BIZ_1 = []
userValues_BSS_1 = []
userValues_BIZ_2 = []
userValues_BSS_2 = []
userValues_BIZ_3 = []
userValues_BSS_3 = []
userValues_BIZ_4 = []
userValues_BSS_4 = []
userValues_BIZ_5 = []
userValues_BSS_5 = []
userValues_BIZ_6 = []
userValues_BSS_6 = []
sql_BIZ_1 = "INSERT INTO account_auth VALUE (%s,%s,%s,%s,%s,%s)"
sql_BSS_1 = "INSERT INTO bss_snmd_as_profile VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
def All_insert_BIZ_data(ALL):
    mysql_BIZ = DB_BIZ()
    mysql_BIZ.init()
    mysql_BIZ.insert_new_data(sql_BIZ_1, ALL)
    print("BIZ", ALL)
    mysql_BIZ.commit()

def All_insert_BSS_data(ALL):
    mysql_BSS = DB_BIZ()
    mysql_BSS.init()
    mysql_BSS.insert_new_data(sql_BIZ_1, ALL)
    print("BSS", ALL)
    mysql_BSS.commit()
if __name__ == '__main__':

    isim = Isim()
    file_csv = File_csv()
    file_csv_num = 1
    # mysql_BIZ_1 = DB_BIZ()
    # mysql_BSS_1 = DB_BSS()
    # mysql_BIZ_2 = DB_BIZ()
    # mysql_BSS_2 = DB_BSS()
    # mysql_BIZ_3 = DB_BIZ()
    # mysql_BSS_3 = DB_BSS()
    # mysql_BIZ_4 = DB_BIZ()
    # mysql_BSS_4 = DB_BSS()
    # mysql_BIZ_5 = DB_BIZ()
    # mysql_BSS_5 = DB_BSS()
    myredis = Db_myRedis()
    # mysql_BIZ.init()
    # mysql_BSS.init()
    # mysql_BIZ_1.init()
    # mysql_BSS_1.init()
    # mysql_BIZ_2.init()
    # mysql_BSS_2.init()
    # mysql_BIZ_3.init()
    # mysql_BSS_3.init()
    # mysql_BIZ_4.init()
    # mysql_BSS_4.init()
    # mysql_BIZ_5.init()
    # mysql_BSS_5.init()
    myredis.init()

    time_start = time.time()
    print("start time: ", time_start)

    for i in range(1, ES_TEST_TIME+1):
        if (i - 1) % ES_TEST_MAX_ITEM == 0:
            file_name = FILE_CSV_PREFIX + str(file_csv_num) + FILE_CSV_SUFFIX
            print(i, "open file: ", file_name)
            file_csv.open(file_name)
            file_csv_num = file_csv_num + 1

        index = i
        token = isim.get_token()
        imsi_main = isim.get_imsi(FLAG_MAIN)
        imsi_secd = isim.get_imsi(FLAG_SECD)
        subscribe = isim.get_subs(imsi_main)
        msisdn_main = isim.get_msisdn(FLAG_MAIN)
        msisdn_second = isim.get_msisdn(FLAG_SECD)
        iccid_secd = isim.get_iccid(FLAG_SECD)
        #imei = isim.get_imei()
        imei = isim.get_imei_id()
        eid = isim.get_eid()

        # print(index, subscribe, imsi_main, msisdn_main, imsi_secd, iccid_secd, imei, eid, token)
        #
        file_csv.write(index, subscribe,
                       imsi_main, msisdn_main,
                       imsi_secd, iccid_secd,
                       imei, eid,
                       token)

        ##########
        if i in (1, 2001):
            userValues_BIZ_1.append(
                (str(index), str(imsi_main), str(token), str(msisdn_main), str(create_at), str(update_at)))
            userValues_BSS_1.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second),
                                     str(iccid_secd), str(imei), str(eid), str(activation_status), str(date_time),
                                     str(index), str(type), str(batch_update_code), str(update_at), str(create_at)))
            # print("userValues_BIZ_1 ok ")
        if i in (2001, 4001):
            userValues_BIZ_2.append(
                (str(index), str(imsi_main), str(token), str(msisdn_main), str(create_at), str(update_at)))
            userValues_BSS_2.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second),
                                     str(iccid_secd), str(imei), str(eid), str(activation_status), str(date_time),
                                     str(index), str(type), str(batch_update_code), str(update_at), str(create_at)))
            # print("userValues_BIZ_2 ok ")
        if i in (4001, 6001):
            userValues_BIZ_3.append(
                (str(index), str(imsi_main), str(token), str(msisdn_main), str(create_at), str(update_at)))
            userValues_BSS_3.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second),
                                     str(iccid_secd), str(imei), str(eid), str(activation_status), str(date_time),
                                     str(index), str(type), str(batch_update_code), str(update_at), str(create_at)))
            # print("userValues_BIZ_3 ok ")
        if i in (6001, 8001):
            userValues_BIZ_4.append(
                (str(index), str(imsi_main), str(token), str(msisdn_main), str(create_at), str(update_at)))
            userValues_BSS_4.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second),
                                     str(iccid_secd), str(imei), str(eid), str(activation_status), str(date_time),
                                     str(index), str(type), str(batch_update_code), str(update_at), str(create_at)))
            # print("userValues_BIZ_4 ok ")
        if i in (8001, 10001):
            userValues_BIZ_5.append(
                (str(index), str(imsi_main), str(token), str(msisdn_main), str(create_at), str(update_at)))
            userValues_BSS_5.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second),
                                     str(iccid_secd), str(imei), str(eid), str(activation_status), str(date_time),
                                     str(index), str(type), str(batch_update_code), str(update_at), str(create_at)))
            # print("userValues_BIZ_5 ok ")

        # data_list_BIZ_1 = (mysql_BIZ_1, userValues_BIZ_1)
        # data_list_BIZ_2 = (mysql_BIZ_2, userValues_BIZ_2)
        # data_list_BIZ_3 = (mysql_BIZ_3, userValues_BIZ_3)
        # data_list_BIZ_4 = (mysql_BIZ_4, userValues_BIZ_4)
        # data_list_BIZ_5 = (mysql_BIZ_5, userValues_BIZ_5)
        data_list_BIZ = [userValues_BIZ_1, userValues_BIZ_2, userValues_BIZ_3, userValues_BIZ_4, userValues_BIZ_5]
        # print(data_list_BIZ_1)

        # data_list_BSS_1 = (mysql_BSS_1, userValues_BSS_1)
        # data_list_BSS_2 = (mysql_BSS_2, userValues_BSS_2)
        # data_list_BSS_3 = (mysql_BSS_3, userValues_BSS_3)
        # data_list_BSS_4 = (mysql_BSS_4, userValues_BSS_4)
        # data_list_BSS_5 = (mysql_BSS_5, userValues_BSS_5)
        data_list_BSS = [userValues_BSS_1, userValues_BSS_2, userValues_BSS_3, userValues_BSS_4, userValues_BSS_5]
        # data_list_BIZ = [data_list_BIZ_1, data_list_BIZ_1, data_list_BIZ_1, data_list_BIZ_1, data_list_BIZ_1]
        # print(data_list_BIZ)
        if i>10000:
            print("开始pool")
            pool = Pool(5)
            pool.map(All_insert_BIZ_data, data_list_BIZ)
            pool.map(All_insert_BSS_data, data_list_BSS)
            # pool.map(All_insert_BIZ_data, data_list_BIZ)
            # pool.map(All_insert_BSS_data,[data_list_BSS_1, data_list_BSS_1, data_list_BSS_1, data_list_BSS_1, data_list_BSS_1])
            # with Pool(5) as pool:
            #     pool.map(All_insert_BIZ_data,
            #              [data_list_BIZ_1, data_list_BIZ_1, data_list_BIZ_1, data_list_BIZ_1, data_list_BIZ_1])
            #     pool.map(All_insert_BSS_data,
            #              [data_list_BSS_1, data_list_BSS_1, data_list_BSS_1, data_list_BSS_1, data_list_BSS_1])
            userValues_BIZ_1 = []
            userValues_BSS_1 = []
            userValues_BIZ_2 = []
            userValues_BSS_2 = []
            userValues_BIZ_3 = []
            userValues_BSS_3 = []
            userValues_BIZ_4 = []
            userValues_BSS_4 = []
            userValues_BIZ_5 = []
            userValues_BSS_5 = []
            userValues_BIZ_6 = []
            userValues_BSS_6 = []
        myredis.insert(imsi_main, token, msisdn_main)

    # mysql_BIZ_1.commit()
    # mysql_BSS_1.commit()
    # mysql_BIZ_2.commit()
    # mysql_BSS_2.commit()
    # mysql_BIZ_3.commit()
    # mysql_BSS_3.commit()
    # mysql_BIZ_4.commit()
    # mysql_BSS_4.commit()
    # mysql_BIZ_5.commit()
    # mysql_BSS_5.commit()

    # myredis.commit()
    time_end = time.time()
    print("finish time: ", time_end)
    print("cost time: ", time_end - time_start)

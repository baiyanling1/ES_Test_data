# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from isim import Isim
from file_csv import File_csv
from data_base_liantong import DB_REPORT
# from data_base import DB_BSS
# from redis_DB import Db_myRedis
import time
from multiprocessing import Pool

# #数据总条数
# ES_TEST_TIME = 100000
#
# #一个文件最大5000条数据
# ES_TEST_MAX_ITEM = 5000

ES_TEST_TIME = 3000000
ES_TEST_MAX_ITEM = 20000

FLAG_MAIN = 1
FLAG_SECD = 2
FILE_CSV_PREFIX = "/Users/hejian/Desktop/2024移动ES性能测试数据/huawei-token-expire/account-auth-huawei-token-expire-"
FILE_CSV_SUFFIX = ".csv"
# FILE_token_expire = "/Users/hejian/Desktoptoken_expire.csv"

alt_smdp_fqdn = "LPA:1$esim.yhdzd.chinamobile.com:8002$"
date_time = "20240509163508"
create_at = time.strftime('%Y-%m-%d %H:%M:%S')
update_at = time.strftime('%Y-%m-%d %H:%M:%S')
activation_status = 'Active'
type = 1
batch_update_code = 'A_220708182148_hwexpire'
sql_BIZ = 'INSERT INTO account_info VALUES '
# sql_BSS = 'insert into bss_snmd_as_profile values '
userValues_BIZ = []
# userValues_BSS = []
# csvValue=[]
# csvValue_all=[]
sql_BIZ_1 = "INSERT INTO account_info VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# sql_BSS_1 = "INSERT INTO bss_snmd_as_profile VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
if __name__ == '__main__':

    isim = Isim()
    file_csv = File_csv()
    file_csv_all = File_csv()
    mysql_BIZ = DB_REPORT()
    # mysql_BSS = DB_BSS()
    # myredis = Db_myRedis()
    file_csv_num = 1
    mysql_BIZ.init()
    # mysql_BSS.init()
    # myredis.init()

    time_start = time.time()
    print("start time: ", time_start)
    file_name_ALL = FILE_CSV_PREFIX + 'ALL' + FILE_CSV_SUFFIX
    file_csv_all.open(file_name_ALL)
    for i in range(1, ES_TEST_TIME+1):
        if (i - 1) % ES_TEST_MAX_ITEM == 0:
            # file_csv.write_all(csvValue)
            mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
            # mysql_BSS.insert_new_data(sql_BSS_1, userValues_BSS)
            # file_name = FILE_CSV_PREFIX + str(file_csv_num) + FILE_CSV_SUFFIX
            # print(i, "open file: ", file_name)
            # file_csv.open(file_name)
            # file_csv_num = file_csv_num + 1
            userValues_BIZ = []
            # userValues_BSS = []
            # csvValue = []

        index = 600000000 + i
        # token = isim.get_token()
        imsi_main = isim.get_imsi(FLAG_MAIN)
        # imsi_secd = isim.get_imsi(FLAG_SECD)
        # subscribe = isim.get_subs(imsi_main)
        msisdn_main = isim.get_msisdn(FLAG_MAIN)
        # msisdn_second = isim.get_msisdn(FLAG_SECD)
        # iccid_main = isim.get_iccid(FLAG_MAIN)
        # iccid_secd = isim.get_iccid(FLAG_SECD)
        #imei = isim.get_imei()
        # device_type = 2
        imei = isim.get_imei_id()
        # eid = isim.get_eid()
        # csvValue_all.append((index, subscribe,
        #                  imsi_main, msisdn_main, iccid_main,
        #                  imsi_secd, iccid_secd,
        #                  imei, eid,
        #                  token))
        #
        # csvValue.append((index, subscribe,
        #                  imsi_main, msisdn_main, iccid_main,
        #                  imsi_secd, iccid_secd,
        #                  imei, eid,
        #                  token))

        userValues_BIZ.append((str(index), str(imei), str(msisdn_main), str(imsi_main), None, None, None, None, None, None, str("2024-04-23 14:59:56"), None, None, None, None))
        # mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
        # userValues_BSS.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second), str(iccid_secd), str(imei), str(eid), str(activation_status), str(date_time), str(index), str(type), str(batch_update_code), str(update_at), str(create_at)))
        #将token插入redis中
        # myredis.insert(imsi_main, token, msisdn_main)
        # 最后一次文件写入和sql执行
        if i == ES_TEST_TIME:
            # file_csv.write_all(csvValue)
            mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
            # mysql_BSS.insert_new_data(sql_BSS_1, userValues_BSS)


    mysql_BIZ.commit()
    # mysql_BSS.commit()
    #把所有数据写入一个csv文件中
    # file_csv_all.write_all(csvValue_all)
    time_end = time.time()
    print("finish time: ", time_end)
    print("cost time: ", time_end - time_start)

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from isim import Isim
from file_csv import File_csv
from data_base_Thacio import DB_BIZ
# from data_base import DB_BSS
# from redis_DB import Db_myRedis
import time
import uuid
from multiprocessing import Pool

# #数据总条数
# ES_TEST_TIME = 100000
#
# #一个文件最大5000条数据
# ES_TEST_MAX_ITEM = 5000

ES_TEST_TIME = 4000000
ES_TEST_MAX_ITEM = 10000

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
sql_BIZ = 'INSERT INTO account_auth VALUES '
userValues_BIZ = []
userValues_BSS = []

sql_volte_1 = "INSERT INTO tbl_volte_service VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

sql_phenix_1 = "INSERT INTO tbl_phoenix_service VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

if __name__ == '__main__':

    isim = Isim()
    mysql_BIZ = DB_BIZ()
    mysql_BIZ.init()

    time_start = time.time()
    print("start time: ", time_start)
    for i in range(1, ES_TEST_TIME+1):
        if (i - 1) % ES_TEST_MAX_ITEM == 0:
            mysql_BIZ.insert_new_data(sql_phenix_1, userValues_BIZ)
            userValues_BIZ = []

        token = isim.get_token()
        primary_imsi = isim.get_imsi(FLAG_MAIN)
        imsi = isim.get_imsi(FLAG_SECD)
        # subscribe = isim.get_subs(primary_imsi)
        primary_msisdn = isim.get_msisdn(FLAG_MAIN)
        msisdn = isim.get_msisdn(FLAG_SECD)
        primary_iccid = isim.get_iccid(FLAG_MAIN)
        iccid = isim.get_iccid(FLAG_SECD)
        # imei = isim.get_imei()
        provisioning_status = 0
        imei = isim.get_imei_id()
        eid = isim.get_eid()
        index = 1 + i
        # userValues_BIZ.append((str(index), str(imsi), str(msisdn), None, str(provisioning_status), '2024-08-28 02:57:18', '2024-08-30 03:20:50',None,None,None,None))
        userValues_BIZ.append((str(index), str(imsi), str(msisdn), None, '6100','1','500','sub6', '2024-08-28 02:57:18', '2024-08-30 03:20:50',None,None,None,None,None))



        # userValues_BIZ.append((str(index), str(imsi_main), str(token), str(msisdn_main), str(device_type),  str(create_at), str(update_at)))
        # 最后一次文件写入和sql执行
        if i == ES_TEST_TIME:
            mysql_BIZ.insert_new_data(sql_phenix_1, userValues_BIZ)


    mysql_BIZ.commit()
    time_end = time.time()
    print("finish time: ", time_end)
    print("cost time: ", time_end - time_start)

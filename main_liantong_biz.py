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

ES_TEST_TIME = 30000000
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
userValues_BIZ = []
sql_BIZ_1 = "INSERT INTO account_info VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# sql_BSS_1 = "INSERT INTO bss_snmd_as_profile VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
if __name__ == '__main__':

    isim = Isim()
    mysql_BIZ = DB_REPORT()
    file_csv_num = 1
    mysql_BIZ.init()

    time_start = time.time()
    print("start time: ", time_start)
    for i in range(1, ES_TEST_TIME+1):
        if (i - 1) % ES_TEST_MAX_ITEM == 0:
            mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
            # mysql_BIZ.commit()
            userValues_BIZ = []

        index = 0 + i
        imsi_main = isim.get_imsi(FLAG_MAIN)
        msisdn_main = isim.get_msisdn(FLAG_MAIN)
        imei = isim.get_imei_id()

        userValues_BIZ.append((str(index), str(imei), str(msisdn_main), str(imsi_main), None, None, None, None, None, None, str("2024-04-23 14:59:56"), None, None, None, None))
        if i == ES_TEST_TIME:
            mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
            # mysql_BIZ.commit()


    mysql_BIZ.commit()
    time_end = time.time()
    print("finish time: ", time_end)
    print("cost time: ", time_end - time_start)

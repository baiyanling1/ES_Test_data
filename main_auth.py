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


ES_TEST_TIME = 2
ES_TEST_MAX_ITEM = 5000

FLAG_MAIN = 1
FLAG_SECD = 2
FILE_CSV_PREFIX = "/Users/redtea/Desktop/account-quth"
FILE_CSV_SUFFIX = ".csv"
FILE_token_expire = "/Users/redtea/Desktop/token_expire.csv"

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
# sql_BIZ_1 = "INSERT INTO account_auth VALUE (%s,%s,%s,%s,%s,%s)"
sql_BIZ_1 = "INSERT INTO account_auth (imsi, imei, token, msisdn, interface_type, create_at, update_at) VALUE (%s,%s,%s,%s,%s,%s,%s)"
sql_BSS_1 = "INSERT INTO bss_snmd_as_profile VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
if __name__ == '__main__':

    isim = Isim()
    # file_csv = File_csv()
    mysql_BIZ = DB_BIZ()
    # mysql_BSS = DB_BSS()
    # myredis = Db_myRedis()
    file_csv_num = 1
    mysql_BIZ.init()
    # mysql_BSS.init()
    # myredis.init()

    time_start = time.time()
    print("start time: ", time_start)

    for i in range(1, ES_TEST_TIME+1):
        index = i
        # print(FLAG_MAIN)
        token = isim.get_token()
        imsi_main = isim.get_imsi(FLAG_MAIN)
        imsi_secd = isim.get_imsi(FLAG_SECD)
        subscribe = isim.get_subs(imsi_main)
        msisdn_main = isim.get_msisdn(FLAG_MAIN)
        msisdn_second = isim.get_msisdn(FLAG_SECD)
        iccid_main = isim.get_iccid(FLAG_MAIN)
        iccid_secd = isim.get_iccid(FLAG_SECD)
        #imei = isim.get_imei()
        imei = isim.get_imei_id()
        eid = isim.get_eid()
        # userValues_BIZ.append((str(imsi_main), str(token), str(msisdn_main), str(create_at), str(update_at)))
        userValues_BIZ.append((str(imsi_main), str(imei), str(token), str(msisdn_main), 'APPLE', str(create_at), str(update_at)))
        # print(userValues_BIZ)
        # userValues_BSS.append((str(index), str(msisdn_main), str(alt_smdp_fqdn), str(msisdn_second), str(iccid_secd), str(imei), str(eid), str(activation_status), str(date_time), str(index), str(type), str(batch_update_code), str(update_at), str(create_at)))
        mysql_BIZ.insert_new_data(sql_BIZ_1, userValues_BIZ)
        # FLAG_MAIN+=i
        userValues_BIZ = []
    mysql_BIZ.commit()
    time_end = time.time()
    print("finish time: ", time_end)
    print("cost time: ", time_end - time_start)

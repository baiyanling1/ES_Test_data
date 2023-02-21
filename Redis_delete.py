

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

def Redis_delete(i):
    myredis = Db_myRedis()
    myredis.init()
    myredis.delete(460160001230088)

    # print("并发函数 %s 开始：", i)
    # FLAG_MAIN = i+100000000
    # FLAG_SECD = i+200000000
    # myredis = Db_myRedis()
    # isim = Isim()
    # myredis.init()
    # for i in range(i, i + 20000):
    #     imsi_main = isim.get_imsi(FLAG_MAIN)
    #     myredis.delete(imsi_main)

if __name__ == '__main__':
    time_start = time.time()
    Redis_delete(9980001)
    # print("start time: ",  time.strftime('%Y-%m-%d %H:%M:%S'))
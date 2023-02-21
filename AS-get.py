from isim import Isim
import time
import random
surname = ["白yl","米n","wendi","赵xu","lucy"]

if __name__ == '__main__':
    time_start = time.time()
    print("start time: ", time.strftime('%Y-%m-%d %H:%M:%S'))
    isim = Isim()
    Note = open('/Users/redtea/Desktop/AS-5000000-0908.dat', mode='a')
    FLAG_MAIN = 1
    FLAG_SECD = 2
    alt_smdp_fqdn = "LPA:1$esim.yhdzd.chinamobile.com:8002$"
    date_time = "20220826163508"
    activation_status = 'Active'
    type = 1
    batch_update_code = 'A_220708182148_moa1g'
    for i in range(1, 5000001):
        imei = isim.get_imei_id()
        eid = isim.get_eid()
        imsi_main = isim.get_imsi(FLAG_MAIN)
        imsi_secd = isim.get_imsi(FLAG_SECD)
        subscribe = isim.get_subs(imsi_main)
        msisdn_main = isim.get_msisdn(FLAG_MAIN)
        msisdn_second = isim.get_msisdn(FLAG_SECD)
        iccid_main = isim.get_iccid(FLAG_MAIN)
        iccid_secd = isim.get_iccid(FLAG_SECD)
        Note.write(str(msisdn_main) + "|" + str(random.choice(surname)) + "|" +"1"+ "|" +str(msisdn_second)+ "|" +str(iccid_secd)+ "|" +str(eid)+ "|" +str(imei)+ "|" +"Active"+ "|" +"202209081526"+ "|" +" "+ "|" +'\n')

    Note.close()

    time_end = time.time()
    print("finish time: ", time.strftime('%Y-%m-%d %H:%M:%S'))
    print("cost time: ", time_end - time_start)

from isim import Isim

FLAG_MAIN = 1
FLAG_SECD = 2
if __name__ == '__main__':
    isim = Isim()
    Note = open('/Users/redtea/Desktop/IMEIEID_HUAWEI_P1_20220907110443_01.dat', mode='a')

    # imei = isim.get_imei()
    imei = isim.get_imei_id()
    eid = isim.get_eid()
    for i in range(30, 40):
        imei = isim.get_imei_id()
        eid = isim.get_eid()
        Note.write(str(imei)+"|"+str(eid)+'\n')

    Note.close()

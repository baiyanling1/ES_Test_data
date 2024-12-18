import time
import threading
import string
import base64
import random

# #token过期数据：
# INIT_IMSI = 461030000000000
# INIT_MSISDN = 13400300001
# INIT_ICCID = 46034567897600000000
# # INIT_IMSI = 460120000000000
# # INIT_MSISDN = 13200300001
# # INIT_ICCID = 46021567897600000000
# INIT_IMEI = 86726303000000
# INIT_IMEI_SN = 0
# # INIT_EID = 34850082573294848000000000000000
# INIT_EID=34840082573294848000000000000000
# INIT_SUBS = "@ims.mnc008.mcc460.3gppnetwork.org"
# # INIT_TAC = [866367, 866058, 865913]
# INIT_TAC = [869112, 862413, 869262]

# #token有效数据：
# INIT_IMSI = 461040000000000
# INIT_MSISDN = 13400400001
# INIT_ICCID = 46044567897600000000
# # INIT_IMSI = 460120000000000
# # INIT_MSISDN = 13200300001
# # INIT_ICCID = 46021567897600000000
# INIT_IMEI = 86726403000000
# INIT_IMEI_SN = 0
# # INIT_EID = 34850082573294848000000000000000
# INIT_EID=34840082574294848000000000000000
# INIT_SUBS = "@ims.mnc008.mcc460.3gppnetwork.org"
# # INIT_TAC = [866367, 866058, 865913]
# INIT_TAC = [869112, 862413, 869262]
# #华为token有效数据：
# INIT_IMSI = 461050000000000
# INIT_MSISDN = 13500400001
# INIT_ICCID = 46054567897600000000
# # INIT_IMSI = 460120000000000
# # INIT_MSISDN = 13200300001
# # INIT_ICCID = 46021567897600000000
# INIT_IMEI = 86726503000000
# INIT_IMEI_SN = 0
# # INIT_EID = 34850082573294848000000000000000
# INIT_EID=34840082575294848000000000000000
# INIT_SUBS = "@ims.mnc008.mcc460.3gppnetwork.org"
# # INIT_TAC = [866367, 866058, 865913]
# INIT_TAC = [869112, 862413, 869262]

#华为token过期数据：
INIT_IMSI = 520053061000000
INIT_MSISDN = 13811400001
INIT_ICCID = 46055777897600000000
# INIT_IMSI = 460120000000000
# INIT_MSISDN = 13200300001
# INIT_ICCID = 46021567897600000000
INIT_IMEI = 86725713000000
INIT_IMEI_SN = 0
# INIT_EID = 34850082573294848000000000000000
INIT_EID=34850182675295848000000000000000
INIT_SUBS = "@ims.mnc008.mcc460.3gppnetwork.org"
# INIT_TAC = [866367, 866058, 865913]
INIT_TAC = [869112, 862413, 869262]



class Isim(object):
    def __init__(self):
        self.imsi = INIT_IMSI
        self.msisdn = INIT_MSISDN
        self.iccid = INIT_ICCID
        self.imei = INIT_IMEI
        self.imei_sn = INIT_IMEI_SN
        self.eid = INIT_EID
        self.TAC = random.choice(INIT_TAC)

    def get_token(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
        characters = random.sample(alphabet, 12)
        n = ''.join(characters)
        token = base64.b64encode(n.encode('utf-8'))
        token = str(token, 'utf-8')
        return token

    def get_subs(self, imsi):
        s = str(imsi) + INIT_SUBS
        subs_ori = base64.b64encode(s.encode('utf-8'))
        subs = str(subs_ori, 'utf-8')
        return subs

    def get_imsi(self, main_flag):
        self.imsi = self.imsi + main_flag
        # print(self.imsi)
        return self.imsi

    def get_msisdn(self, main_flag):
        self.msisdn = self.msisdn + main_flag
        return self.msisdn

    def get_iccid(self, main_flag):
        self.iccid = self.iccid + main_flag
        return self.iccid

    def get_imei_id(self):
        imei = 0
        tac = random.choice(INIT_TAC)
        #tac = 867263
        fac = 4
        sn = self.imei_sn
        cd = 0

        #imei = 867263 * 100 + fac
        imei = tac * 100 + fac
        imei = imei * 1000000 + sn

        #caculate check data
        cd_data = imei
        for i in range(0, 14):
            bit = cd_data % 10
            if i % 2 == 0:
                bit = bit * 2
                cd = int(cd + (bit / 10) + (bit % 10))
            else:
                cd = int(cd + bit)
            cd_data = int(cd_data / 10)
        cd = cd % 10
        if cd != 0:
            cd = 10 - cd

        imei = imei * 10 + cd
        self.imei_sn = self.imei_sn + 1
        return imei

    def get_imei(self):
        imei_14 = str(self.imei)
        imei_15 = 0
        for num in range(14):
            if num % 2 == 0:
                imei_15 = imei_15 + int(imei_14[num])
            else:
                imei_15 = imei_15 + (int(imei_14[num]) * 2) % 10 + (int(imei_14[num]) * 2) / 10
        imei_15 = int(imei_15) % 10
        if imei_15 == 0:
            imei = imei_14 + str(imei_15)
        else:
            imei = imei_14 + str(10 - imei_15)
        self.imei = self.imei + 1
        return imei

    def get_eid(self):
        eid = self.eid
        row1 = eid
        y = row1 % 97
        eid_new = 98 - y + row1
        self.eid += 100000000
        return eid_new
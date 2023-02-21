import time
import threading
import string
import base64
import csv

KEY_IDX = "index"
KEY_SUBC = "subscriber"
KEY_IMSI_MAIN = "main-imsi"
KEY_IMSI_SECD = "secondry-imsi"
KEY_MSISDN_MAIN = "main-msisdn"
KEY_MSISDN_SECD = "secondry-msisdn"
KEY_ICCID_MAIN = "main-iccid"
KEY_ICCID_SECD = "secondry-iccid"
KEY_IMEI_SECD = "secondry-imei"
KEY_EID_SECD = "secondry-eid"
KEY_TOKEN = "token"

class File_csv(object):
    def __init__(self):
        self.file_name = 0
        self.writer = 0

    def open(self, name):
        self.file_name = name
        with open(self.file_name, "a") as csvfile:
            self.writer = csv.writer(csvfile)
            self.writer.writerow([KEY_IDX, KEY_SUBC,
                                  KEY_IMSI_MAIN, KEY_MSISDN_MAIN,KEY_ICCID_MAIN,
                                  KEY_IMSI_SECD, KEY_ICCID_SECD,
                                  KEY_IMEI_SECD, KEY_EID_SECD,KEY_MSISDN_SECD,
                                  KEY_TOKEN])

    def write(self, index, subscribe, imsi_main, msisdn_main, iccid_main, imsi_secd,
                    iccid_secd, imei_secd, eid_secd, msisdn_secd, token):
        with open(self.file_name, "a") as csvfile:
            self.writer = csv.writer(csvfile)
            self.writer.writerow([index, subscribe,
                                  imsi_main, msisdn_main, iccid_main,
                                  imsi_secd, iccid_secd,
                                  imei_secd, eid_secd,msisdn_secd,
                                  token])
        return 0
    def write_all(self,all):
        with open(self.file_name, "a") as csvfile:
            self.writer = csv.writer(csvfile)
            self.writer.writerows(all)
        return 0

    def close(self):
        return 0

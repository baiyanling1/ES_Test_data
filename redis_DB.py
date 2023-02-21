
import redis

REDIS_IP='10.10.0.4'
REDIS_PORT=6379
REDIS_PWD='QaKdgBiaz6B6'


class Db_myRedis(object):
    def __init__(self):
        self.file = 0
        self.r=''

    def init(self):
        self.r = redis.Redis(host=REDIS_IP, port=REDIS_PORT, password=REDIS_PWD)

    def insert(self, imsi, token, msisdn):
        self.r.hset("com.redteamobile.es.auth.token:"+str(imsi), "token", token)
        self.r.hset("com.redteamobile.es.auth.token:"+str(imsi), "primaryMsisdn", str(msisdn))

    def delete(self, imsi):
        self.r.delete("com.redteamobile.es.auth.token:"+str(imsi))
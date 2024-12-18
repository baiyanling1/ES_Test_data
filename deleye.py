import redis

# 请替换为您的 Redis 主机、端口和密码
REDIS_HOST = '10.18.50.178'  # 根据实际情况修改
REDIS_PORT = 6379  # 根据实际情况修改
REDIS_PASSWORD = 'QaKdgBiaz6B6'  # 替换为您的密码

# 连接到 Redis
try:
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    # 检查连接是否成功
    r.ping()
    print("Connected to Redis")
except redis.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    exit(1)


def delete_matching_keys(pattern):
    cursor = 0
    total_deleted = 0
    batch_size = 10000  # 每批处理的键数量

    while True:
        try:
            # 执行 SCAN 命令
            cursor, keys = r.scan(cursor, match=pattern)

            if keys:
                for i in range(0, len(keys), batch_size):
                    batch = keys[i:i + batch_size]
                    deleted_count = r.delete(*batch)  # 批量删除
                    total_deleted += deleted_count
                    # print(f'Deleted batch of {deleted_count} keys: {batch}')

            # 如果游标返回到 0，则停止循环
            if cursor == 0:
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    print(f'Total deleted keys: {total_deleted}')


if __name__ == "__main__":
    # delete_matching_keys('com.redteamobile.es.auth.token:*')
    delete_matching_keys('com.redteamobile.es.auth.msisdn:*')
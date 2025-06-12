import redis

# 连接到 Redis 服务器
client = redis.StrictRedis(host='10.18.50.26', port=6379, password='redtea.123', db=0, decode_responses=True)

# Redis Hash 名称
hash_name = "com.redteamobile.es.stat.snmp:"  # 确保 Hash 名称与 Redis CLI 中完全一致

try:
    # 获取 Hash 中的所有键
    all_keys = client.hkeys(hash_name)
    if not all_keys:
        print(f"No keys found in hash: {hash_name}. Please verify the hash name.")
    else:
        print(f"Found {len(all_keys)} keys in hash: {hash_name}")

        # 遍历每个键并更新值为 "10"
        for key in all_keys:
            # 打印执行的 Redis 命令
            print(f"HSET {hash_name} {key} 10")
            client.hset(hash_name, key, "10")

        # 如果需要，可以检查并打印更新后的 Hash 内容
        # updated_values = client.hgetall(hash_name)
        # print(f"Updated Hash Values: {updated_values}")

except Exception as e:
    print(f"Error: {e}")

import redis

# 连接到 Redis 服务器
client = redis.StrictRedis(host='10.18.50.26', port=6379, password='redtea.123', db=0, decode_responses=True)

# Redis Hash 名称
hash_name = "com.redteamobile.es.stat.snmp:"  # 确保 Hash 名称与 Redis CLI 中完全一致


# HSET com.redteamobile.es.stat.snmp: 1.3.6.1.4.1.50791.1.20.12.0 1

try:
    # 获取 Hash 中的所有键
    all_keys = client.hkeys(hash_name)
    if not all_keys:
        print(f"No keys found in hash: {hash_name}. Please verify the hash name.")
    else:
        print(f"Found {len(all_keys)} keys in hash: {hash_name}")

        # 遍历每个键并更新值为 "1"
        for key in all_keys:
            # 获取当前键的值
            current_value = client.hget(hash_name, key)
            print(f"Current value for {key}: {current_value}")

            # 如果当前值为 "0" 或者值为空（意味着没有值），则更新为 "1"
            if current_value == "1" or current_value is None:
                client.hset(hash_name, key, "10")
                print(f"Updated Key: {key} to Value: 1")
            else:
                print(f"Key: {key} already has Value: {current_value}, no update needed.")

        # 检查并打印更新后的 Hash 内容
        updated_values = client.hgetall(hash_name)
        print(f"Updated Hash Values: {updated_values}")

except Exception as e:
    print(f"Error: {e}")

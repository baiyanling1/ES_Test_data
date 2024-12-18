import redis
import csv

# 连接到远程 Redis 服务器，并使用密码进行身份验证
r = redis.StrictRedis(host='10.18.50.178', port=6379, password='QaKdgBiaz6B6', db=0)

# 定义输出 CSV 文件的名称和路径
output_file = '/Users/hejian/Desktop/ES/泰国/性能测试/data/auth/exported_tokens-0910.csv'

# 批量操作的大小，调整该值可以优化性能
batch_size = 1000

# 打开 CSV 文件进行写操作
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # 写入 CSV 文件的头部
    writer.writerow(['Key Suffix', 'Token'])

    # 用于存储批量数据的列表
    batch_data = []

    # 获取所有符合特定模式的键
    for key in r.scan_iter(match="com.redteamobile.es.auth.token:*"):
        # 使用 Redis Pipeline 来批量获取数据
        pipeline = r.pipeline()
        key_suffix = key.decode().split(":")[-1]

        # 假设整个字符串是 'token' 值，'msisdn' 不存在
        pipeline.get(key)
        token = pipeline.execute()[0]

        # 添加到批量数据列表中
        if token:
            batch_data.append([key_suffix, token.decode()])

        # 如果达到批量大小，写入文件并清空批量数据列表
        if len(batch_data) >= batch_size:
            writer.writerows(batch_data)
            batch_data = []

    # 写入最后一批数据
    if batch_data:
        writer.writerows(batch_data)

print(f"Data export to {output_file} is complete.")

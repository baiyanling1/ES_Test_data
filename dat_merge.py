import os

# 设置存放 .DAT 文件的目录
directory = "/Users/hejian/Desktop/移动ES/2025割接/华为25号文件"  # 修改为你的 .dat 文件所在的目录
output_file = os.path.join(directory, "merged_output.dat")

# 用于存储唯一的数据行
unique_lines = set()

# 检查目录是否存在
if not os.path.exists(directory):
    print(f"错误：目录 {directory} 不存在！")
    exit(1)

# 获取所有 .dat 文件（不区分大小写）
dat_files = [f for f in os.listdir(directory) if f.lower().endswith('.dat')]
# print(f"找到 {len(dat_files)} 个 .dat 文件：")
# for f in dat_files:
#     print(f"- {f}")

if not dat_files:
    print("错误：目录中没有找到 .dat 文件！")
    exit(1)

# 遍历目录中的所有 .dat 文件
for filename in dat_files:
    file_path = os.path.join(directory, filename)
    # print(f"\n正在处理文件：{filename}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            line_count = 0
            for line in file:
                unique_lines.add(line.strip())  # 去除换行符并添加到集合（去重）
                line_count += 1
            # print(f"从 {filename} 读取了 {line_count} 行")
    except Exception as e:
        print(f"处理文件 {filename} 时出错：{str(e)}")

print(f"\n总共收集到 {len(unique_lines)} 行唯一数据")

# 将去重后的数据写入新文件
with open(output_file, "w", encoding="utf-8") as out_file:
    for line in sorted(unique_lines):  # 排序后写入
        out_file.write(line + "\n")

print(f"合并完成，去重后数据已保存到 {output_file}")

from isim import Isim
import csv
import os
import datetime

# 创建 Isim 实例
isim = Isim()
# 设置 FLAG_MAIN
FLAG_MAIN = 1
FLAG_SECD = 2

#生成 imis ranges
def expand_prefix_range(start_prefix, end_prefix, count_per_prefix):
    """
    将起止前缀转换为 [[前缀, 数量], ...]
    """
    return [[prefix, count_per_prefix] for prefix in range(start_prefix, end_prefix + 1)]

def expand_multiple_prefix_ranges(ranges, count_per_prefix):
    """
    接收多个起止前缀范围，输出 [[prefix, count], ...] 列表
    """
    result = []
    for start, end in ranges:
        result.extend([[prefix, count_per_prefix] for prefix in range(start, end + 1)])
    return result

def generate_csv_only_imsi(filename, total_count):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['main-imsi'])  # 写入表头

            for _ in range(total_count):
                main_imsi = isim.get_imsi(FLAG_MAIN)  # 获取 main-imsi
                main_imei = isim.get_imei_id()
                imei = isim.get_imei_id()
                eid = isim.get_eid()
                writer.writerow([main_imsi])  # 写入每一行
        print(f"CSV 文件 '{filename}' 已生成，包含 {total_count} 条数据。")
    except Exception as e:
        print(f"生成 CSV 文件时出错: {e}")

def generate_csv_only_imsi_and_imei(filename, total_count):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['main-imsi','main-imei'])  # 写入表头
            for _ in range(total_count):
                main_imsi = isim.get_imsi(FLAG_MAIN)  # 获取 main-imsi
                main_imei = isim.get_imei_id()
                writer.writerow([main_imsi,main_imei])  # 写入每一行
        print(f"CSV 文件 '{filename}' 已生成，包含 {total_count} 条数据。")
    except Exception as e:
        print(f"生成 CSV 文件时出错: {e}")

def generate_csv_imsi_range(filename, total_count, ranges):
    """
    生成 IMSI + IMEI 的 CSV 文件
    :param filename: 输出 CSV 文件路径
    :param total_count: 总共生成多少条数据
    :param ranges: IMSI 生成的前缀和数量范围，例如 [[4605577, 3], [4605588, 2]]
    """
    gen = Isim(ranges)
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['main-imsi', 'main-imei'])  # 写入表头
            for _ in range(total_count):
                main_imsi = gen.get_next_imsi()  # 获取 main-imsi
                main_imei = gen.get_imei_id()    # 获取 main-imei
                writer.writerow([main_imsi, main_imei])
        print(f"✅ CSV 文件 '{filename}' 已生成，包含 {total_count} 条数据。")
    except Exception as e:
        print(f"❌ 生成 CSV 文件时出错: {e}")

def generate_multisim_csv(filename, total_count):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['main-imsi', 'main-imei', 'main-msisdn', 'main-iccid', 'secondary-imei', 'secondary-eid', 'secondary-msisdn', 'secondary-iccid', 'secondary-imsi'])  # 写入表头

            for _ in range(total_count):
                main_imsi = isim.get_imsi(FLAG_MAIN)  # 获取 main-imsi
                main_imei = isim.get_imei_id()
                main_msisdn = isim.get_msisdn(FLAG_MAIN)
                imei = isim.get_imei_id()
                eid = isim.get_eid()
                msisdn_second = isim.get_msisdn(FLAG_SECD)
                iccid_secd = isim.get_iccid(FLAG_SECD)
                secd_imsi = isim.get_imsi(FLAG_SECD)
                main_iccid = isim.get_iccid(FLAG_MAIN)
                writer.writerow([main_imsi, main_imei, main_msisdn, main_iccid, imei, eid, msisdn_second, iccid_secd, secd_imsi])  # 写入每一行
        print(f"CSV 文件 '{filename}' 已生成，包含 {total_count} 条数据。")
    except Exception as e:
        print(f"生成 CSV 文件时出错: {e}")

def split_csv(input_filename, split_count):
    try:
        # 获取原文件的目录
        directory = os.path.dirname(input_filename)
        base_name = os.path.basename(input_filename).replace('.csv', '')  # 获取文件名（不带扩展名）

        with open(input_filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # 读取表头

            current_file_index = 1
            current_row_count = 0

            # 创建第一个输出文件
            output_file = open(os.path.join(directory, f'{base_name}_part_{current_file_index}.csv'), mode='w',
                               newline='')
            writer = csv.writer(output_file)
            writer.writerow(header)  # 写入表头

            for row in reader:
                writer.writerow(row)
                current_row_count += 1

                if current_row_count >= split_count:
                    output_file.close()  # 关闭当前文件
                    current_file_index += 1
                    current_row_count = 0

                    # 创建下一个输出文件
                    output_file = open(os.path.join(directory, f'{base_name}_part_{current_file_index}.csv'), mode='w',
                                       newline='')
                    writer = csv.writer(output_file)
                    writer.writerow(header)  # 写入表头到新文件

            # 确保最终的文件被关闭且是有效写入
            if current_row_count > 0:
                output_file.close()  # 关闭最后一个文件
            else:
                output_file.close()  # 关闭文件，避免留下空文件
                os.remove(os.path.join(directory, f'{base_name}_part_{current_file_index}.csv'))  # 删除空文件

        print(f"已将 '{input_filename}' 拆分为多个文件，每个文件包含 {split_count} 条数据，并保存在原目录下。")
    except Exception as e:
        print(f"拆分 CSV 文件时出错: {e}")

def generate_output_filename(base_dir, prefix, total_count):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return os.path.join(base_dir, f"{prefix}_{total_count}_{now}.csv")

if __name__ == "__main__":
    base_dir = r'E:\联通ES\性能'
    prefix = 'auth_user'

    # -------- 前缀&count模式 --------
    # ranges = [[4605577, 10], [4605588, 10] , [4605599, 10]]

    # -------- 单 IMSI range 模式 --------
    # start_prefix, end_prefix, count_per_prefix = 4605577, 4605588, 10
    # ranges = expand_prefix_range(start_prefix, end_prefix, count_per_prefix)
    # total_count = len(ranges) * count_per_prefix

    # -------- 多 IMSI range 模式 --------
    prefix_ranges = [(4605577, 4605579), (4605588, 4605590)]
    count_per_prefix = 1
    ranges = expand_multiple_prefix_ranges(prefix_ranges, count_per_prefix)
    total_count = len(ranges) * count_per_prefix
    print("总数：", total_count)

    output_file = generate_output_filename(base_dir, prefix, total_count)
    generate_csv_imsi_range(output_file, total_count, ranges)

    # -------- 指定总数，IMSI使用默认递增 --------
    # total_count = 30 # 可调整生成的数据总数
    # split_count = 50,000 # 可调整每个分割文件的数据条数
    # generate_csv_only_imsi_and_imei(output_file_A, total_count)

    # -------- 一号双所有字段数据 --------
    # generate_multisim_csv(output_file_A, total_count)

    # --------拆分已有的 CSV 文件 --------
    # split_csv(output_file_A, split_count)

import random
from datetime import datetime

def calculate_luhn_checksum(digits):
    """计算Luhn算法校验位"""
    total = 0
    is_even = True
    for digit in reversed(digits):
        digit = int(digit)
        if is_even:
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        total += digit
        is_even = not is_even
    return str((10 - (total % 10)) % 10)

def generate_imei(tac="35411617"):
    """生成IMEI号码"""
    # TAC部分（前8位）
    imei = tac
    
    # 序列号部分（6位）
    serial = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    imei += serial
    
    # 计算校验位
    checksum = calculate_luhn_checksum(imei)
    imei += checksum
    
    return imei

def calculate_eid_checksum(digits):
    """计算EID校验位 - 使用ISO/IEC 7812-1标准"""
    total = 0
    weight = 1
    for digit in reversed(digits):
        if digit.isdigit():
            product = int(digit) * (2 if weight % 2 == 0 else 1)
            total += (product // 10) + (product % 10)
        weight += 1
    return str((10 - (total % 10)) % 10)

def generate_eid(base_eid=850182675295848):
    """生成EID号码
    基准EID：34850182675295848000000000000000
    """
    # 先将base_eid转为字符串并添加18个0
    base_eid_str = str(base_eid) + "00000000000000000"
    base_eid_int = int(base_eid_str)
    
    # 计算模97
    y = base_eid_int % 97
    
    # 计算新的EID
    eid_new = 98 - y + base_eid_int
    
    return str(eid_new)

def generate_numbers(num=1, tac="35411617", base_eid=850182675295848):
    """生成指定数量的IMEI和EID号码
    :param num: 需要生成的号码数量
    :param tac: IMEI的TAC号码（8位）
    :param base_eid: EID的起始值
    """
    current_eid = base_eid  # 使用传入的base_eid作为起始值
    
    print(f"\n将生成 {num} 组IMEI和EID号码：\n")
    for i in range(num):
        imei = generate_imei(tac)
        eid = generate_eid(current_eid)
        print(f"第 {i+1} 组:")
        print(f"IMEI: {imei}")
        print(f"EID:  {eid}")
        print()
        current_eid += 100000000  # 每次增加这个值来生成下一个EID

if __name__ == "__main__":
    # 可以直接修改这里的参数来生成不同数量的号码
    generate_numbers(num=2, tac="35142438", base_eid=850182675295858) 
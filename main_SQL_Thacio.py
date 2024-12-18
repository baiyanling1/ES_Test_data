import mysql.connector

# 数据库连接
db = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="db_provision"
)

cursor = db.cursor()

# 插入语句
insert_query = """
INSERT INTO tbl_watch_subscription (
    imei, imsi, eid, iccid, msisdn, impu, impi, meid, display_name,
    primary_iccid, primary_imsi, primary_msisdn, primary_imei,
    activation_status, interface_type, application_category, selected_plan_id,
    device_id, activation_mode, device_type, device_vendor_name,
    service_type, provision_status, activate_code, smdp_address,
    iccid_status, is_pos, user_id, number_plan_type, create_at,
    update_at, start_time, end_time, iccid_profile_type,
    subscription_profile_id, original_activation_status, original_iccid_status,
    remove_reason, transaction_id
) VALUES (%s, %s, %s, %s, %s, NULL, NULL, %s, %s, %s, 
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
          %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# 生成并插入数据
try:
    # 假设从某个基值开始递增
    base_value = 862413040005136
    data_list = []

    for i in range(200000):  # 生成 20 万条记录
        imei = base_value + i
        imsi = 520053070000771 + i
        eid = f'348401826752948480000256{str(i).zfill(6)}'  # 根据需求生成 EID
        iccid = f'46055667897600000{str(i).zfill(2)}'  # 根据需求生成 ICCID
        msisdn = f'13800400770{i % 10}'  # 随机 MSISDN
        primary_iccid = f'4605566789760000{str(i + 1).zfill(2)}'
        primary_imsi = 520053070000769 + i
        primary_msisdn = msisdn
        primary_imei = imei + 1  # 让主 IMEI 递增

        # 向数据列表添加元组
        data_list.append((imei, imsi, eid, iccid, msisdn, 
                         primary_iccid, primary_imsi, primary_msisdn, primary_imei,
                         'Active', 'APPLE', 'GearSubscription', 
                         '{"basic-access-plan":"BaPlanA","insurance-plan":"InPlanB","roaming-plan":"RoPlanC"}',
                         1, 'Watch', 'Vendor A', 1, 'Provision-Completed', 
                         None, None, 'RELEASED', 'userA', 
                         1725000900053 + i, 1725000902273 + i, 
                         1725000902273 + i, 'my-profile-type', 
                         'RioProfile', 'New', 'ALLOCATED', 
                         '84c7750d10294cd0b6014660cc1e0fd5'))

        # 每1000条记录提交一次
        if len(data_list) >= 1000:
            cursor.executemany(insert_query, data_list)
            db.commit()  # 提交事务
            data_list.clear()  # 清空数据列表

    # 处理剩余的数据
    if data_list:
        cursor.executemany(insert_query, data_list)
        db.commit()

    print("Successfully inserted 200,000 records.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    db.close()

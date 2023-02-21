
import glob
import os
import pandas as pd

inputfile = str(os.path.dirname(os.getcwd())) + "/jmeter_csv/token失效/account-quth-sdk-expire*.csv"
print(inputfile)
outputfile = str(os.path.dirname(os.getcwd())) + "/jmeter_csv/token失效/account-quth-sdk-expire_all.csv"
csv_list = glob.glob(inputfile)
print(csv_list)
filepath = csv_list[0]
df = pd.read_csv(filepath)
df = df.to_csv(outputfile, index=False)

for i in range(1, len(csv_list)):
    filepath = csv_list[i]
    df = pd.read_csv(filepath)
    df = df.to_csv(outputfile, index=False, header=False, mode='a+')


# import pandas as pd
# import numpy as np
# #读取文件
# df1 = pd.read_csv("/Users/redtea/Desktop/中国移动ES/测试数据/jmeter_csv/token 有效/account-quth_apple1.csv")
# df2 = pd.read_csv("/Users/redtea/Desktop/中国移动ES/测试数据/jmeter_csv/token 有效/account-quth_apple2.csv")
# #合并
# df = pd.concat([df1,df2])
# df.drop_duplicates()  #数据去重
# #保存合并后的文件


# csv_list = glob.glob('/Users/redtea/Desktop/中国移动ES/测试数据/jmeter_csv/token 有效/account-quth_apple*.csv')
# print('共发现%s个CSV文件' % len(csv_list))
# print('正在处理............')
# for i in csv_list:
#     fr = open(i, 'r', encoding='utf-8').read()
#     with open('文件合集.csv', 'a', encoding='utf-8') as f:
#         f.write(fr)


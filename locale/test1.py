# -*- coding: utf-8 -*-

import json
import pandas as pd

data = [] # 用于存储每一行的Json数据
with open('temp.txt','r', encoding = 'UTF-8') as fr:
    for line in fr:
        j = json.loads(line)
        data.append(j)
print(data)
df = pd.DataFrame() # 最后转换得到的结果
for line in data:
    for i in line:
        df1 = pd.DataFrame([i])
        df = df.append(df1)

# 在excel表格的第1列写入, 不写入index
df.to_excel('data.xlsx', sheet_name='Data', startcol=0, index=False)

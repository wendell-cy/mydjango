import os
import pandas as pd

# 输入参数为excel表格所在目录
def to_one_excel(dir):
    dfs = []
    # 遍历文件目录，将所有表格表示为pandas中的DataFrame对象
    for root_dir, sub_dir, files in os.walk(r'' + dir):
        for file in files:
            if file.endswith('xls'):
                # 构造绝对路径
                file_name = os.path.join(root_dir, file)
                # print(file_name)
                df = pd.read_excel(file_name)
                dfs.append(df)
    # 行合并
    df_concated = pd.concat(dfs)
    # 按照name去重
    df_concated.drop_duplicates(keep='first', inplace=True)
    # 构造输出目录的绝对路径
    out_path = os.path.join(dir, 'res.xlsx')
    # 输出到excel表格中，并删除pandas默认的index列
    df_concated.to_excel(out_path, sheet_name='Sheet2', index=None)

# 调用并执行函数
to_one_excel('excel_dir')

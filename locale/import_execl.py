import xlrd
import xlwt
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch('192.168.3.201')


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('共耗时约 {:.2f} 秒'.format(time.time() - start))
        return res
    return wrapper

class ExcelData():
    def __init__(self, data_path, sheetname):
        self.data_path = data_path                                 # excle表格路径，需传入绝对路径
        self.sheetname = sheetname                                 # excle表格内sheet名
        self.data = xlrd.open_workbook(self.data_path)             # 打开excel表格
        self.table = self.data.sheet_by_name(self.sheetname)       # 切换到相应sheet
        self.keys = self.table.row_values(0)                       # 第一行作为key值
        self.rowNum = self.table.nrows                             # 获取表格行数
        self.colNum = self.table.ncols                             # 获取表格列数
        # print(self.rowNum)
        # print(self.colNum)

    def readExcel(self):
        if self.rowNum<2:
            print("excle内数据行数小于2")
        else:
            L = []                                                 #列表L存放取出的数据
            for i in range(1,self.rowNum):                         #从第二行（数据行）开始取数据
                sheet_data = {}                                    #定义一个字典用来存放对应数据
                for j in range(self.colNum):                       #j对应列值
                    sheet_data[self.keys[j]] = self.table.row_values(i)[j]    #把第i行第j列的值取出赋给第j列的键值，构成字典
                L.append(sheet_data)                               #一行值取完之后（一个字典），追加到L列表中
            #print(type(L))
            return L


@timer
def gen():
    """ 使用生成器批量写入数据 """
    action = ({
        "_index": "s2",
        "_type": "doc",
        "_source": {
            "title": i,
            "info": get_data.readExcel()[i]
        }
    } for i in range(len(get_data.readExcel())))
    helpers.bulk(es, action)
    # es.index(index='s2', doc_type='typeName', action, id=None)

def create_data():
    """ 写入数据 """
    for line in get_data.readExcel():
        es.index(index='s2', doc_type='doc', body={'title': line})


# wb = xlwt.Workbook()							# 打开一个excel文件，注意这里的Workbook，第一个W是大写
# ws = wb.add_sheet('Sheet1')
if __name__ == '__main__':
    data_path = "20201212.xls"  #文件的绝对路径
    sheetname = "Sheet1"
    get_data = ExcelData(data_path, sheetname)                       #定义get_data对象
    print(len(get_data.readExcel()))
    for i in range(len(get_data.readExcel())):
        print(get_data.readExcel()[i])
        break
    gen()
    #ws.write(get_data.readExcel())
    #wb.save("test.xlsx")
    # print(get_data.readExcel())


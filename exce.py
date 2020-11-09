'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 先将xls文件转成xlsx的文件，然后格式化数据，然后再将xlsx文件转成xls
Date: 2020-11-09 22:30:26
LastEditTime: 2020-11-09 23:53:28
'''
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import win32com.client as win32
# 转换文件格式

def xlsToxlsx(filename, format):
    if format == 51: # .xls-->.xlsx
        new_filename = "{}x".format(filename)
    elif format == 56: # .xlsx-->.xls
        new_filename = r"D:\learn\scripts\new_test.xls"
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    print(filename)
    wb = excel.Workbooks.Open(filename)
    print(new_filename)
    wb.SaveAs(new_filename, FileFormat = format, AccessMode=3)    
    wb.Close()                              
    excel.Application.Quit()




# 自动给excel表格修改行高
# 1.xlsx 的文件修改完成之后变成1_new.xlsx
def formatExcel(filename, filename2, height=12):
    wb = load_workbook(filename)
    for index, _ in enumerate(wb.sheetnames):
        ws = wb[wb.sheetnames[index]]
        for i in range(1, ws.max_row+1):
            ws.row_dimensions[i].height = height
    wb.save(filename2) 



if __name__ == '__main__':
    xlsToxlsx(r"D:\learn\scripts\1.xls", 51)
    formatExcel("1.xlsx", "new_1.xlsx")
    xlsToxlsx(r"D:\learn\scripts\new_1.xlsx", 56)
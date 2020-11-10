'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 先将xls文件转成xlsx的文件，然后格式化数据，然后再将xlsx文件转成xls
Date: 2020-11-09 22:30:26
LastEditTime: 2020-11-10 16:52:33
'''
import os
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string
import win32com.client as win32
# 转换文件格式

def xlsToxlsx(filename, formats):
    if formats == 51: # .xls-->.xlsx
        new_filename = "{}x".format(filename)
    elif formats == 56: # .xlsx-->.xls
        new_filename = r"D:\learn\scripts\new_test.xls"
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    print(filename)
    wb = excel.Workbooks.Open(filename)
    print(new_filename)
    wb.SaveAs(new_filename, FileFormat = formats)    
    wb.Close()                              
    excel.Application.Quit()


# 检查所有的单元格，如果存在时间的单元格记录对应的列
def checkDataFormat(ws):
    tmp_list = []
    for row  in ws.rows:
        for cell in row:
            if cell.value and cell.number_format == "[$-F800]dddd\,\ mmmm\ dd\,\ yyyy":
                # print("--->>> {}".format(get_column_letter(cell.column)))
                tmp_list.append(get_column_letter(cell.column))
                # print("--->>> {}".format(cell.number_format))
    return set(tmp_list)
# 自动给excel表格修改行高
# 1.xlsx 的文件修改完成之后变成1_new.xlsx
def formatExcel(filename, filename2, height=10, width=11):
    wb = load_workbook(filename)
    for index, _ in enumerate(wb.sheetnames):
        ws = wb[wb.sheetnames[index]]
        cdf = checkDataFormat(ws)
        # print('----->>>> {}'.format(ws['C5'].number_format))
        # print('----->>>> {}'.format(type(ws['C5'].number_format)))

            
        for i in range(1, ws.max_row+1):
            ws.row_dimensions[i].height = height

        for j in range(1, ws.max_column+1):
            # print('----->>>> {}'.format(sheets))
            for k in cdf:
                ws.column_dimensions[k].width = 12
            ws.column_dimensions[get_column_letter(j)].width = 8

    wb.save(filename2) 


if __name__ == '__main__':
    cur_path = os.getcwd()
    filename = os.path.join(cur_path, "1.xls")
    xlsToxlsx(filename, 51)
    formatExcel("1.xlsx", "new_1.xlsx", 10)
    # xlsToxlsx(r"D:\learn\scripts\new_1.xlsx", 56)
'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 先将xls文件转成xlsx的文件，然后格式化数据，然后再将xlsx文件转成xls
Date: 2020-11-09 22:30:26
LastEditTime: 2020-11-10 22:38:55
'''
import os
import sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string
import win32com.client as win32
import zipfile

# 解压zip


def unzip(filename):
    _, suffix = os.path.splitext(filename)
    if suffix == ".zip":
        with zipfile.ZipFile(filename) as zf:
            path, _ = os.path.split(filename)
            zf.extractall(path)

# 处理中文乱码的文件名


def changeFilename(path):
    for filename in os.listdir(path):
        # if os.path.isdir(os.path.join(path, filename)):
        try:
            zip_file = filename.encode('cp437').decode('gbk')
        except:
            zip_file = filename.encode('utf-8').decode('utf-8')
        if os.path.isdir(os.path.join(path, filename)):
            os.rename(os.path.join(path, filename),
                      os.path.join(path, zip_file))
            changeFilename(os.path.join(path, zip_file))
        else:
            os.rename(os.path.join(path, filename),
                      os.path.join(path, zip_file))


def get_files(path, file_list=[]):
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            get_files(os.path.join(path, file))
        else:
            _, suffix = os.path.splitext(os.path.join(path, file))
            if suffix == ".xls":
                file_list.append(os.path.join(path, file))

    return file_list


# 转换文件格式
def xlsToxlsx(filename, formats):
    if formats == 51:  # .xls-->.xlsx
        new_filename = "{}x".format(filename)
    elif formats == 56:  # .xlsx-->.xls
        pass
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(filename)
    wb.SaveAs(new_filename, FileFormat=formats)
    wb.Close()
    excel.Application.Quit()


# 检查所有的单元格，如果存在时间的单元格记录对应的列
def checkDataFormat(ws):
    tmp_list = []
    for row in ws.rows:
        for cell in row:
            if cell.value and cell.number_format == "[$-F800]dddd\,\ mmmm\ dd\,\ yyyy":
            # if cell.value and cell.number_format != "General":
                tmp_list.append(get_column_letter(cell.column))
    return set(tmp_list)


# 自动给excel表格修改行高
# 1.xlsx 的文件修改完成之后变成1_new.xlsx
def formatExcel(filename, filename2, height=10, width=11):
    wb = load_workbook(filename)
    for index, _ in enumerate(wb.sheetnames):
        ws = wb[wb.sheetnames[index]]
        cdf = checkDataFormat(ws)
        for i in range(1, ws.max_row+1):
            ws.row_dimensions[i].height = height
        for j in range(1, ws.max_column+1):
            for k in cdf:
                ws.column_dimensions[k].width = 12.0
            ws.column_dimensions[get_column_letter(j)].width = 10.0
    wb.save(filename2)


def main():
    for file_zip in os.listdir(os.getcwd()):
        filename_zip = os.path.join(os.getcwd(), file_zip)
        unzip(filename_zip)
    changeFilename(os.getcwd())
    for filename in get_files(os.getcwd()):
        xlsToxlsx(filename, 51)
        xlsxFileName = "{}x".format(filename)
        path, fname = os.path.split(xlsxFileName)
        tmpPath = path.split(os.sep)
        tmpPath.insert(3, "new")
        newPath = str(os.sep).join(tmpPath)
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        newXlsxFfileName = os.path.join(newPath, fname)
        formatExcel(xlsxFileName, newXlsxFfileName, 10)


if __name__ == '__main__':
    main()

'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 
Date: 2020-10-09 14:49:34
LastEditTime: 2020-10-09 15:51:44
'''
# coding:utf-8

'''
1.列出当前目录下的所有目录
2.判断目录中是否存在指定目录
3.存在写入success.csv
4.不存在写入fail.csv
'''
import os



def judge(path):
    success_list = []
    fail_list = []
    for dirs in  os.listdir(path):
        path2 = os.path.join(path, dirs)
        if os.path.isdir(path2):
            path2_dir = [i for i in os.listdir(path2)]
            if "rdt_log" in path2_dir:
                success_list.append(dirs)
            else:
                fail_list.append(dirs)
    return success_list, fail_list

def writeCSV(filename, data):
    data = set(data)
    with open(filename, "w") as f:
        for i in data:
            f.write("{}\n".format(i))    
            
if __name__ == '__main__':
    s,f = judge(r"Y:\log\20ww39r01\bkc_sop\bkc_sop-bkc20ww39r01-ts20WW39Thu_142627")
    writeCSV("s.csv", s)
    writeCSV("f.csv", f)
'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 
Date: 2020-10-09 14:49:34
LastEditTime: 2020-10-20 09:36:30
'''
# coding:utf-8

'''
1.列出当前目录下的所有目录
2.判断目录中是否存在指定目录
3.存在写入success.csv
'''
import os
import datetime
import shutil
import logging
import logging.config


logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

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

def copydir(sdir, ddir):
    if not os.path.exists(ddir):
        shutil.copytree(sdir, ddir)

def copyfile(sdir, ddir, filename):
    year = datetime.datetime.now().year
    for files in os.listdir(sdir):
        if os.path.isfile(os.path.join(sdir, files)) and str(year) in files:
            sfile = os.path.join(sdir, files)
            filename = '{}_{}'.format(filename, files)
            shutil.copyfile(sfile, os.path.join(ddir, filename))


def writeCSV(filename, success, fail):
    success = set(success)
    fail = set(fail)
    with open(filename, "w") as f:
        for i in success:
            f.write("{},success\n".format(i))    

if __name__ == '__main__':
    dirname = os.getcwd()
    week = dirname.split(os.sep)[3]
    newdirname = r'C:\sop\sop_to_manual\{}\execution'.format(week)
   
    if not os.path.exists(newdirname):
        os.mkdir(newdirname)
    
    s,f = judge(dirname)
    writeCSV("s.csv", s, f)
    logger.info("------------------- copying -----------")
    for i in s:
        sdir = os.path.join(dirname, i)
        ddir = os.path.join(newdirname, i)
        logger.info("copy {}    to   {}  ".format(sdir, ddir))
        copydir(sdir, ddir)
        copyfile(sdir, newdirname, i)
        
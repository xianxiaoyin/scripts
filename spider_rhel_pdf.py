# coding:utf-8
'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 后面需要改成多线程下载
Date: 2020-11-27 09:23:37
LastEditTime: 2020-12-03 11:37:46

pip install lxml requests
'''
import os
import sys
import time
import requests
from lxml import etree


def dirExist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def getUrlPdf(url, xpath):
    data = requests.get(url)
    tree = etree.HTML(data.text)
    result = tree.xpath(xpath)
    if result:
        return result
    else:
        print("未获取到url，请检查网页样式是否发生改变！")
        sys.exit()

def downLoadPdf(path, url):
    dirExist(path)
    if url:
        filename = os.path.split(url)[1]
        r = requests.get(url)
        with open(os.path.join(path,filename), 'wb') as f:
            f.write(r.content)
    else:
        print("获取到的url连接错误，请检查网页样式是否发生改变！")
        sys.exit()

if __name__ == '__main__':
    domain = r"https://access.redhat.com"
    rhel7 = "https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/"
    rhel8 = "https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/"
    for i in [rhel7, rhel8]:
        basepath =   '/'.join([os.getcwd(), rhel7.split("/")[-2]])
        dataDict = {}
        for i in getUrlPdf(i, '//*[@id="searchResults"]/div/div/h2/text() | //*[@id="searchResults"]/div/div/ul/li/div/ul/li[4]/a/@href'):
            if not i.endswith(".pdf"):
                key = i
                dataDict[key] = [] 
            else:
                dataDict[key].append(i)
        # 删除空数据
        for key in list(dataDict.keys()):
            if not dataDict.get(key):
                del dataDict[key]
        for k, v in dataDict.items():
            path =    os.path.join(basepath, k)
            print("正在下载的目录 --- >>> %s" %path)
            for u in  v:
                url = domain + u
                print("正在下载的文件 --- >>> %s" %url)
                downLoadPdf(path, url)
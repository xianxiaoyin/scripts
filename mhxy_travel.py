# -*- encoding: utf-8 -*-
'''
@File: 		   mhxy_travel.py
@Descripttion: 梦幻西游转服查询
@Date: 		   2022-03-13 09:32:58
@Author: 	   xianxiaoyin
'''
import requests


def getHtml(url) -> dict:
    html = requests.get(url)
    startIndex = html.text.index("=")
    return (eval(html.text[startIndex+1:]))


def main():
    while True:
        searchName = input("你正在使用的是【可转入服务器查询程序】请输入你要查询的服务器：[输入q/Q退出]")
        if searchName == "q" or searchName == "Q":
            break
        urlTravel = "http://xyq.163.com/2011/zhuanyi/js/travel_list.js"
        urlServer = "http://xyq.163.com/2011/zhuanyi/js/server_list.js"
        travelDict = getHtml(urlTravel)
        serverDict = getHtml(urlServer)
        tag = True
        for k, v in travelDict.items():
            if searchName in v:
                tag = False
                vList = [{serverDict[i]: i}for i in v]
                print("转出服务器--->{}".format(k))
                for j in vList:
                    print("                      转入服务器--->{0}:{1}".format(list(j.keys())[0], list(j.values())[0]))
        if tag:
            print("你查询的服务器，不能够转出到任何其他服务器中！")


if __name__ == "__main__":
    main()

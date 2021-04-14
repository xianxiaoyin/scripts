'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: ...
Date: 2021-04-07 10:59:23
LastEditTime: 2021-04-07 10:59:26
'''
import os
import argparse
import time

import requests


class Kuwo:
    def __init__(self, directory=None):
        self.directory = directory
        self.url = r'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord'
        self.hotUrl = r'http://www.kuwo.cn/api/www/bang/bang/bangMenu'
        self.bangurl = r'http://www.kuwo.cn/api/www/bang/bang/musicList'
        self.headers = {
            "Accept":
            "application/json, text/plain, */*",
            "Accept-Encoding":
            "gzip, deflate",
            "Accept-Language":
            "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "csrf":
            "32BSV9VN7MI",
            "Host":
            "www.kuwo.cn",
            "Proxy-Connection":
            "keep-alive",
            "Referer":
            "http://www.kuwo.cn/search/list?key=%E8%AE%B8%E5%B5%A9",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Cookie":
            "_ga=GA1.2.75061214.1605191230; _gid=GA1.2.10323238.1618403369; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1618403369; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1618403369; kw_token=32BSV9VN7MI"
        }
        self.session = requests.Session()
        self.proxies = {
            "http": "http://child-prc.intel.com:913",
            "https": "http://child-prc.intel.com:913",
        }

    def getRid(self, name):
        '''
        输入歌手名字
        获取歌曲的rid
        rid是歌曲的唯一id
        '''
        ridList = []
        params = {
            "key": "{}".format(name),
            "httpsStatus": "1",
            "reqId": "153f8970-9d1d-11eb-8c80-7d4c9ef72cd8",
            "pn": "1",
            "rn": "30"
        }

        html = self.session.get(self.url, params=params, headers=self.headers)
        data = html.json().get("data")
        for i in data.get("list"):
            ridList.append((i.get("rid"), i.get("name")))
        return ridList

    def getMp3(self, rids):
        '''
        获取歌曲的下载链接和歌曲名称
        '''
        print("正在检索下载链接，请等待······")
        mp3_url_list = []
        url1 = "http://www.kuwo.cn/url"
        for rid in rids:
            params = {
                "format": "mp3",
                "rid": "{}".format(rid[0]),
                "response": "url",
                "type": "convert_url3",
                "br": "128kmp3",
                "from": "web",
                "t": "1618299165629",
                "httpsStatus": "1",
                "reqId": "70956310-9c2a-11eb-9c19-d71d7b4a25fc"
            }
            html = self.session.get(url1, params=params, headers=self.headers)
            if html.status_code != 200:
                continue
            mp3_url_list.append((rid[1], html.json().get("url")))
        return mp3_url_list

    def downLoad(self, urls):
        ''' 
        下载歌曲 
        '''
        print("歌曲下载中······")
        for mp3_url in urls:
            msg_name = '正在下载的歌曲===>>> {}.mp3'.format(mp3_url[0])
            # msg_url = '正在下载的歌曲链接===>>> {}'.format(mp3_url[1])
            data = self.session.get(mp3_url[1])
            print(msg_name)
            # print(msg_url)
            name = '{}.mp3'.format(mp3_url[0].replace("(", "").replace(
                ")", '').replace("|", ""))
            namePath = os.path.join(self.directory,
                                    name) if self.directory else name
            with open(namePath, 'wb') as f:
                f.write(data.content)
            time.sleep(5)

    def getBangId(self):
        '''
        爬取排行榜歌曲
        http://www.kuwo.cn/api/www/bang/bang/bangMenu?httpsStatus=1&reqId=91f61fc0-9d21-11eb-8c80-7d4c9ef72cd8
        '''
        bangIdList = []
        params = {
            "httpsStatus": "1",
            "reqId": "91f61fc0-9d21-11eb-8c80-7d4c9ef72cd8"
        }

        data = self.session.get(url=self.hotUrl,
                                headers=self.headers,
                                params=params).json().get("data")
        for i in data:
            for j in i.get("list"):
                bangIdList.append(j.get("sourceid"))
        return bangIdList

    def getBangRid(self, bangIds):
        '''
            根据榜单id 获取榜单下面歌曲的rid
            http://www.kuwo.cn/api/www/bang/bang/musicList?bangId=242&pn=1&rn=30&httpsStatus=1&reqId=723bf400-9d23-11eb-8c80-7d4c9ef72cd8
        '''
        bangRidList = []
        for bangid in bangIds:
            print(bangid)
            params = {
                "bangId": "{}".format(bangid),
                "pn": "1",
                "rn": "30",
                "httpsStatus": "1",
                "reqId": "723bf400-9d23-11eb-8c80-7d4c9ef72cd8"
            }
            data = self.session.get(
                url=self.bangurl, params=params,
                headers=self.headers).json().get("data").get("musicList")
            for i in data:
                bangRidList.append((i.get("rid"), i.get("name")))
        return bangRidList


def main():
    parser = argparse.ArgumentParser(
        description='如果有输入就搜索输入内容并下载，如果没有输入就下载排行榜歌曲')
    parser.add_argument('-n', "--name", type=str, help="输入歌手名称或歌曲名")
    parser.add_argument('-d', "--dir", type=str, help="下载内容存放位置")
    args = parser.parse_args()
    if args.dir:
        kuwo = Kuwo(args.dir)
    else:
        kuwo = Kuwo()
    # 输入歌手和歌曲名称搜索下载
    if args.name:
        print("要下载的歌曲名或歌手名为： {}".format(args.name))
        rids = kuwo.getRid(args.name)
        urls = kuwo.getMp3(rids)
        kuwo.downLoad(urls)

    # 下载排行榜歌曲
    else:
        print("正在进行排行榜歌曲下载······ ")
        bangIds = kuwo.getBangId()
        bangRids = kuwo.getBangRid(bangIds)
        urls = kuwo.getMp3(bangRids)
        kuwo.downLoad(urls)


if __name__ == '__main__':
    main()
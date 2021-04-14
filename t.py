'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: ...
Date: 2021-04-07 10:59:23
LastEditTime: 2021-04-07 10:59:26
'''
import requests
import time

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "csrf": "MYYQXWUGGQS",
    "Host": "www.kuwo.cn",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://www.kuwo.cn/search/list?key=%E5%BC%A0%E7%A2%A7%E6%99%A8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Cookie": "_ga=GA1.2.11070868.1617867392; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1617867392,1617954498,1618282269; _gid=GA1.2.1492175435.1618282269; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1618301594; _gat=1; kw_token=MYYQXWUGGQS"





}



session = requests.Session()
# session.headers.update(headers)


def base(url, session, data_type="json", params=None):
    proxies = {
        "http": "http://child-prc.intel.com:913",
        "https": "http://child-prc.intel.com:913",
    }
    html = session.get(url, proxies=proxies, params=params, headers=headers)
    if data_type == 'json':
        return html.json()
    else:
        return html



def getHtml(url, session, name):
    ridList = []
    params = {
        "key": "{}".format(name),
        "httpsStatus": "1",
        "reqId": "fe318d50-9c27-11eb-9c19-d71d7b4a25fc"
    }
    
    html = base(url, session, params=params)
    data = html.get("data")
    
    for i in data.get("list"):
        ridList.append((i.get("rid"), i.get("name")))
    return ridList

def getMP3(url, session, name):
    mp3_url_list = []
    url1 = "http://www.kuwo.cn/url"
    for rid in getHtml(url, session, name):
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
        html = base(url1, session, params=params)
        mp3_url_list.append((rid[1], html.get("url")))
    return mp3_url_list


def download(url, session, name):
    proxies = {
        "http": "http://child-prc.intel.com:913",
        "https": "http://child-prc.intel.com:913",
    }
    mp3_urls = getMP3(url, session, name)
    for mp3_url in mp3_urls:
        msg_name = '正在下载的歌曲名称===>>> {}'.format(mp3_url[0])
        msg_url = '正在下载的歌曲链接===>>> {}'.format(mp3_url[1])
        data = requests.get(mp3_url[1],  proxies=proxies)
        print(msg_name)
        print(msg_url)
        name = '{}.mp3'.format(mp3_url[0])
        with open(name, 'wb') as f:
            f.write(data.content)
        time.sleep(5)

if __name__ == '__main__':
    name = input("请输入歌曲名字或歌手名：")
    url = r'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord'
    download(url, session, name)

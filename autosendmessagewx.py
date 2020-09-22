'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 
Date: 2020-09-21 09:14:53
LastEditTime: 2020-09-21 10:38:08
'''
# from __future__ import unicode_literals        #python3.x以上版本把改行注释即可
from threading import Timer
from wxpy import *
import requests
import json
'''
bot = Bot(cache_path=True)
# bot = Bot(console_qr=2,cache_path="botoo.pkl")   　　　　#这里的二维码是用像素的形式打印出来！，如果你在windows环境上运行，替换为  bot=Bot()


def get_news1():
    # 获取金山词霸每日一句，英文和翻译
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    contents = r.json()['content']
    translation = r.json()['translation']
    return contents, translation


def send_news():
    try:
        my_friend = bot.friends().search(u'周思维')[0]  # 你朋友的微信名称，可以是备注，不是微信帐号。
        my_friend.send(get_news1()[0])
        my_friend.send(u"测试测试，不要回复")
        t = Timer(10, send_news)  # 定时器 10秒钟执行一次
        t.start() 
    except:
        my_friend = bot.friends().search('无心')[0] # 你的微信名称，不是微信帐号。
        my_friend.send(u"今天消息发送失败了")


if __name__ == "__main__":
    send_news()

'''

bot=Bot(cache_path=True)

@bot.register() #接收从指定群发来的消息，发送者即recv_msg.sender为组
def recv_send_msg(recv_msg):
    print('收到的消息：',recv_msg.text)
    print('收到的消息：',recv_msg.sender.name)
    msg = '自动回复 {}'.format(recv_msg.text)
    print("这是返回信息", msg)
    return msg
    # 对指定人自动回复消息
    # if recv_msg.sender.name == u"周思维":
    #     msg = '{} ?'.format(recv_msg.text)
    #     print("这是返回信息", msg)
    #     return msg

if __name__ == "__main__":
    embed()
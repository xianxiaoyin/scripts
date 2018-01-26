# coding:utf8

'''
随机获取一个免费的ip代理地址
from agentpool import AgentPool
ips = AgentPool()
print(ips.get_agent())
>>>120.25.164.134:8118
'''


import requests
import random
from lxml import etree


class AgentPool(object):
    def __init__(self):
        self.url = 'https://www.kuaidaili.com/free/inha/{}/'.format(random.randint(0, 50))
        self.xpaths1 = '//*[@id="list"]/table/tbody/tr/td[1]'
        self.xpaths2 = '//*[@id="list"]/table/tbody/tr/td[2]'

    def get_agent(self):
        html = requests.get(self.url)
        context = etree.HTML(html.content)
        data = [i.text for i in context.xpath(self.xpaths1)]
        data2 = [i.text for i in context.xpath(self.xpaths2)]
        return ':'.join(random.choice(dict(zip(data, data2)).items()))


if __name__ == '__main__':
    pool = AgentPool()
    print(pool.get_agent())

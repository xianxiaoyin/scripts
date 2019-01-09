# coding:utf8

import psutil

def get_cpu_percent():
    pids = psutil.pids()
    n = 0
    numlist = []
    for pid in pids:
        p = psutil.Process(pid)
        if 'qemu-system' in p.name():
            print(p.name())
            while n < 50:
                numlist.append(p.cpu_percent(interval=1)/psutil.cpu_count(logical=True))
                n += 1
            print('{}'.format(sum(numlist)/len(numlist)))

try:
    get_cpu_percent()
except:
    print('test faild')





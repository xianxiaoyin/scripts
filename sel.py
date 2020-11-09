'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 
Date: 2020-10-24 10:14:59
LastEditTime: 2020-10-25 19:12:05

http://vls3.zzu.edu.cn/

http://123.15.57.120/vls2s/vls3isapi.dll/getmain?ptopid=C8F10FBBF71B425196F6586A040812FB
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import time

browser = webdriver.Ie(executable_path="./IEDriverServer.exe")

# browser.get("http://www.baidu.com")
browser.get("http://vls3.zzu.edu.cn/")
browser.implicitly_wait(60) 
browser.find_element_by_name("uid").clear()
browser.find_element_by_name("uid").send_keys("19103522010")
browser.find_element_by_name("pw").clear()
browser.find_element_by_name("pw").send_keys("19920410")
browser.find_element_by_name("B1").click()
browser.find_element_by_name("gointo").click()
browser.switch_to.frame("content")
tag_a = browser.find_elements_by_xpath("//table/tbody/tr[2]/td/p/a")
actions = ActionChains(browser)
print("=================")
for i in tag_a: 
    if i.text == "财务分析<网上考试>":
        i.click()
        tag_b = browser.find_elements_by_xpath("//table/tbody/tr[3]/td[1]/a")
        for j in tag_b:
            if j.text == "课件学习":
                j.click()
                tag_c = browser.find_elements_by_xpath("//table/tbody/tr/td/a")
                for g in tag_c:
                    g.click()
                    tag_d = browser.find_elements_by_xpath("//table/tbody/tr[11]/td[2]/p/a")
                    print(tag_d)
                    for k in tag_d:
                        actions.context_click(k)
                        actions.perform()
                        time.sleep(3)
                        pyautogui.typewrite(['down'])
                        pyautogui.typewrite(['enter'])
                        time.sleep(5)
                        browser.find_element_by_name("return6").click()
                        print("------------------")

                
time.sleep(30)
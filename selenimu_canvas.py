from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
tag = True
capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = {'browser': 'ALL'}
options = Options()
options.add_experimental_option('w3c', False)

browser = webdriver.Chrome("./chromedriver.exe",desired_capabilities=capabilities, chrome_options=options)
browser.maximize_window()
browser.get(
    r'https://files.unity3d.com/marcot/benchmarks2018.2.5f1/?_ga=2.581733866.1204451712.1603392192-1393365139.1598485611'
)

browser.implicitly_wait(60)
canvas_element = browser.find_element_by_id('#canvas')
while tag:
    for i in browser.get_log("browser"):
        print(i["message"])
        if "Stabilizing" in i["message"]:
            ActionChains(browser).move_to_element_with_offset(canvas_element, 610, 610).click().perform()

        if "Overall" in i["message"]:
            print(i["message"])
            tag = False
browser.close()


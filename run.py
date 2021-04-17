import requests
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time
import jiexi_data 

url = "https://detail.tmall.com/item.htm?id=%s"

searchListUrl = "https://s.taobao.com/search?q=灯具&s="

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
}


def ChangeCookies(driver,headers):
    # oldCookies = headers['cookie']
    # cookiesDictList = list()
    # for i in oldCookies.split(';'):
    #     iSplit = i.split('=')
    #     cookiesDictList.append({"name": iSplit[0].strip(), "value": iSplit[1]})
    # driver.get("https://www.baidu.com")
    # for cookie in cookiesDictList:
    #     driver.add_cookie(cookie)
    driver.get(searchListUrl+str(44*0))
    input("验证后，退出登录，按回车继续。")
    Cookies = driver.get_cookies()
    newCookies = ''
    for i in Cookies:
        newCookies += i['name']+'='+i['value']+';'
    headers['cookie'] = newCookies
    return headers


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")  # 配置隐私模式
# 减少打印
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)
driver.maximize_window()
with open('stealth.min.js') as f:
    js = f.read()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})

headers=ChangeCookies(driver,headers)

InfoList = list()
for i in range(0, 1):
    r = requests.get(searchListUrl+str(44*i), headers=headers)
    try:
        d = json.loads(re.findall(r"g_page_config = (.+?);\n", r.text)[0])
    except Exception as e:
        print(e)
        if("验证码" in r.text):
            # 更换cookies
            headers = ChangeCookies(driver,headers)
        else:
            with open("%s.html" % time.time(), "w") as f:
                f.write(r.text)
            break
    InfoList.append(d)
    print(44*i, len(InfoList))


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
}
idList = list()
for d in InfoList:
    for u in d['mods']['itemlist']['data']['auctions']:
        idList.append(u["nid"])

# 去重
idSet=list(set(idList))

for nid in idList:
    jiexi_data.jiexi_ziye_data(url % nid)
    # r = requests.get(url % nid, headers=headers)
    # soup = BeautifulSoup(r.text, 'lxml')
    # title = soup.select('h1')[1].text.strip()
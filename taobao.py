from selenium import webdriver
import time
import csv
import os
import re
import random


def search_product(key):
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="q"]').send_keys(key)
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(25)
    driver.implicitly_wait(10)
    drop_down(driver)
    #token = 100  # int(re.findall(r'\d+', token)[0])
    time.sleep(25)
#点击搜索

def next_page(key):
    token = 100
    num = 0
    while num != token - 1:
        driver.get('https://s.taobao.com/search?q={}&s={}'.format(key, 44 * num))
        driver.implicitly_wait(10)
        drop_down(driver)
        html = driver.page_source
        url_list = re.findall('href=\"(.*?)"', html)
        url_all=[]
        for url in url_list:
            if "detail" in url:
                url_all.append(url)
        for url_detail in set(url_all):
            start_url = 'http:'
            url_detail = "".join([start_url, url_detail])
            jiexi_data.jiexi_ziye_data(url_detail)
            num += 1


def drop_down(driver_used):
    time.sleep(random.randint(2, 6))
    driver_used.implicitly_wait(5)
    for x in range(1, 12, 2):
        time.sleep(1)
        j = x / 10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver_used.execute_script(js)
#下拉至底

def login(key):
    driver.maximize_window()
    driver.get('https://www.taobao.com')#https://login.taobao.com/member/login.jhtml
    search_product(key)
    next_page(key)

#谷歌打开登陆网页

def get_data():#改下下面的内容去获取淘宝子页的数据
    driver.implicitly_wait(5)
    data_list_total = []
    divs = driver.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
    for div in divs:
        shangpinName = div.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text
        Price = div.find_element_by_xpath('.//strong').text
        persons = div.find_element_by_xpath('.//div[@class="deal-cnt"]').text
        shop = div.find_element_by_xpath('.//div[@class="shop"]/a').text
        driver.implicitly_wait(2)
        img = div.find_element_by_xpath('.//*[@class="pic"]/a/img').get_attribute('src')
        data_list = [shop, shangpinName, Price, persons, img]
        data_list_total.append(data_list)
        # print(shangpinName, Price, persons, shop, img, sep='|')
    return data_list_total


# def save_data(key, page_number):
#     data_list_total = get_data()
#     csvFile = open(r'E:\taobao_data\{}\第{}页.csv'.format(key, page_number), 'w')
#     try:
#         writer = csv.writer(csvFile)
#         for i in data_list_total:
#             writer.writerow(i)
#     finally:
#         csvFile.close()


def start():
    keywords = input("请输入要搜索的商品名称：")
    login(keywords)
    next_page(keywords)
#开始

def mkdir(keywords):
    os.mkdir(r'E:\taobao_data\{}'.format(keywords))


# def mkscv_savedata(keywords, page_number):
#     if os.path.exists(r'E:\taobao_data\{}'.format(keywords)):
#         save_data(keywords, page_number)
#     else:
#         mkdir(keywords)
#         save_data(keywords, page_number)


if __name__ == '__main__':
    # 加启动配置
    option = webdriver.ChromeOptions()
    option.add_argument(r'--user-data-dir=C:\Users\Liu\AppData\Local\Google\Chrome\User Data')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    prefs = {
        'profile.default_content_setting_values': {
            'notifications':2
        }
    }
    option.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=option)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
    })
    start()

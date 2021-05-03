# -- coding: utf-8 --
from selenium import webdriver
from taobao import drop_down
import time
import json
from bs4 import BeautifulSoup
import requests
import re
import json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}


def jiexi_ziye_data(url, xiaoliang):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    # option = webdriver.ChromeOptions()
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # # 无头模式
    # option.add_argument('--headless')
    # driver = webdriver.Chrome(options=option)
    # driver.get(url)
    # driver.implicitly_wait(5)
    # drop_down(driver)
    try:
        #正则匹配js内容
        d = json.loads(re.findall(r"TShop.Setup\(\r\n([\s\S]*)\);[\s\S]*}\)\(\);", r.text)[0])
    except:
        print("正则匹配失败")
    try:
        shop_name = soup.select("#shopExtra > div.slogo > a > strong")[0].text
        # if driver.find_element_by_xpath('//*[@id="shopExtra"]/div[1]/a/strong').text:
        #     shop_name = driver.find_element_by_xpath(
        #         '//*[@id="shopExtra"]/div[1]/a/strong').text
    except:
        shop_name = -1
    try:
        shop_introduction = soup.select(
            "#J_DetailMeta > div.tm-clear > div.tb-property > div > div.tb-detail-hd > h1")[0].text.strip()
        # if driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/div/h1').text:
        #     shop_introduction = driver.find_element_by_xpath(
        #         '/html/body/div/div/div/div/div/div/div/div/h1').text
    except:
        shop_introduction = -1
    try:
        price = d['detail']['defaultItemPrice']
        # if driver.find_element_by_id("J_StrPriceModBox"):
        #     price = driver.find_element_by_id("J_StrPriceModBox").text
    except:
        price = -1
    # 销量使用别的浏览器无法打开，需要在已登录的浏览器中进行打开
    # if driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/ul/li/div/span').text:
    #     xiaoliang = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/ul/li/div/span').text
    # else:
    #     xiaoliang = -1
    try:
        pinpaimingcheng = d['itemDO']['brand']
    except:
        pinpaimingcheng = -1
    try:
        # if driver.find_element_by_xpath('//*[@id="shop-info"]/div[2]/div[1]/div[2]/span'):
        #     star = driver.find_element_by_xpath(
        #         '//*[@id="shop-info"]/div[2]/div[1]/div[2]/span').text
        star=soup.select("#shop-info > div.main-info > div:nth-child(1) > div.shopdsr-score.shopdsr-score-up-ctrl > span")[0].text
    except:
        star = -1
    # url = driver.current_url
    try:
        # parent_elem = driver.find_element_by_xpath('//*[@id="J_AttrUL"]')
        # child_elements = parent_elem.find_elements_by_xpath('.//*')
        attr=soup.select("#J_AttrUL")[0].text.split("\n")
        attrDict = dict()
        for content in attr:
            try:
                content=content.replace("：",":",1) 
                cList = content.split(":")
                attrDict[cList[0].strip()] = cList[1].strip()
                print(content)
            except:
                continue
    except:
        attrDict = dict()

    imgs=d['propertyPics']['default']

    d = dict()
    d['shop_name'] = shop_name
    d['pinpaimingcheng'] = pinpaimingcheng
    d['shop_introduction'] = shop_introduction
    d['price'] = price
    d['xiaoliang'] = xiaoliang
    d['star'] = star
    d['url'] = url
    d['pic'] = list()
    d['attr'] = attrDict
    print('店铺名称：', shop_name)
    print('品牌名称：', pinpaimingcheng)
    print('商品介绍：', shop_introduction)
    print('价格：', price)
    print('月销量：', xiaoliang)
    print('评分：', star)
    print('当前的url是：', url)
    
    for link in imgs:
        print(link)
        d['pic'].append(link)
    # with open("data/%s.json" % url.split('=')[-1], "w+") as f:
    #     json.dump(d, f)
  #  driver.quit()
    return d


if __name__ == "__main__":
    r=jiexi_ziye_data("https://detail.tmall.com/item.htm?id=639067225502", 1)
    input()

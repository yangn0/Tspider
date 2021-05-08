# -- coding: utf-8 --
from selenium import webdriver
from taobao import drop_down
import time
import json
from bs4 import BeautifulSoup
import requests
import re
import json
# cookie: enc=GdOTDNECvJaRqqd29tQam3aJoaihX%2FmgOF7pzQVVFoDpPFpgfOlh%2BjeZNOKqYgKw7Bq3R4A9bkbKSDpYX9q609nazbizbTM1f8QdogbXEmU%3D; cna=oXxxGKIoXEACATwIxdIxAiGC; cq=ccp%3D1; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E8%B7%AF%E4%BB%94%E4%BB%94%E5%95%86%E8%B4%B8%E5%BA%97; xlly_s=1; t=e43e658815f685d87d603367dbb1aa85; _tb_token_=39365bb1e50e4; cookie2=17cbdb3c6d89ab9b1ac76d1f29be6e1b; pnm_cku822=098%23E1hvzvvUvbpvUvCkvvvvvjiWPFsh1ji2RsM9gjivPmP9AjiPR2SpljlnPLF9tji2i9hvCvvvpZpgvpvhvvCvpvvCvvOv9hCvvvmgvpvIvvCvpvvvvvvvvhXVvvvCJpvvByOvvUhQvvCVB9vv9BQvvhXVvvmCjU9CvvOCvhE2tWmIvpvUvvCCRnFUqSQUvpCWvL1BZBzv5fVQKoZH0R9t%2BFuTWDAvD40OdigDN%2BBlDBh1n7ERiNoOVXkfwxzXSfpAhC3qVUcn%2B3mfjLEc6aZtn1mAVAElYEkJ5igDN9gCvvpvvPMM; tfstk=cXuOBOiSgpvihCVKacKHlMNAx3oAat1Tn1wAkCGa7a5MQ1bVosAqr4n7qhNVBydd.; l=eBSeKDVVjaNjzW5zBO5Zlurza77tBIdb8sPzaNbMiInca6KRsFa4-NCCHooH-dtjgtfFue-yAqdWaRFH7faLRE1Jn0cNKXIpB1v9-; isg=BGhozjL-nJusR7CnNL9k-KqDOVZ6kcybPigSqiKYQuPWfQnnyaIsKxH_cRWNzYRz

headers = '''authority: detail.tmall.com
method: GET
path: /item.htm?id=628376593702
scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8
cache-control: no-cache
pragma: no-cache
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"
sec-ch-ua-mobile: ?0
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36
'''
# headers转换


def trans(s):
    d = dict()
    s = s.split("\n")
    for i in s:
        if(i == ''):
            continue
        if(i[0] == ":"):
            i = i[1:]
        d[i.split(': ')[0]] = i.split(': ')[1]
    return d


def jiexi_ziye_data_se(url, xiaoliang):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 无头模式
    option.add_argument('--headless')
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    driver.implicitly_wait(5)
    drop_down(driver)
    try:
        shop_name = driver.find_element_by_xpath(
            '//*[@id="shopExtra"]/div[1]/a/strong').text
    except:
        try:
            shop_name = driver.find_element_by_css_selector(
                '.tb-shop-name').text
        except:
            try:
                shop_name = driver.find_element_by_css_selector(
                'div.shop-name > div.shop-name-wrap > a').text 
            except:
                shop_name = -1
    try:
        if driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/div/h1').text:
            shop_introduction = driver.find_element_by_xpath(
                '/html/body/div/div/div/div/div/div/div/div/h1').text
    except:
        try:
            shop_introduction = driver.find_element_by_css_selector(
                '.tb-main-title').text
        except:
            shop_introduction = -1
    try:
        if driver.find_element_by_id("J_StrPriceModBox"):
            price = driver.find_element_by_id("J_StrPriceModBox").text
    except:
        price = -1
    # 销量使用别的浏览器无法打开，需要在已登录的浏览器中进行打开
    # if driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/ul/li/div/span').text:
    #     xiaoliang = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/ul/li/div/span').text
    # else:
    #     xiaoliang = -1
    # try:
    #     if driver.find_element_by_id('J_BrandAttr'):
    #         pinpaimingcheng = driver.find_element_by_id('J_BrandAttr').text
    # except:
    #     pinpaimingcheng = -1
    try:
        if driver.find_element_by_xpath('//*[@id="shop-info"]/div[2]/div[1]/div[2]/span'):
            star = driver.find_element_by_xpath(
                '//*[@id="shop-info"]/div[2]/div[1]/div[2]/span').text
    except:
        try:
            star = driver.find_element_by_css_selector(
                '.tb-shop-rate > dl:nth-child(1) > dd > a').text
        except:
            try:
                star = driver.find_element_by_css_selector(
                    'div.shop-service-info > ul > li:nth-child(1) > span.rateinfo > em').text
            except:
                star = -1
    # url = driver.current_url
    attrDict = dict()
    try:
        parent_elem = driver.find_element_by_xpath('//*[@id="J_AttrUL"]')
        child_elements = parent_elem.find_elements_by_xpath('.//*')
        for conent in child_elements:
            cList = conent.text.split("：")
            attrDict[cList[0]] = cList[1]
            print(conent.text)
    except:
        try:
            parent_elem = driver.find_elements_by_css_selector('.attributes-list li')
            for conent in parent_elem:
                content = content.replace("：", ":", 1)
                cList = conent.text.split(":")
                attrDict[cList[0]] = cList[1]
                print(conent.text)
        except:
            pass
    d = dict()
    d['shop_name'] = shop_name
    # d['pinpaimingcheng'] = pinpaimingcheng
    d['shop_introduction'] = shop_introduction
    d['price'] = price
    d['xiaoliang'] = xiaoliang
    d['star'] = star
    d['url'] = url
    d['pic'] = list()
    d['attr'] = attrDict
    print('店铺名称：', shop_name)
    # print('品牌名称：', pinpaimingcheng)
    print('商品介绍：', shop_introduction)
    print('价格：', price)
    print('月销量：', xiaoliang)
    print('评分：', star)
    print('当前的url是：', url)
    try:
        imgs=driver.find_elements_by_xpath("//*[@alt='商品预览图']")
        if len(imgs)==0:
            raise
        for link in driver.find_elements_by_xpath("//*[@alt='商品预览图']"):
            smpicUrl = link.get_attribute('src')
            bigPicUrl = smpicUrl.replace('60x60q90', '430x430q90')
            print(bigPicUrl)
            d['pic'].append(bigPicUrl)
    except:
        try:
            imgs=driver.find_elements_by_css_selector('#J_UlThumb > li img')
            if len(imgs)==0:
                raise
            for link in driver.find_elements_by_css_selector('#J_UlThumb > li img'):
                smpicUrl = link.get_attribute('src')
                bigPicUrl = smpicUrl.replace('50x50', '430x430')
                print(bigPicUrl)
                d['pic'].append(bigPicUrl)
        except:
            d['pic']=[]
    # with open("data/%s.json" % url.split('=')[-1], "w+") as f:
    #     json.dump(d, f)
    driver.quit()
    return d


def jiexi_ziye_data(url, xiaoliang):
    r = requests.get(url, headers=trans(headers))
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
        # 正则匹配js内容
        d = json.loads(re.findall(
            r"TShop.Setup\(\r\n([\s\S]*)\);[\s\S]*}\)\(\);", r.text)[0])
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
        star = soup.select(
            "#shop-info > div.main-info > div:nth-child(1) > div.shopdsr-score > span")[0].text
    except:
        star = -1
    # url = driver.current_url
    try:
        # parent_elem = driver.find_element_by_xpath('//*[@id="J_AttrUL"]')
        # child_elements = parent_elem.find_elements_by_xpath('.//*')
        attr = soup.select("#J_AttrUL")[0].text.split("\n")
        attrDict = dict()
        for content in attr:
            try:
                content = content.replace("：", ":", 1)
                cList = content.split(":")
                attrDict[cList[0].strip()] = cList[1].strip()
                print(content)
            except:
                continue
    except:
        attrDict = dict()

    imgs = d['propertyPics']['default']

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
        d['pic'].append("http:"+link)
    # with open("data/%s.json" % url.split('=')[-1], "w+") as f:
    #     json.dump(d, f)
  #  driver.quit()
    return d


if __name__ == "__main__":
    r = jiexi_ziye_data_se(
        "https://detail.tmall.com/item.htm?id=573481226938", 1)
    input()

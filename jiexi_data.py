# -- coding: utf-8 --
from selenium import webdriver
from taobao import drop_down
import time,json


def jiexi_ziye_data(url):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    driver.implicitly_wait(5)
    drop_down(driver)
    try:
        if driver.find_element_by_xpath('//*[@id="shopExtra"]/div[1]/a/strong').text:
            shop_name = driver.find_element_by_xpath('//*[@id="shopExtra"]/div[1]/a/strong').text
    except :
        shop_name = -1
    try:
        if driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/div/h1').text:
            shop_introduction = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/div/h1').text
    except :
        shop_introduction = -1
    try:
        if driver.find_element_by_id("J_StrPriceModBox"):
            price = driver.find_element_by_id("J_StrPriceModBox").text
    except :
        price = -1
    #销量使用别的浏览器无法打开，需要在已登录的浏览器中进行打开
    # if driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/ul/li/div/span').text:
    #     xiaoliang = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/ul/li/div/span').text
    # else:
    #     xiaoliang = -1
    try:
        if driver.find_element_by_id('J_BrandAttr'):
            pinpaimingcheng = driver.find_element_by_id('J_BrandAttr').text
    except :
        pinpaimingcheng = -1
    try:
        if driver.find_element_by_xpath('//*[@id="shop-info"]/div[2]/div[1]/div[2]/span'):
            star = driver.find_element_by_xpath('//*[@id="shop-info"]/div[2]/div[1]/div[2]/span').text
    except :
        star = -1
    url = driver.current_url
    try:
        parent_elem = driver.find_element_by_xpath('//*[@id="J_AttrUL"]')
        child_elements = parent_elem.find_elements_by_xpath('.//*')
        for conent in child_elements:
            print(conent.text)
    except :
        pass
    d=dict()
    d['shop_name']=shop_name
    d['pinpaimingcheng']=pinpaimingcheng
    d['shop_introduction']=shop_introduction
    d['price']=price
    d['star']=star
    d['url']=url
    d['pic']=list()
    print('店铺名称：', shop_name)
    print('品牌名称：', pinpaimingcheng)
    print('商品介绍：', shop_introduction)
    print('价格：', price)
    #print('月销量：', xiaoliang)
    print('评分：', star)
    print('当前的url是：', url)
    for link in driver.find_elements_by_xpath("//*[@alt='商品预览图']"):
        smpicUrl=link.get_attribute('src')
        bigPicUrl=smpicUrl.replace('60x60q90','430x430q90')
        print(bigPicUrl)
        d['pic'].append(bigPicUrl)
    with open("data/%s.json"%url.split('=')[1],"w+") as f:
        json.dump(d,f)

    driver.quit()


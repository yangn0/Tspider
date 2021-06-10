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
from xpinyin import Pinyin
import os
import datetime
import csv
import dingRobot
import traceback
import manager
import multiprocessing
from multiprocessing import Pool,Lock


def mk_dir_file(name, PcNum, path='D:\\goods'):

    year = str(datetime.datetime.now().year)
    if datetime.datetime.now().month < 10:
        month = '0'+str(datetime.datetime.now().month)
    else:
        month = str(datetime.datetime.now().month)
    if datetime.datetime.now().day < 10:
        day = '0'+str(datetime.datetime.now().day)
    else:
        day = str(datetime.datetime.now().day)
    if not os.path.exists(os.path.join(path, year)):
        year_path = os.path.join(path, year)
        os.makedirs(year_path)
        path = os.path.join(path, year)
    else:
        path = os.path.join(path, year)
    if not os.path.exists(os.path.join(path, month)):
        month_path = os.path.join(path, month)
        os.makedirs(month_path)
        path = os.path.join(path, month)
    else:
        path = os.path.join(path, month)
    if not os.path.exists(os.path.join(path, day)):
        day_path = os.path.join(path, day)
        os.makedirs(day_path)
        path = os.path.join(path, day)
    else:
        path = os.path.join(path, day)
    p = Pinyin()
    # path_taobao = str(PcNum)+'_pdd_'+p.get_pinyin(name, '')+int(time.time()*100)
    # if not os.path.exists(os.path.join(path, path_pdd)):
    #     path_pdd = os.path.join(path, path_pdd)
    #     os.makedirs(path_pdd)
    #     path = os.path.join(path, path_pdd)
    # else:
    #     path = os.path.join(path, path_pdd) #如果没有这个path则直接创建
    path = os.path.join(path, "%s_%s_%s_%s.csv" %
                        (pcNum, "tb", p.get_pinyin(name, ""), day))
    return path


def ChangeCookies(driver, headers):
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
    headers["user-agent"] =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
    return headers




def worker_one(n,nid,idsalesDict,lock,dir_path,csv_path,pcNum,searchName,searchNameNum):
    url = "https://detail.tmall.com/item.htm?id=%s"
    print(n,nid)
    
    searchNameErrorNum=0
    whileFlag = 3
    while(1):
        try:
            data = jiexi_data.jiexi_ziye_data_se(
                url % nid, idsalesDict[nid])
            whileFlag -= 1
            if len(data['pic']) == 0:
                if whileFlag <= 0:
                    print("whileFlag<=0 again", url % nid)
                    break
                continue
            break
        except:
            traceback.print_exc()
            print("again%s" % whileFlag, url % nid)
            whileFlag -= 1
            time.sleep(1)
            if whileFlag <= 0:
                lock.acquire()
                searchNameErrorNum += 1
                with open("error.log", "a") as f:
                    f.write(str(datetime.datetime.now()) +
                            " "+url % nid+"\n")
                lock.release()
                break
            continue
    if whileFlag <= 0:
        return
    # 保存图片
    data['pic_path'] = list()
    data["goodId"] = nid
    try:
        lock.acquire()
        if not os.path.exists(os.path.join(dir_path, data["goodId"])):
            os.mkdir(os.path.join(dir_path, data["goodId"]))
        lock.release()
    except:
        return
    pic_path = os.path.join(dir_path, data["goodId"])
    for count, pic in enumerate(data['pic']):
        count += 1
        while(1):
            try:
                imageText = 'img_none'
                image = requests.get(pic)
                imageText = image.text
                f = open(os.path.join(
                    pic_path, str(count)+'.jpg'), 'wb')
                # 将下载到的图片数据写入文件
                f.write(image.content)
                f.close()
                data['pic_path'].append(os.path.join(
                    pic_path, str(count)+'.jpg').split('\\', 1)[1])
                break
            except Exception as e:
                print(repr(e))
                print(imageText)
                continue
    lock.acquire()
    # 保存
    searchNameNum.set(searchNameNum.get()+1)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["淘宝", data["goodId"], data['shop_name'], data['shop_introduction'], data['price'],
                        data['xiaoliang'], data['star'], data['url'], json.dumps(data['pic']), json.dumps(data['pic_path']), json.dumps(data['attr'], ensure_ascii=False)])
    with open(dir_path+'record_finish_list.txt', 'a') as f:
                f.writelines(nid+'\n')
    # 更新管理系统状态
    manager.postStatus({
        "pcNum": pcNum,
        "nowPage": searchNameNum.get(),
        "nowKeyword":searchName ,
        "lastTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
        "lastId": data["goodId"]
    })
    lock.release()

def searchWorker(searchName,searchPage,pcNum,searchNameNum):
    searchNameErrorNum = 0

    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    }
    dingRobot.sendText(str(datetime.datetime.now()) +
                        " 机器号：%s 淘宝 正在爬取关键字:%s" % (pcNum, searchName))
    csv_path = mk_dir_file(searchName, pcNum,)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["网站来源", "商品ID", "店铺名称", "商品名称", "价格",
                            "销量", "评分", "url", "picUrl", "图片本地path", "属性"])

    dir_path = os.path.dirname(csv_path)
    InfoList = list()
    for i in range(0, searchPage):
        while(1):
            try:
                r = requests.get(searchListUrl+str(44*i), headers=headers)
                d = json.loads(re.findall(
                    r"g_page_config = (.+?);\n", r.text)[0])
                break
            except Exception as e:
                print(e)
                if("验证码" in r.text):
                    # 更换cookies
                    dingRobot.sendText(
                        str(datetime.datetime.now())+"机器号：%s 淘宝 验证码" % pcNum)
                    headers = ChangeCookies(driver, headers)
                    continue
                else:
                    with open("error-%s-%s.html" % (searchName, time.time()), "w", encoding="utf-8") as f:
                        f.write(r.text)
                    continue
        InfoList.append(d)
        print(44*i, len(InfoList))
    

    # 商品子页

    idsalesDict = dict()
    #salesList = list()
    for d in InfoList:
        try:
            for u in d['mods']['itemlist']['data']['auctions']:
                idsalesDict[u["nid"]] = u['view_sales']
                # idList.append(u["nid"])
                # salesList.append(u['view_sales'])
        except:
            continue

    # 去重
    # idSet = list(set(idList))
    lock = multiprocessing.Manager().Lock()
    
    p = Pool(5)
    for n, nid in enumerate(idsalesDict):
        lock.acquire()
        # 记录当前运行爬虫的
        if os.path.exists(dir_path+'record_finish_list.txt'):
            #print("查找断点")
            with open(dir_path+'record_finish_list.txt','r') as f:
                if nid in f.read():
                    lock.release()
                    continue
        lock.release()
        mang=manager.getPauseAndGoOn(pcNum)
        if mang==-1:
            print("停止")
            return -1
        p.apply_async(worker_one, args = (n,nid,idsalesDict,lock,dir_path,csv_path,pcNum,searchName,searchNameNum,))
    p.close()  
    p.join()  
    
    dingRobot.sendText(str(datetime.datetime.now())+" 机器号：%s 淘宝 关键字:%s爬取完成 成功%s条 失败%s条" %
                        (pcNum, searchName, searchNameNum.get(), searchNameErrorNum))

if __name__ == "__main__":
    pcNum = "yn"  # 机器号

    
    searchNameNum = multiprocessing.Manager().Value(int, 0)

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
    # 珠宝
    # searchNameList = [
    #     "黄金项链", "黄金吊坠 ", "黄金转运珠", "黄金戒指", "黄金手镯", "黄金手链脚链", "黄金耳饰", "钻戒", "钻石项链吊坠", "钻石手镯手链", "钻石耳饰", "裸钻", "彩宝", "K金吊坠", "K金项链", "K金戒指", "K金手镯手链脚链", "K金耳饰", "铂金 ", "翡翠手镯",
    #     "翡翠吊坠", "翡翠耳饰", "和田玉吊坠", "和田玉手链", "和田玉戒指", "珍珠项链 ", "珍珠手链", "珍珠耳饰", "珍珠戒指",
    #     "水晶玛瑙手链", "水晶玛瑙项链", "水晶玛瑙耳饰", "水晶玛瑙戒指", "银手镯", "银项链", "银手链", "银戒指", "银耳饰", "宝宝银饰", "投资金", "投资银", "投资收藏"
    # ]

    searchNameList = ["壁灯", "吊灯", "吸顶灯", "落地灯", "吊扇灯", "客厅灯", "卧室灯", "LED灯", "照明灯", "灯罩灯", "台灯", "床头灯", "应急灯筒灯", "射灯", "天花灯", "厨卫灯", "节能灯",
                      "荧光灯", "白炽灯", "路灯", "水晶灯", "过道灯", "中式灯", "阳台灯", "美式灯", "日式灯", "欧式灯", "韩式灯", "地中海灯", "儿童灯", "轨道灯", "镜前灯", "杀菌灯", "麻将灯", "庭院灯", "卫浴灯", "浴霸灯"]
    headers = {}
    while(1):
        try:
            nowSet=manager.getSet()
            nowKeyword=json.loads(nowSet[pcNum]['keyword'])
            startFlag=nowSet[pcNum]['start']
            startTime=nowSet[pcNum]['startTime']
            page=nowSet[pcNum]['page']
        except:
            print("从爬虫管理平台获取信息失败，等待10秒后重试。")
            traceback.print_exc()
            time.sleep(10)
            continue
        if(startFlag!=1 or time.time()<startTime):
            time.sleep(10)
            print("等待开始")
            continue
        searchNameList=nowKeyword
        for searchName in searchNameList:
            searchListUrl = "https://s.taobao.com/search?q=%s&s=" % (searchName)
            rtn=searchWorker(searchName,int(page),pcNum,searchNameNum)
            if rtn==-1:
                break
            
        manager.setStop(pcNum)
        

    # goods/
    #   2021/
    #       04/
    #           20/
    #               B1_pdd_dengju_20.csv
    #               B1_pdd_dengju_16189063191/         id
    #                   1.jpg

    # "xxx/x/01.jpg,xxxxx/02.jpg"

    # input("全部完成")

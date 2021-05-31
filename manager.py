import requests
import json
import time

url="http://172.16.0.106:5000/"

def getSet():
    r=requests.get(url+"set")
    d=json.loads(r.text)
    return d['data']

def setStop(pcNum):
    r=requests.post(url+"set",json={
        "pcNum": pcNum,
        "start":-1
    })
    d=json.loads(r.text)
    print(d)

def getPauseAndGoOn(pcNum):
    while(1):
        r=requests.get(url+"set")
        d=json.loads(r.text)
        if(d['data'][pcNum]['start']==-1):
            return -1
        if(d['data'][pcNum]['start']==0):
            while 1:
                time.sleep(10)
                print("暂停")
                r=requests.get(url+"set")
                d=json.loads(r.text)
                if d['data'][pcNum]['start']!=0:
                    break
        if(d['data'][pcNum]['start']==1):
             return 1

def postSet(data):
    r=requests.post(url+"set",json=data)
    d=json.loads(r.text)
    print(d)

def getStatus():
    r=requests.get(url+"status")
    d=json.loads(r.text)
    return d

def postStatus(data):
    r=requests.post(url+"status",json=data)
    d=json.loads(r.text)
    print(d)

if __name__ == '__main__':
    print(getSet())
    print(getStatus())

    postSet({
    "pcNum": "X1",
    "start": True,
    "startTime": 46456213,
    "keyword": [
        "壁灯",
        "吊灯",
        "吸顶灯",
        "落地灯",
        "吊扇灯",
        "客厅灯",
        "卧室灯",
        "LED灯",
        "照明灯",
        "灯罩灯",
        "台灯",
        "床头灯",
        "应急灯筒灯",
        "射灯",
        "天花灯",
        "厨卫灯",
        "节能灯",
        "荧光灯",
        "白炽灯",
        "路灯",
        "水晶灯",
        "过道灯",
        "中式灯",
        "阳台灯",
        "美式灯",
        "日式灯",
        "欧式灯",
        "韩式灯",
        "地中海灯",
        "儿童灯",
        "轨道灯",
        "镜前灯",
        "杀菌灯",
        "麻将灯",
        "庭院灯",
        "卫浴灯",
        "浴霸灯"
    ],
    "page": "100"
})

    postStatus({
        "pcNum": "X2",
        "nowPage": 1000,
        "nowKeyword": "灯具",
        "lastTime":"2021.5.27",
        "lastId":"d45645313"
    })